import datetime
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from aomail.email_providers.utils import email_to_db
from aomail.models import Email, SocialAPI
from django.contrib.auth.models import User
from aomail.email_providers.imap.authentication import connect_to_imap


LOGGER = logging.getLogger(__name__)


def save_emails_to_db(user: User):
    """Saves email from last sync date to db

    Args:
        user (User): The user object containing user and email data.
    """
    social_apis = SocialAPI.objects.filter(user=user)
    for social_api in social_apis:
        if social_api.imap_config:
            threading.Thread(target=process_emails, args=(social_api,)).start()


def process_emails(social_api: SocialAPI):
    """Processes emails from the social API.

    Args:
        social_api (SocialAPI): The social API object containing user and email data.
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

    last_email_fetched_date = social_api.last_fetched_date.strftime("%d-%b-%Y")
    start_time = datetime.datetime.now()

    nb_processed_emails = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_email_id = {}

        # if possible fetch only the ids as we will fetch the data twice otherwise its fine and not a big deal
        for email in mailbox.fetch(
            criteria=f"SINCE {last_email_fetched_date}", mark_seen=False
        ):
            message_id = email.headers.get("message-id")
            email_id = message_id[0].split("<")[1].split(">")[0]

            if Email.objects.filter(provider_id=email_id).exists():
                continue

            future = executor.submit(email_to_db, social_api, email_id)
            future_to_email_id[future] = email_id

        for future in as_completed(future_to_email_id):
            email_id = future_to_email_id[future]
            try:
                if future.result():  # Increment count if email_to_db returns True
                    nb_processed_emails += 1
            except Exception as e:
                LOGGER.error(f"Error processing email ID {email_id}: {str(e)}")

    LOGGER.info(
        f"All {nb_processed_emails} emails have been processed for {social_api.email} and type_api {social_api.type_api}"
    )

    social_api.last_fetched_date = start_time
