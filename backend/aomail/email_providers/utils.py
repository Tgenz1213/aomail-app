"""
Contains common functions for email service provider APIs.

Features:
- ✅ email_to_db: Save email notifications from various email service APIs to the database.
"""

import logging
import re
from concurrent.futures import ThreadPoolExecutor
from django.db import transaction
from django.contrib.auth.models import User
from aomail.ai_providers import gemini
from aomail.constants import (
    ANSWER_REQUIRED,
    DEFAULT_CATEGORY,
    GOOGLE,
    HIGHLY_RELEVANT,
    IMPORTANT,
    INFORMATIVE,
    MICROSOFT,
    MIGHT_REQUIRE_ANSWER,
    NO_ANSWER_REQUIRED,
    NOT_RELEVANT,
    POSSIBLY_RELEVANT,
    USELESS,
    ENCRYPTION_KEYS,
)
from aomail.utils.tree_knowledge import Search
from aomail.utils import email_processing
from aomail.models import (
    Contact,
    KeyPoint,
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
from aomail.controllers.labels import is_shipping_label, process_label
from aomail.utils.security import encrypt_text


LOGGER = logging.getLogger(__name__)


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
            process_label(
                email_data["from_info"][1],
                email_data["subject"],
                email_data["safe_html"],
                email_entry,
            )

        LOGGER.info(
            f"Email ID: {email_data['email_id']} saved successfully for user ID: {user.id}"
        )
        return True

    except Exception as e:
        LOGGER.error(f"Error saving email for user ID: {user.id}: {str(e)}")
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
        return email_operations_google.get_mail_to_db(social_api, email_id)
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
        return gemini.categorize_and_summarize_email(
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
        short_summary=encrypt_text(
            ENCRYPTION_KEYS["Email"]["short_summary"], email_ai["summary"]["short"]
        ),
        one_line_summary=encrypt_text(
            ENCRYPTION_KEYS["Email"]["one_line_summary"],
            email_ai["summary"]["one_line"],
        ),
        html_content=encrypt_text(
            ENCRYPTION_KEYS["Email"]["html_content"], email_data.get("safe_html", "")
        ),
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


def camel_to_snake(name: str) -> str:
    """
    Converts a camelCase string to snake_case.

    Args:
        name (str): The camelCase string to be converted.

    Returns:
        str: The converted snake_case string.
    """
    # Replace capital letters with underscore + lowercase letter
    snake = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    return snake
