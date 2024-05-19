"""
File handling schedule tasks ran in django settings

NOT WORKING NOR TESTED
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
import logging


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


######################## SCHEDULED TASKS ########################
class Command(BaseCommand):

    def update_subscription_status(self):
        """Update subscription status"""
        from .models import Subscription

        today = timezone.now().date()
        subscriptions = Subscription.objects.filter(end_date__lt=today, is_active=True)

        LOGGER.info("Starting update_subscription_status script")
        for subscription in subscriptions:
            subscription.is_active = False
            subscription.save()
            LOGGER.info(f"Subscription {subscription.id} status updated to inactive.")
