"""
Contains common functions for email service provider APIs.

Features:
- ✅ email_to_db: Save email notifications from various email service APIs to the database.
"""

import datetime
import logging
import os
import re
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from django.db import transaction
from django.contrib.auth.models import User
from aomail.ai_providers import claude
from aomail.constants import (
    ANSWER_REQUIRED,
    DEFAULT_CATEGORY,
    GOOGLE,
    HIGHLY_RELEVANT,
    IMPORTANT,
    INFORMATIVE,
    MEDIA_ROOT,
    MICROSOFT,
    MIGHT_REQUIRE_ANSWER,
    NO_ANSWER_REQUIRED,
    NOT_RELEVANT,
    POSSIBLY_RELEVANT,
    USELESS,
)
from aomail.utils.tree_knowledge import Search
from aomail.utils import email_processing
from aomail.models import (
    Contact,
    KeyPoint,
    Label,
    Preference,
    Rule,
    SocialAPI,
    Category,
    Email,
    Sender,
    CC_sender,
    BCC_sender,
    Picture,
    Attachment,
    Statistics,
)
from aomail.email_providers.microsoft import (
    email_operations as email_operations_microsoft,
)
from aomail.email_providers.google import (
    email_operations as email_operations_google,
)
from aomail.ai_providers.utils import update_tokens_stats


LOGGER = logging.getLogger(__name__)
REQUIRED_SUBJECT_KEYWORDS = [["shipping label", "use by"]]
DATE_PATTERNS = [r"\b\d{2}/\d{2}/\d{4}\b"]
CARRIER_PATTERNS = [
    re.compile(
        r"3\.\s*Drop the parcel off\s*</strong>\s*in the\s*(.*?)\s*drop-off point of your choice\.\s*</p>",
        re.IGNORECASE | re.DOTALL,
    )
]
DEADLINE_PATTERNS = [
    re.compile(
        r"<strong>\s*Postage\s*deadline:\s*</strong>\s*</td>\s*<td[^>]*>\s*(.*?)\s*</td>",
        re.IGNORECASE | re.DOTALL,
    )
]
ITEM_NAME_PATTERNS = [
    re.compile(
        r"<strong>\s*Item:\s*</strong>\s*</td>\s*<td[^>]*>\s*(.*?)\s*<br\s*/?>",
        re.IGNORECASE | re.DOTALL,
    )
]
REQUIRED_SUBJECT_KEYWORDS = [["shipping label", "use by"]]
DATE_PATTERNS = [r"\b\d{2}/\d{2}/\d{4}\b"]
ECOMMERCE_PLATFORMS = ["vinted", "augustin"]
CARRIER_NAMES = {
    "mondialrelay": "mondial_relay",
    "mondial relay": "mondial_relay",
    "Mondial Relay": "mondial_relay",
    "ups": "ups",
    "UPS": "ups",
    "la poste": "la_poste",
    "laposte": "la_poste",
    "chronopost": "chronopost",
    "Chronopost": "chronopost",
    "relais colis": "relais_colis",
    "relaiscolis": "relais_colis",
}


def email_to_db(social_api: SocialAPI, email_id: str = None) -> bool:
    """
    Save email notifications from various email service APIs to the database.

    Args:
        social_api (SocialAPI): The SocialAPI instance associated with the user.
        email_id (Optional[str]): The ID of the email notification (if applicable).

    Returns:
        bool: True if the email was successfully saved, False otherwise.
    """
    user = social_api.user
    api_type = social_api.type_api

    LOGGER.info(
        f"Saving email to database for user ID: {user.id} using {api_type.capitalize()} API"
    )

    try:
        email_data = get_email_data(social_api, email_id)
        if not email_data:
            return False

        if not should_process_email(email_data):
            return True

        processed_email = process_email(email_data, user, social_api)
        email_entry = save_email_to_db(processed_email, user, social_api)

        if is_shipping_label(email_data["subject"]):
            label_data = extract_label_data(
                email_data["from_info"][1], email_entry.html_content
            )
            create_shipping_label(email_entry, label_data)

        LOGGER.info(
            f"Email ID: {email_data['email_id']} saved successfully for user ID: {user.id}"
        )
        return True

    except Exception as e:
        LOGGER.error(f"Error saving email for user ID: {user.id}: {str(e)}")
        return False


