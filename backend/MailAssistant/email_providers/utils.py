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


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)



# CLean the documenation + clean the logging messages + optimize the function where its obvious. DO NOT TRY anything that moight not work


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

    # TODO: log also the api if its MICROSFOT or GOOLE
    LOGGER.info(
        f"Starting the process of saving email to database for user ID: {user.id}"
    )
    # like here
    LOGGER.info(
        f"Starting the process of saving email from Microsoft Graph API to database for user ID: {user.id} and email ID: {email_id}"
    )
    # or here
    LOGGER.info(
        f"Starting the process of saving email from Google API to database for user ID: {user.id}"
    )

    if type_api == MICROSOFT:
        access_token = auth_microsoft.refresh_access_token(social_api)

        (
            subject,
            from_name,
            decoded_data,
            email_id,
            sent_date,
            has_attachments,
            is_reply,
        ) = email_operations_microsoft.get_mail_to_db(access_token, None, email_id)

        if Email.objects.filter(provider_id=email_id).exists():
            return True

        sender = Sender.objects.filter(email=from_name[1]).first()

        if not decoded_data:
            LOGGER.info(
                f"No decoded data retrieved from Microsoft Graph API for user ID: {user.id} and email ID: {email_id}"
            )
            return False

        category_dict = email_processing.get_db_categories(user)
        category = Category.objects.get(name=DEFAULT_CATEGORY, user=user)
        rules = Rule.objects.filter(sender=sender)
        rule_category = None

        if rules.exists():
            for rule in rules:
                if rule.block:
                    return True

                if rule.category:
                    category = rule.category
                    rule_category = True

        user_description = social_api.user_description
        language = Preference.objects.get(user=user).language

        if is_reply:
            # Summarize conversation with Search
            email_content = email_processing.preprocess_email(decoded_data)
            user_id = user.id
            search = Search(user_id)
            conversation_summary = search.summarize_conversation(
                subject, email_content, user_description, language
            )
        else:
            # Summarize single email with Search
            email_content = email_processing.preprocess_email(decoded_data)
            user_id = user.id
            search = Search(user_id)
            email_summary = search.summarize_email(
                subject, email_content, user_description, language
            )

        email_processed = claude.categorize_and_summarize_email(
            subject, decoded_data, category_dict, user_description, from_name[1]
        )

        priority: str = email_processed["importance"]
        topic: str = email_processed["topic"]
        answer: str = email_processed["response"]
        relevance: str = email_processed["relevance"]
        flags: dict = email_processed["flags"]
        spam: bool = flags["spam"]
        scam: bool = flags["scam"]
        newsletter: bool = flags["newsletter"]
        notification: bool = flags["notification"]
        meeting: bool = flags["meeting"]
        summary: dict = email_processed["summary"]
        short_summary: str = summary["short"]
        one_line_summary: str = summary["one_line"]

        if not rule_category:
            if topic in category_dict:
                category = Category.objects.get(name=topic, user=user)

        if not sender:
            sender_name, sender_email = from_name[0], from_name[1]
            if not sender_name:
                sender_name = sender_email

            sender = Sender.objects.filter(email=sender_email).first()
            if not sender:
                sender = Sender.objects.create(email=sender_email, name=sender_name)

        try:
            email_entry = Email.objects.create(
                social_api=social_api,
                provider_id=email_id,
                email_provider=MICROSOFT,
                short_summary=short_summary,
                one_line_summary=one_line_summary,
                subject=subject,
                priority=priority,
                sender=sender,
                category=category,
                user=user,
                date=sent_date,
                has_attachments=has_attachments,
                answer=answer,
                relevance=relevance,
                spam=spam,
                scam=scam,
                newsletter=newsletter,
                notification=notification,
                meeting=meeting,
            )

            if is_reply:
                conversation_summary_category = conversation_summary["category"]
                conversation_summary_organization = conversation_summary["organization"]
                conversation_summary_topic = conversation_summary["topic"]
                keypoints: dict = conversation_summary["keypoints"]

                for index, keypoints_list in keypoints.items():
                    for keypoint in keypoints_list:
                        KeyPoint.objects.create(
                            is_reply=True,
                            position=index,
                            category=conversation_summary_category,
                            organization=conversation_summary_organization,
                            topic=conversation_summary_topic,
                            content=keypoint,
                            email=email_entry,
                        )

            else:
                email_summary_category = email_summary["category"]
                email_summary_organization = email_summary["organization"]
                email_summary_topic = email_summary["topic"]

                for keypoint in email_summary["keypoints"]:
                    KeyPoint.objects.create(
                        is_reply=False,
                        category=email_summary_category,
                        organization=email_summary_organization,
                        topic=email_summary_topic,
                        content=keypoint,
                        email=email_entry,
                    )

            contact_name, contact_email = from_name[0], from_name[1]
            Contact.objects.get_or_create(
                user=user, email=contact_email, username=contact_name
            )

            LOGGER.info(
                f"Email ID: {email_id} saved to database successfully for user ID: {user.id} using Microsoft Graph API"
            )
            return True

        except Exception as e:
            LOGGER.error(
                f"An error occurred when trying to create an email with ID {email_id} for user ID: {user.id}: {str(e)}"
            )
            return str(e)

    elif type_api == GOOGLE:
        LOGGER.info(
            f"Starting the process of saving email from Google API to database for user ID: {user.id}"
        )

        email_user = social_api.email
        services = auth_google.authenticate_service(user, email_user)

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
        ) = email_operations_google.get_mail_to_db(services)

        if Email.objects.filter(provider_id=email_id).exists():
            return True

        user_description = (
            social_api.user_description if social_api.user_description else ""
        )
        language = Preference.objects.get(user=user).language

        if not decoded_data:
            LOGGER.info(
                f"No decoded data retrieved from Google API for user ID: {user.id} and email ID: {email_id}"
            )
            return "No decoded data"

        sender = Sender.objects.filter(email=from_name[1]).first()
        category_dict = email_processing.get_db_categories(user)
        category = Category.objects.get(name=DEFAULT_CATEGORY, user=user)
        rules = Rule.objects.filter(sender=sender)
        rule_category = None

        if rules.exists():
            for rule in rules:
                if rule.block:
                    return True

                if rule.category:
                    category = rule.category
                    rule_category = True

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

        priority: str = email_processed["importance"]
        topic: str = email_processed["topic"]
        answer: str = email_processed["response"]
        relevance: str = email_processed["relevance"]
        flags: dict = email_processed["flags"]
        spam: bool = flags["spam"]
        scam: bool = flags["scam"]
        newsletter: bool = flags["newsletter"]
        notification: bool = flags["notification"]
        meeting: bool = flags["meeting"]
        summary: dict = email_processed["summary"]
        short_summary: str = summary["short"]
        one_line_summary: str = summary["one_line"]

        if not rule_category:
            category = Category.objects.get(name=topic, user=user)

        if not sender:
            sender_name, sender_email = from_name[0], from_name[1]
            if not sender_name:
                sender_name = sender_email

            sender = Sender.objects.filter(email=sender_email).first()
            if not sender:
                sender = Sender.objects.create(email=sender_email, name=sender_name)

        try:
            email_entry = Email.objects.create(
                social_api=social_api,
                provider_id=email_id,
                email_provider=GOOGLE,
                short_summary=short_summary,
                one_line_summary=one_line_summary,
                html_content=safe_html,
                subject=subject,
                priority=priority,
                sender=sender,
                category=category,
                user=user,
                date=sent_date,
                has_attachments=has_attachments,
                answer=answer,
                relevance=relevance,
                spam=spam,
                scam=scam,
                newsletter=newsletter,
                notification=notification,
                meeting=meeting,
            )

            if is_reply:
                conversation_summary_category = conversation_summary["category"]
                conversation_summary_organization = conversation_summary["organization"]
                conversation_summary_topic = conversation_summary["topic"]
                keypoints: dict = conversation_summary["keypoints"]

                for index, keypoints_list in keypoints.items():
                    for keypoint in keypoints_list:
                        KeyPoint.objects.create(
                            is_reply=True,
                            position=index,
                            category=conversation_summary_category,
                            organization=conversation_summary_organization,
                            topic=conversation_summary_topic,
                            content=keypoint,
                            email=email_entry,
                        )
            else:
                email_summary_category = email_summary["category"]
                email_summary_organization = email_summary["organization"]
                email_summary_topic = email_summary["topic"]

                for keypoint in email_summary["keypoints"]:
                    KeyPoint.objects.create(
                        is_reply=False,
                        category=email_summary_category,
                        organization=email_summary_organization,
                        topic=email_summary_topic,
                        content=keypoint,
                        email=email_entry,
                    )

            contact_name, contact_email = from_name[0], from_name[1]
            Contact.objects.get_or_create(
                user=user, email=contact_email, username=contact_name
            )

            if cc_info:
                for email, name in cc_info:
                    CC_sender.objects.create(
                        mail_id=email_entry, email=email, name=name
                    )

            if bcc_info:
                for email, name in bcc_info:
                    BCC_sender.objects.create(
                        mail_id=email_entry, email=email, name=name
                    )

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

            LOGGER.info(
                f"Email ID: {email_id} saved to database successfully for user ID: {user.id} using Google API"
            )
            return True

        except Exception as e:
            LOGGER.error(
                f"An error occurred when trying to create an email with ID {email_id} for user ID: {user.id}: {str(e)}"
            )
            return str(e)
