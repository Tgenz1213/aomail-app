"""
Contains common functions for email service provider APIs.

Features:
- ✅ email_to_db: Save email notifications from various email service APIs to the database.
"""

import logging
from django.db import transaction
from django.contrib.auth.models import User
from MailAssistant.ai_providers import claude
from MailAssistant.constants import GOOGLE, MICROSOFT
from MailAssistant.utils.tree_knowledge import Search
from MailAssistant.utils import email_processing
from MailAssistant.models import (
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
)
from MailAssistant.email_providers.microsoft import (
    email_operations as email_operations_microsoft,
)
from MailAssistant.email_providers.google import (
    email_operations as email_operations_google,
)


######################## LOGGING CONFIGURATION ########################
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
        save_email_to_db(processed_email, user, social_api)

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

    if email_data["is_reply"]:
        summary = search.summarize_conversation(
            email_data["subject"], email_content, user_description, language
        )
    else:
        summary = search.summarize_email(
            email_data["subject"], email_content, user_description, language
        )

    from_email = email_data["from_info"][1]

    email_processed = claude.categorize_and_summarize_email(
        email_data["subject"],
        email_data["preprocessed_data"],
        category_dict,
        user_description,
        from_email,
    )

    return {
        "email_data": email_data,
        "email_processed": email_processed,
        "summary": summary,
    }


@transaction.atomic
def save_email_to_db(processed_email: dict, user: User, social_api: SocialAPI):
    """
    Save the processed email to the database.

    Args:
        processed_email (dict): A dictionary containing the processed email data.
        user (User): The user object associated with the email.
        social_api (SocialAPI): An object representing the social API being used.
    """
    email_data = processed_email["email_data"]
    is_reply = email_data["is_reply"]
    email_ai = processed_email["email_processed"]
    summary = processed_email["summary"]

    category, sender = process_email_entities(email_data, user)

    email_entry = create_email_entry(
        email_ai, email_data, user, social_api, category, sender
    )
    create_keypoints(summary, is_reply, email_entry)

    if social_api.type_api == GOOGLE:
        create_cc_bcc_senders(email_data, email_entry)
        create_pictures_and_attachments(email_data, email_entry)


def process_email_entities(
    processed_email: dict, user: User
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
    category_name = processed_email.get("topic", "Uncategorized")
    category = Category.objects.get_or_create(name=category_name, user=user)[0]

    sender_name, sender_email = processed_email["from_info"]
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
            CC_sender.objects.create(mail_id=email_entry, email=email, name=name)

    if bcc_info:
        for email, name in bcc_info:
            BCC_sender.objects.create(mail_id=email_entry, email=email, name=name)


def create_pictures_and_attachments(processed_email: dict, email_entry: Email):
    """
    Create Picture and Attachment entries.

    Args:
        processed_email (dict): A dictionary containing the processed email data.
        email_entry (Email): The Email object to associate the pictures and attachments with.
    """
    for image_path in processed_email.get("image_files", []):
        Picture.objects.create(mail_id=email_entry, picture=image_path)

    for attachment in processed_email.get("attachments", []):
        Attachment.objects.create(
            mail_id=email_entry,
            name=attachment["attachmentName"],
            id_api=attachment["attachmentId"],
        )
