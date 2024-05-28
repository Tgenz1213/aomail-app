"""
File handling schedule tasks ran in django settings

FOR NOW NOTHING WORKS
"""

import logging
import time
from django.utils import timezone
from datetime import timedelta
from MailAssistant.models import GoogleListener
from MailAssistant.email_providers import google_api


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


######################## SCHEDULED TASKS ########################
'''def update_subscription_status(self):
    """Update subscription status"""
    from .models import Subscription

    today = timezone.now().date()
    subscriptions = Subscription.objects.filter(end_date__lt=today, is_active=True)

    LOGGER.info("Starting update_subscription_status script")
    for subscription in subscriptions:
        subscription.is_active = False
        subscription.save()
        LOGGER.info(f"Subscription {subscription.id} status updated to inactive.")'''


def renew_gmail_subscriptions():
    """
    Resubscribe all Gmail accounts where their subscription is about to expire.

    This function checks for all GoogleListener instances where the last_modified
    date is older than or equal to 3 days from today and attempts to resubscribe
    the associated Gmail accounts to email notifications.
    """
    start_time = time.time()

    # Calculate the datetime from which all subscriptions need to be renewed
    today = timezone.now()
    renewal_threshold = today - timedelta(days=3)

    # Get all GoogleListener instances that need to be renewed
    google_listeners = GoogleListener.objects.filter(
        last_modified__lte=renewal_threshold
    )

    nb_subrenew = 0

    for google_listener in google_listeners:
        social_api = google_listener.social_api
        user = social_api.user
        email = social_api.email

        subscribed = google_api.subscribe_to_email_notifications(user, email)
        if not subscribed:
            LOGGER.critical(
                f"Failed to renew the subscription for user: {user}, email: {email}"
            )
        else:
            google_listener.last_modified = today
            google_listener.save()
            nb_subrenew += 1
            LOGGER.info(
                f"Successfully renewed the subscription for user: {user}, email: {email}"
            )

    elapsed_time = time.time() - start_time
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_time = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    LOGGER.info(f"Renewed {nb_subrenew} subscriptions in {formatted_time}.")
