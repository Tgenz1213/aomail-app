import datetime
import logging
import time
from django.contrib.auth.models import User
from aomail.utils import email_processing
from aomail.email_providers.imap.authentication import connect_to_imap
from aomail.models import SocialAPI


LOGGER = logging.getLogger(__name__)


def set_all_contacts(user: User, social_api: SocialAPI):
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
        f"Saving contacts of: {social_api.email} and type_api: {social_api.type_api} for user ID: {user.id}"
    )

    for email in mailbox.fetch(mark_seen=False):
        if email_processing.save_email_sender(
            user, email.from_values.name, email.from_values.email
        ):
            nb_contact_saved += 1

        for to_email in email.to_values:
            if email_processing.save_email_sender(user, to_email.name, to_email.email):
                nb_contact_saved += 1

        for cc_email in email.cc_values:
            if email_processing.save_email_sender(user, cc_email.name, cc_email.email):
                nb_contact_saved += 1

        for bcc_email in email.bcc_values:
            if email_processing.save_email_sender(
                user, bcc_email.name, bcc_email.email
            ):
                nb_contact_saved += 1

    formatted_time = str(datetime.timedelta(seconds=time.time() - start))
    LOGGER.info(
        f"Saved {nb_contact_saved} contacts of: {social_api.email} for user ID: {user.id} in {formatted_time}"
    )
    mailbox.logout()