def extract_label_data(email_address: str, body: str) -> dict:
    """
    Extracts shipping label information such as carrier name, item name, and postage deadline from the email body.

    Args:
        email_address (str): The email address of the sender.
        body (str): The HTML content of the email body.

    Returns:
        dict: A dictionary containing the carrier name, postage deadline, and item name.
    """
    data = {"carrier": None, "deadline": None, "item_name": None, "platform": None}

    # Normalize the body to remove unwanted characters
    normalized_body = re.sub(r"[\r\n]+", " ", body)  # Replace newlines with spaces
    normalized_body = re.sub(
        r"\s+", " ", normalized_body
    )  # Replace multiple spaces with a single space

    for pattern in CARRIER_PATTERNS:
        carrier_match = pattern.search(normalized_body)
        if carrier_match:
            carrier_name = carrier_match.group(1).strip()
            carrier_name = carrier_name.lower()
            data["carrier"] = CARRIER_NAMES.get(carrier_name, carrier_name)
            break

    for pattern in DEADLINE_PATTERNS:
        deadline_match = pattern.search(normalized_body)
        if deadline_match:
            deadline_str = deadline_match.group(1).strip()
            try:
                data["deadline"] = datetime.datetime.strptime(
                    deadline_str, "%d/%m/%Y %I:%M %p"
                ).isoformat()
            except ValueError:
                try:
                    data["deadline"] = datetime.datetime.strptime(
                        deadline_str, "%d/%m/%Y"
                    ).isoformat()
                except ValueError:
                    data["deadline"] = None
            break

    if not data["carrier"]:
        carrier_pattern_list = "|".join(
            re.escape(name) for name in CARRIER_NAMES.keys()
        )
        carrier_fallback_pattern = re.compile(
            rf"\b({carrier_pattern_list})\b", re.IGNORECASE
        )

        fallback_match = carrier_fallback_pattern.search(normalized_body)
        if fallback_match:
            carrier_key = fallback_match.group(0).lower()
            data["carrier"] = CARRIER_NAMES.get(carrier_key, carrier_key.capitalize())

    for pattern in ITEM_NAME_PATTERNS:
        item_match = pattern.search(normalized_body)
        if item_match:
            data["item_name"] = item_match.group(1).strip()
            break

    for platform in ECOMMERCE_PLATFORMS:
        if platform in email_address:
            data["platform"] = platform
            break

    return data


def create_shipping_label(email: Email, label_data: dict):
    """
    Create the shipping label by merging the official shipping label with a custom message.

    Args:
        email (Email): The email object that contains information about the email message.
        label_data (dict): A dictionary containing the label information such as:
            carrier: The carrier name.
            item_name: The name of the item.
            platform: The platform information.
            postage_deadline: The postage deadline.
    """
    attachment_name = Attachment.objects.get(email=email).name

    if email.social_api.type_api == GOOGLE:
        attachment = email_operations_google.get_attachment_data(
            email.user, email.social_api.email, email.provider_id, attachment_name
        )
    elif email.social_api.type_api == MICROSOFT:
        ...

    pdf_reader = PdfReader(BytesIO(attachment["data"]))
    pdf_writer = PdfWriter()

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        packet = BytesIO()

        if label_data["carrier"] in [
            "mondial_relay",
            "ups",
            "la_poste",
            "chronopost",
            "relais_colis",
        ]:
            orientation = landscape(letter)
        else:
            orientation = landscape(letter)

        canvas_object = canvas.Canvas(packet, pagesize=orientation)
        canvas_object.setFont("Helvetica", 10)

        if label_data["carrier"] in ["mondial_relay", "ups"]:
            if label_data["carrier"] == "mondial_relay":
                y = (
                    pdf_reader.pages[0].mediabox.height / 2
                    - 0.11 * pdf_reader.pages[0].mediabox.height
                )
            else:
                y = (
                    pdf_reader.pages[0].mediabox.height
                    - 0.11 * pdf_reader.pages[0].mediabox.height
                )

            x = pdf_reader.pages[0].mediabox.width / (
                4 if label_data["carrier"] == "mondial_relay" else (3 / 2)
            )
            x -= canvas_object.stringWidth(label_data["item_name"]) / 2
            canvas_object.drawString(x, y, label_data["item_name"])
            y -= 0.018 * pdf_reader.pages[0].mediabox.height

        else:
            if label_data["carrier"] == "la_poste":
                x, y = (
                    1 / 10 * pdf_reader.pages[0].mediabox.width,
                    1 / 5 * pdf_reader.pages[0].mediabox.height
                    - 0.07 * pdf_reader.pages[0].mediabox.height,
                )
            elif label_data["carrier"] == "chronopost":
                x, y = (
                    0.035 * pdf_reader.pages[0].mediabox.width,
                    0.034 * pdf_reader.pages[0].mediabox.height,
                )
            elif label_data["carrier"] == "relais_colis":
                x, y = (
                    3 / 4 * pdf_reader.pages[0].mediabox.width
                    - canvas_object.stringWidth(label_data["item_name"]) / 2,
                    2 / 3 * pdf_reader.pages[0].mediabox.height
                    - 0.034 * pdf_reader.pages[0].mediabox.height,
                )
            canvas_object.drawString(x, y, label_data["item_name"])

        canvas_object.save()
        packet.seek(0)
        new_pdf = PdfReader(packet)
        page.merge_page(new_pdf.pages[0])
        pdf_writer.add_page(page)

    label_name = save_custom_label(
        pdf_writer, label_data["carrier"], label_data["item_name"]
    )
    if label_name:
        save_label_to_db(email, label_data, label_name)


