"""
File handling schedule tasks ran in django settings

FOR NOW NOTHING WORKS
"""

import logging
from django.utils import timezone
from datetime import timedelta
from backend.MailAssistant.models import GoogleListener
from backend.MailAssistant.email_providers import google_api


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


def debug_cron():
    print(
        "--------------------------IF YOU SEE THIS CELERY TASKS ARE WORKING PROPERLY!!!! ------------------------"
    )


def renew_gmail_subscriptions():
    """
    Resubscribe all Gmail accounts where their subscription is about to expire.

    This function checks for all GoogleListener instances where the last_modified
    date is older than or equal to 3 days from today and attempts to resubscribe
    the associated Gmail accounts to email notifications.
    """
    # Calculate the datetime from which all subscriptions need to be renewed
    today = timezone.now()
    renewal_threshold = today - timedelta(days=3)

    # Get all GoogleListener instances that need to be renewed
    google_listeners = GoogleListener.objects.filter(
        last_modified__lte=renewal_threshold
    )

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
            LOGGER.info(
                f"Successfully renewed the subscription for user: {user}, email: {email}"
            )
