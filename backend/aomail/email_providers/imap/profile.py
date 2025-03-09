import datetime
import logging
import time
from django.contrib.auth.models import User
from aomail.utils import email_processing
from aomail.email_providers.imap.authentication import connect_to_imap
from aomail.models import SocialAPI


LOGGER = logging.getLogger(__name__)


def get_data(social_api: SocialAPI) -> dict:
    """
    Retrieves email statistics for a given IMAP social API.

    Args:
        social_api (SocialAPI): The social API object containing user and email data.

    Returns:
        dict: A dictionary containing email statistics.
    """
    mailbox = connect_to_imap(
        social_api.email,
        social_api.imap_config.app_password,
        social_api.imap_config.host,
        social_api.imap_config.port,
        social_api.imap_config.encryption,
    )

    num_emails_received = 0
    num_emails_read = 0
    num_emails_archived = 0
    num_emails_starred = 0
    num_emails_sent = 0

    if mailbox:
        num_emails_received = len(mailbox.numbers())
        num_emails_read = len(mailbox.numbers(criteria="SEEN"))
        # not quite accurate though
        num_emails_archived = len(mailbox.numbers(criteria="DELETED"))
        num_emails_starred = len(mailbox.numbers(criteria="FLAGGED"))
        # old date to be sure to get all sent emails
        num_emails_sent = len(mailbox.numbers(criteria=f"SENTSINCE 01-Jan-1990"))
        mailbox.logout()

    return {
        "num_emails_received": num_emails_received,
        "num_emails_read": num_emails_read,
        "num_emails_archived": num_emails_archived,
        "num_emails_starred": num_emails_starred,
        "num_emails_sent": num_emails_sent,
    }


def set_all_contacts(social_api: SocialAPI):
    """Saves all contacts by fetching all emails from user's inbox"""
    mailbox = connect_to_imap(
        social_api.email,
        social_api.imap_config.app_password,
        social_api.imap_config.host,
        social_api.imap_config.port,
        social_api.imap_config.encryption,
    )
    if not mailbox:
        return

    nb_contact_saved = 0
    start = time.time()
    LOGGER.info(
        f"Saving contacts of: {social_api.email} and type_api: {social_api.type_api} for user ID: {social_api.user.id}"
    )

    for email in mailbox.fetch(mark_seen=False):
        if email_processing.save_email_sender(
            social_api.user, email.from_values.name, email.from_values.email
        ):
            nb_contact_saved += 1

        for to_email in email.to_values:
            if email_processing.save_email_sender(
                social_api.user, to_email.name, to_email.email
            ):
                nb_contact_saved += 1

        for cc_email in email.cc_values:
            if email_processing.save_email_sender(
                social_api.user, cc_email.name, cc_email.email
            ):
                nb_contact_saved += 1

        for bcc_email in email.bcc_values:
            if email_processing.save_email_sender(
                social_api.user, bcc_email.name, bcc_email.email
            ):
                nb_contact_saved += 1

    formatted_time = str(datetime.timedelta(seconds=time.time() - start))
    LOGGER.info(
        f"Saved {nb_contact_saved} contacts of: {social_api.email} for user ID: {social_api.user.id} in {formatted_time}"
    )
    mailbox.logout()