def save_label_to_db(email: Email, label_data: dict, label_name: str):
    """
    Saves the shipping label details to the database.

    Args:
        email (Email): An instance of the Email model representing the email associated with the shipping label.
        label_data (dict): A dictionary containing details about the label.
        label_name (str): The name of the PDF file containing the shipping label.
    """
    Label.objects.create(
        email=email,
        item_name=label_data["item_name"],
        platform=label_data["platform"],
        carrier=label_data["carrier"],
        label_name=label_name,
        postage_deadline=label_data["postage_deadline"],
    )


def save_custom_label(
    pdf_writer: PdfWriter, carrier: str, item_name: str
) -> str | None:
    """
    Saves the shipping label PDF to the specified directory, ensuring the filename is unique.

    Args:
        pdf_writer (PdfWriter): The PdfWriter object containing the modified PDF content.
        carrier (str): The name of the carrier.
        item_name (str): The name of the item.
    """
    try:
        directory = os.path.join(MEDIA_ROOT, "labels")
        label_name = f"{carrier}_{item_name}.pdf"
        n = 1

        while os.path.exists(os.path.join(directory, label_name)):
            label_name = f"{carrier}_{item_name}({n}).pdf"
            n += 1

        with open(os.path.join(directory, label_name), "wb") as f:
            pdf_writer.write(f)

        return label_name

    except FileNotFoundError as e:
        LOGGER.error(f"Directory not found while saving the label: {str(e)}")
        return None
    except IOError as e:
        LOGGER.error(f"IO error occurred while saving the label: {str(e)}")
        return None
    except Exception as e:
        LOGGER.error(f"An unexpected error occurred while saving the label: {str(e)}")
        return None


def is_shipping_label(subject: str) -> bool:
    """
    Determines if the email contains a shipping label based on specific keywords and date patterns.

    Args:
        subject (str): The subject of the email.

    Returns:
        bool: True if the email contains a shipping label, False otherwise.
    """
    for keywords in REQUIRED_SUBJECT_KEYWORDS:
        if all(keyword in subject for keyword in keywords):
            for date_pattern in DATE_PATTERNS:
                if re.search(date_pattern, subject):
                    return True

    return False


def get_email_data(social_api: SocialAPI, email_id: str = None) -> dict:
    """
    Fetch email data from the appropriate API.

    Args:
        social_api (SocialAPI): An object representing the social API being used.
        email_id (str, optional): The ID of the email to fetch. Defaults to None.

    Returns:
        dict: A dictionary containing the fetched email data.
    """
    if social_api.type_api == MICROSOFT:
        return email_operations_microsoft.get_mail_to_db(social_api, email_id)
    elif social_api.type_api == GOOGLE:
        return email_operations_google.get_mail_to_db(social_api)
    else:
        raise ValueError(f"Unsupported API type: {social_api.type_api}")


def should_process_email(email_data: dict) -> bool:
    """
    Check if the email should be processed.

    Args:
        email_data (dict): A dictionary containing the email data.

    Returns:
        bool: True if the email should be processed, False otherwise.
    """
    if Email.objects.filter(provider_id=email_data["email_id"]).exists():
        return False

    from_email = email_data["from_info"][1]

    sender = Sender.objects.filter(email=from_email).first()
    if sender:
        rules = Rule.objects.filter(sender=sender)
        if rules.exists() and any(rule.block for rule in rules):
            return False

    return True


