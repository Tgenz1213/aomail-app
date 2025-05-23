"""
Module for handling scheduled tasks related to file handling in Django settings.
"""

import logging
import time
from django.utils import timezone
from datetime import timedelta
from aomail.models import GoogleListener
from aomail.email_providers.google import webhook as google_webhook
from aomail.constants import ENV


LOGGER = logging.getLogger(__name__)


def renew_gmail_subscriptions():
    """
    Resubscribe all Gmail accounts where their subscription is about to expire.

    This function checks for all GoogleListener instances where the last_modified
    date is older than or equal to 3 days from today and attempts to resubscribe
    the associated Gmail accounts to email notifications.
    """
    start_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    LOGGER.info(
        f"{start_time} - [{ENV}] Starting the subscription renewal process for Gmail accounts."
    )
    start_time = time.time()

    # Calculate the datetime from which all subscriptions need to be renewed
    today = timezone.now()
    renewal_threshold = today - timedelta(days=3)

    # Get all GoogleListener instances that need to be renewed
    google_listeners = GoogleListener.objects.filter(
        last_modified__lte=renewal_threshold
    ).exclude(social_api__user__subscription__is_block=True)

    nb_subrenew = 0

    for google_listener in google_listeners:
        social_api = google_listener.social_api

        if not social_api:
            continue

        user = social_api.user
        email = social_api.email

        subscribed = google_webhook.subscribe_to_email_notifications(user, email)
        if not subscribed:
            LOGGER.critical(
                f"Failed to renew the subscription for user ID: {user.id}, SocialAPI ID: {social_api.id}"
            )
        else:
            google_listener.last_modified = today
            google_listener.save()
            nb_subrenew += 1
            LOGGER.info(
                f"Successfully renewed the subscription for user ID: {user.id}, SocialAPI ID: {social_api.id}"
            )

    elapsed_time = time.time() - start_time
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_time = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    LOGGER.info(f"Renewed {nb_subrenew} subscriptions in {formatted_time}.")
