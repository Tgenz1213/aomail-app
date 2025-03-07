"""
Provides email search and operation functions using Google API.

Endpoints:
- ❌ get_mail: Retrieves email details by index or message ID.
"""

import logging
from imap_tools import A, H
from aomail.models import SocialAPI
from aomail.email_providers.imap.authentication import connect_to_imap
from aomail.utils import email_processing
from django.contrib.auth.models import User


LOGGER = logging.getLogger(__name__)


def get_demo_list(user: User, email: str) -> list[str]:
    """
    Retrieves a list of up to 5 email message IDs from the user's Gmail inbox.

    Args:
        user (User): The user object representing the email account owner.
        email (str): The email address of the user.

    Returns:
        list[str]: A list of up to 10 email message IDs from the inbox.
                   Returns an empty list if no messages are found.
    """
    social_api = SocialAPI.objects.get(user=user, email=email)
    mailbox = connect_to_imap(
        social_api.email,
        social_api.imap_config.app_password,
        social_api.imap_config.host,
        social_api.imap_config.port,
        social_api.imap_config.encryption,
    )

    if not mailbox:
        return []

    email_ids = []
    emails = mailbox.fetch(
        reverse=True,
        limit=5,
        mark_seen=False,
    )
    for email in emails:
        message_id = email.headers.get("message-id")
        email_id = message_id[0].split("<")[1].split(">")[0]
        email_ids.append(email_id)

    return email_ids


def get_mail_to_db(social_api: SocialAPI, email_id: str) -> dict:
    """
    Retrieves detailed email information using IMAP protocol, processing it for storage in the database.

    Args:
        social_api (SocialAPI): The social API object containing user and email data.
        email_id (str): The ID of the email to retrieve.

    Returns:
        dict: A dictionary containing the processed email data.
    """
    mailbox = connect_to_imap(
        social_api.email,
        social_api.imap_config.app_password,
        social_api.imap_config.host,
        social_api.imap_config.port,
        social_api.imap_config.encryption,
    )

    if not mailbox:
        return {}

    emails = mailbox.fetch(
        A(
            header=H(
                "Message-ID",
                email_id,
            )
        ),
        limit=5,
        mark_seen=False,
    )
    if not emails:
        return {}

    email = list(emails)[0]

    clear_html = email_processing.html_clear(email.html)
    preprocessed_data = email_processing.preprocess_email(clear_html)

    return {
        "subject": email.subject,
        "from_info": (email.from_values.name, email.from_values.email),
        "email_html": email.html,
        "preprocessed_data": preprocessed_data,
        "safe_html": email.html,
        "email_id": email_id,
        "sent_date": email.date,
        "has_attachments": email.attachments != [],
        "is_reply": email.reply_to != (),
        "cc_info": [(cc.name, cc.email) for cc in email.cc_values],
        "bcc_info": [(bcc.name, bcc.email) for bcc in email.bcc_values],
        "image_files": [],
        "attachments": [],
    }