def process_email(email_data: dict, user: User, social_api: SocialAPI) -> dict:
    """
    Process the email data.

    Args:
        email_data (dict): A dictionary containing the email data to be processed.
        user (User): The user object associated with the email.
        social_api (SocialAPI): An object representing the social API being used.

    Returns:
        dict: A dictionary containing the processed email data, including the original
              email data, processed information, and summary.
    """
    user_description = social_api.user_description or ""
    language = Preference.objects.get(user=user).language
    category_dict = email_processing.get_db_categories(user)

    email_content = email_processing.preprocess_email(email_data["preprocessed_data"])
    search = Search(user.id)

    from_email = email_data["from_info"][1]

    def get_summary():
        if email_data["is_reply"]:
            return search.summarize_conversation(
                email_data["subject"], email_content, user_description, language
            )
        else:
            return search.summarize_email(
                email_data["subject"], email_content, user_description, language
            )

    def get_email_processed():
        return claude.categorize_and_summarize_email(
            email_data["subject"],
            email_data["preprocessed_data"],
            category_dict,
            user_description,
            from_email,
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        summary_future = executor.submit(get_summary)
        email_processed_future = executor.submit(get_email_processed)

        summary = summary_future.result()
        email_processed = email_processed_future.result()
        summary = update_tokens_stats(user, summary)
        email_processed = update_tokens_stats(user, email_processed)

    if email_processed["topic"] not in category_dict:
        email_processed["topic"] = DEFAULT_CATEGORY

    return {
        "email_data": email_data,
        "email_processed": email_processed,
        "summary": summary,
    }


@transaction.atomic
def save_email_to_db(processed_email: dict, user: User, social_api: SocialAPI) -> Email:
    """
    Save the processed email to the database.

    Args:
        processed_email (dict): A dictionary containing the processed email data.
        user (User): The user object associated with the email.
        social_api (SocialAPI): An object representing the social API being used.

    Returns:
        email_entry (Email): The saved Email model instance representing the stored email.
    """
    email_data = processed_email["email_data"]
    email_ai = processed_email["email_processed"]
    summary = processed_email["summary"]
    topic = email_ai["topic"]
    is_reply = email_data["is_reply"]
    from_info = email_data["from_info"]

    category, sender = process_email_entities(topic, from_info, user)

    email_entry = create_email_entry(
        email_ai, email_data, user, social_api, category, sender
    )
    create_keypoints(summary, is_reply, email_entry)
    save_stats(email_ai, user)

    if social_api.type_api == GOOGLE:
        create_cc_bcc_senders(email_data, email_entry)
        create_pictures_and_attachments(email_data, email_entry)

    return email_entry


def save_stats(email_ai: dict, user: User):
    """
    Updates the statistical data for a user based on the AI analysis of an email.

    Args:
        email_ai (dict): A dictionary containing AI-generated information about the email.
        user (User): The user object whose statistics are being updated.
    """
    statistics = Statistics.objects.get(user=user)

    statistics.nb_emails_received += 1

    statistics.nb_meeting += 1 if email_ai["flags"]["meeting"] else 0
    statistics.nb_spam += 1 if email_ai["flags"]["spam"] else 0
    statistics.nb_scam += 1 if email_ai["flags"]["scam"] else 0
    statistics.nb_newsletter += 1 if email_ai["flags"]["newsletter"] else 0
    statistics.nb_notification += 1 if email_ai["flags"]["notification"] else 0

    statistics.nb_emails_important += 1 if email_ai["importance"] == IMPORTANT else 0
    statistics.nb_emails_informative += (
        1 if email_ai["importance"] == INFORMATIVE else 0
    )
    statistics.nb_emails_useless += 1 if email_ai["importance"] == USELESS else 0

    statistics.nb_answer_required += 1 if email_ai["response"] == ANSWER_REQUIRED else 0
    statistics.nb_might_require_answer += (
        1 if email_ai["response"] == MIGHT_REQUIRE_ANSWER else 0
    )
    statistics.nb_no_answer_required += (
        1 if email_ai["response"] == NO_ANSWER_REQUIRED else 0
    )

    statistics.nb_highly_relevant += (
        1 if email_ai["relevance"] == HIGHLY_RELEVANT else 0
    )
    statistics.nb_possibly_relevant += (
        1 if email_ai["relevance"] == POSSIBLY_RELEVANT else 0
    )
    statistics.nb_not_relevant += 1 if email_ai["relevance"] == NOT_RELEVANT else 0

    statistics.save()


def process_email_entities(
    topic: str, from_info: tuple, user: User
) -> tuple[Category, Sender]:
    """
    Get or create the email category, sender, and contact.

    Args:
        processed_email (dict): A dictionary containing the processed email data.
        user (User): The user object associated with the email.

    Returns:
        tuple: A tuple containing two elements:
               category: The Category object for the email.
               sender: The Sender object for the email.
    """
    category = Category.objects.get_or_create(name=topic, user=user)[0]

    sender_name, sender_email = from_info
    sender, _ = Sender.objects.get_or_create(
        email=sender_email, defaults={"name": sender_name or sender_email}
    )

    Contact.objects.get_or_create(
        user=user, email=sender_email, defaults={"username": sender_name}
    )

    return category, sender


def create_email_entry(
    email_ai: dict,
    email_data: dict,
    user: User,
    social_api: SocialAPI,
    category: Category,
    sender: Sender,
) -> Email:
    """
    Create the main Email entry in the database.

    Args:
        email_ai (dict): Information provided by the AI processing.
        email_data (dict): Raw email data from the email provider.
        user (User): The user object associated with the email.
        social_api (SocialAPI): The social API object used to fetch the email.
        category (Category): The category object for the email.
        sender (Sender): The sender object for the email.

    Returns:
        Email: The created Email object.
    """
    return Email.objects.create(
        social_api=social_api,
        provider_id=email_data["email_id"],
        email_provider=social_api.type_api,
        short_summary=email_ai["summary"]["short"],
        one_line_summary=email_ai["summary"]["one_line"],
        html_content=email_data.get("safe_html", ""),
        subject=email_data["subject"],
        priority=email_ai["importance"],
        sender=sender,
        category=category,
        user=user,
        date=email_data["sent_date"],
        has_attachments=email_data["has_attachments"],
        answer=email_ai["response"],
        relevance=email_ai["relevance"],
        spam=email_ai["flags"]["spam"],
        scam=email_ai["flags"]["scam"],
        newsletter=email_ai["flags"]["newsletter"],
        notification=email_ai["flags"]["notification"],
        meeting=email_ai["flags"]["meeting"],
    )


def create_keypoints(summary: dict, is_reply: bool, email_entry: Email):
    """
    Create KeyPoint entries for the email.

    Args:
        summary (dict): data from ai aswith keypoiiunts
        is_reply (Email): The Email object to associate the keypoints with.
    """
    if is_reply:
        keypoints = summary["keypoints"]
        for index, keypoints_list in keypoints.items():
            for keypoint in keypoints_list:
                KeyPoint.objects.create(
                    is_reply=True,
                    position=index,
                    category=summary["category"],
                    organization=summary["organization"],
                    topic=summary["topic"],
                    content=keypoint,
                    email=email_entry,
                )
    else:
        for keypoint in summary["keypoints"]:
            KeyPoint.objects.create(
                is_reply=False,
                category=summary["category"],
                organization=summary["organization"],
                topic=summary["topic"],
                content=keypoint,
                email=email_entry,
            )


def create_cc_bcc_senders(processed_email: dict, email_entry: Email):
    """
    Create CC and BCC sender entries.

    Args:
        processed_email (dict): A dictionary containing the processed email data.
        email_entry (Email): The Email object to associate the CC and BCC senders with.
    """
    cc_info = processed_email.get("cc_info", [])
    bcc_info = processed_email.get("bcc_info", [])

    if cc_info:
        for email, name in cc_info:
            CC_sender.objects.create(email_object=email_entry, email=email, name=name)

    if bcc_info:
        for email, name in bcc_info:
            BCC_sender.objects.create(email_object=email_entry, email=email, name=name)


def create_pictures_and_attachments(processed_email: dict, email_entry: Email):
    """
    Create Picture and Attachment entries.

    Args:
        processed_email (dict): A dictionary containing the processed email data.
        email_entry (Email): The Email object to associate the pictures and attachments with.
    """
    for image_path in processed_email.get("image_files", []):
        Picture.objects.create(email=email_entry, path=image_path)

    for attachment in processed_email.get("attachments", []):
        Attachment.objects.create(
            email=email_entry,
            name=attachment["attachmentName"],
            id_api=attachment["attachmentId"],
        )
