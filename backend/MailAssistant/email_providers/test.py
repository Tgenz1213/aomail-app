"""
TODO:
- split email_to_db + separate call depending on the api
"""

import logging
from MailAssistant.ai_providers import claude
from MailAssistant.constants import (
    DEFAULT_CATEGORY,
    GOOGLE,
    MICROSOFT,
)
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
from MailAssistant.email_providers.google import (
    authentication as auth_google,
    email_operations as email_operations_google,
)
from MailAssistant.email_providers.microsoft import (
    authentication as auth_microsoft,
    email_operations as email_operations_microsoft,
)

LOGGER = logging.getLogger(__name__)


def email_to_db(social_api: SocialAPI, email_id: str = None) -> bool | str:
    """
    Saves email notifications from Google or Microsoft Graph API listener to the database.

    Args:
        social_api (SocialAPI): The SocialAPI instance associated with the user.
        email_id (str): The ID of the email notification from Microsoft Graph API.

    Returns:
        bool | str: True if the email was successfully saved, False if there was an issue saving the email,
                    or an error message if an exception occurred.
    """
    type_api = social_api.type_api
    user = social_api.user

    LOGGER.info(
        f"Starting the process of saving email to database for user ID: {user.id}"
    )

    try:
        if type_api == MICROSOFT:
            return process_microsoft_email(social_api, email_id)
        elif type_api == GOOGLE:
            return process_google_email(social_api)
        else:
            raise ValueError(f"Unsupported API type: {type_api}")
    except Exception as e:
        LOGGER.error(
            f"An error occurred when processing email for user ID: {user.id}: {str(e)}"
        )
        return str(e)


def process_microsoft_email(social_api: SocialAPI, email_id: str) -> bool:
    access_token = auth_microsoft.refresh_access_token(social_api)
    email_data = email_operations_microsoft.get_mail_to_db(access_token, None, email_id)
    return process_email(social_api, email_data, MICROSOFT)


def process_google_email(social_api: SocialAPI) -> bool:
    email_user = social_api.email
    services = auth_google.authenticate_service(social_api.user, email_user)
    email_data = email_operations_google.get_mail_to_db(services)
    return process_email(social_api, email_data, GOOGLE)


def process_email(social_api: SocialAPI, email_data: Tuple, provider: str) -> bool:
    user = social_api.user
    if provider == MICROSOFT:
        (
            subject,
            from_name,
            decoded_data,
            email_id,
            sent_date,
            has_attachments,
            is_reply,
        ) = email_data
        safe_html, cc_info, bcc_info, image_files, attachments = (
            None,
            None,
            None,
            None,
            None,
        )
    elif provider == GOOGLE:
        (
            subject,
            from_name,
            decoded_data,
            safe_html,
            email_id,
            sent_date,
            has_attachments,
            is_reply,
            cc_info,
            bcc_info,
            image_files,
            attachments,
        ) = email_data

    if Email.objects.filter(provider_id=email_id).exists():
        return True

    if not decoded_data:
        LOGGER.info(
            f"No decoded data retrieved for user ID: {user.id} and email ID: {email_id}"
        )
        return False

    sender = get_or_create_sender(from_name)
    category, rule_category = get_category_and_rule(user, sender)

    if should_block_email(sender):
        return True

    email_processed = process_email_content(
        social_api, subject, decoded_data, from_name, is_reply
    )

    if not rule_category:
        category = update_category(user, email_processed["topic"], category)

    try:
        with transaction.atomic():
            email_entry = create_email_entry(
                social_api,
                email_processed,
                email_id,
                provider,
                subject,
                sender,
                category,
                sent_date,
                has_attachments,
                safe_html,
            )
            create_keypoints(email_entry, email_processed, is_reply)
            create_contact(user, from_name)

            if provider == GOOGLE:
                process_google_specific_data(
                    email_entry, cc_info, bcc_info, image_files, attachments
                )

        LOGGER.info(
            f"Email ID: {email_id} saved to database successfully for user ID: {user.id}"
        )
        return True
    except Exception as e:
        LOGGER.error(
            f"An error occurred when creating email with ID {email_id} for user ID: {user.id}: {str(e)}"
        )
        return str(e)


def get_or_create_sender(from_name: Tuple[str, str]) -> Sender:
    sender_name, sender_email = from_name
    sender = Sender.objects.filter(email=sender_email).first()
    if not sender:
        sender = Sender.objects.create(
            email=sender_email, name=sender_name or sender_email
        )
    return sender


def get_category_and_rule(user: User, sender: Sender) -> Tuple[Category, bool]:
    category = Category.objects.get(name=DEFAULT_CATEGORY, user=user)
    rules = Rule.objects.filter(sender=sender)
    rule_category = False

    for rule in rules:
        if rule.block:
            return None, True
        if rule.category:
            category = rule.category
            rule_category = True
            break

    return category, rule_category


def should_block_email(sender: Sender) -> bool:
    return Rule.objects.filter(sender=sender, block=True).exists()


def process_email_content(
    social_api: SocialAPI,
    subject: str,
    decoded_data: str,
    from_name: Tuple[str, str],
    is_reply: bool,
) -> Dict:
    user = social_api.user
    user_description = social_api.user_description or ""
    language = Preference.objects.get(user=user).language
    category_dict = email_processing.get_db_categories(user)

    email_content = email_processing.preprocess_email(decoded_data)
    search = Search(user.id)

    if is_reply:
        conversation_summary = search.summarize_conversation(
            subject, email_content, user_description, language
        )
    else:
        email_summary = search.summarize_email(
            subject, email_content, user_description, language
        )

    email_processed = claude.categorize_and_summarize_email(
        subject, decoded_data, category_dict, user_description, from_name[1]
    )

    if is_reply:
        email_processed["conversation_summary"] = conversation_summary
    else:
        email_processed["email_summary"] = email_summary

    return email_processed


def update_category(user: User, topic: str, default_category: Category) -> Category:
    return Category.objects.get(name=topic, user=user) if topic else default_category


def create_email_entry(
    social_api: SocialAPI,
    email_processed: Dict,
    email_id: str,
    provider: str,
    subject: str,
    sender: Sender,
    category: Category,
    sent_date: datetime,
    has_attachments: bool,
    safe_html: str = None,
) -> Email:
    return Email.objects.create(
        social_api=social_api,
        provider_id=email_id,
        email_provider=provider,
        short_summary=email_processed["summary"]["short"],
        one_line_summary=email_processed["summary"]["one_line"],
        html_content=safe_html,
        subject=subject,
        priority=email_processed["importance"],
        sender=sender,
        category=category,
        user=social_api.user,
        date=sent_date,
        has_attachments=has_attachments,
        answer=email_processed["response"],
        relevance=email_processed["relevance"],
        spam=email_processed["flags"]["spam"],
        scam=email_processed["flags"]["scam"],
        newsletter=email_processed["flags"]["newsletter"],
        notification=email_processed["flags"]["notification"],
        meeting=email_processed["flags"]["meeting"],
    )


def create_keypoints(email_entry: Email, email_processed: Dict, is_reply: bool):
    if is_reply:
        conversation_summary = email_processed["conversation_summary"]
        for index, keypoints_list in conversation_summary["keypoints"].items():
            for keypoint in keypoints_list:
                KeyPoint.objects.create(
                    is_reply=True,
                    position=index,
                    category=conversation_summary["category"],
                    organization=conversation_summary["organization"],
                    topic=conversation_summary["topic"],
                    content=keypoint,
                    email=email_entry,
                )
    else:
        email_summary = email_processed["email_summary"]
        for keypoint in email_summary["keypoints"]:
            KeyPoint.objects.create(
                is_reply=False,
                category=email_summary["category"],
                organization=email_summary["organization"],
                topic=email_summary["topic"],
                content=keypoint,
                email=email_entry,
            )


def create_contact(user: User, from_name: Tuple[str, str]):
    contact_name, contact_email = from_name
    Contact.objects.get_or_create(user=user, email=contact_email, username=contact_name)


def process_google_specific_data(
    email_entry: Email,
    cc_info: List,
    bcc_info: List,
    image_files: List,
    attachments: List,
):
    if cc_info:
        for email, name in cc_info:
            CC_sender.objects.create(mail_id=email_entry, email=email, name=name)

    if bcc_info:
        for email, name in bcc_info:
            BCC_sender.objects.create(mail_id=email_entry, email=email, name=name)

    if image_files:
        for image_path in image_files:
            Picture.objects.create(mail_id=email_entry, picture=image_path)

    if attachments:
        for attachment in attachments:
            Attachment.objects.create(
                mail_id=email_entry,
                name=attachment["attachmentName"],
                id_api=attachment["attachmentId"],
            )
