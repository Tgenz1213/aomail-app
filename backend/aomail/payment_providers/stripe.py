"""
Handles Stripe payment processes, including subscription management and webhook event handling.

Endpoints:
- ✅ create_checkout_session: Creates a Stripe Checkout session for a subscription.
- ✅ webhook: Unified Stripe webhook listener that processes various Stripe events.
"""

import stripe
import json
import logging
from rest_framework import status
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from aomail.constants import BASE_URL, CREDS_PATH, ENV
from aomail.models import Subscription


LOGGER = logging.getLogger(__name__)
STRIPE_CREDS = json.load(open(f"{CREDS_PATH}stripe_creds.json"))
PUBLISHABLE_KEY = STRIPE_CREDS["publishable_key"]
SECRET_KEY = STRIPE_CREDS["secret_key"]
WEBHOOK_SECRET = STRIPE_CREDS[ENV + "_webhook_secret"]
PRODUCTS = {
    "start": {
        "monthly": "price_1Q9nJBK8H3QtVm1pZFyeR37V",
        "yearly": "price_1Q9nXSK8H3QtVm1pNkx2zscT",
    },
    "premium": {
        "monthly": "price_1Q9na2K8H3QtVm1peN7oqrVS",
        "yearly": "price_1Q9naRK8H3QtVm1p8qftrgvj",
    },
    "entreprise": {
        "monthly": "price_1Q9nbjK8H3QtVm1piHUqrxEf",
        "yearly": "price_1Q9nc3K8H3QtVm1p9qgl2Udi",
    },
}
PLANS = {
    "prod_R1r1SojHfBmNRn": "start",
    "prod_R1rIjwktRkHlkX": "premium",
    "prod_R1rKdtMxUxyRER": "entreprise",
}


stripe.api_key = SECRET_KEY


@api_view(["POST"])
def create_checkout_session(request: HttpRequest):
    """
    Creates a Stripe Checkout session for a subscription.

    Args:
        request (HttpRequest): The HTTP request object containing product and frequency.

    Returns:
        Response: A JSON response containing the session ID or an error message.
    """
    try:
        parameters: dict = json.loads(request.body)
        product = parameters.get("product")
        frequency = parameters.get("frequency")

        if product not in PRODUCTS or frequency not in PRODUCTS[product]:
            return Response(
                {"error": "Invalid product or frequency"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        price_id = PRODUCTS[product][frequency]
        checkout_session = stripe.checkout.Session.create(
            success_url=f"{BASE_URL}settings?stripe-payment-success=true",
            cancel_url=f"{BASE_URL}settings?stripe-payment-success=false",
            mode="subscription",
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
        )

        return Response(
            {"id": checkout_session.id},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
def webhook(request: HttpRequest) -> Response:
    """
    Unified Stripe webhook listener that processes various Stripe events.

    Args:
        request (HttpRequest): The HTTP request object containing the event data.

    Returns:
        Response: A JSON response indicating the status of the webhook processing.
    """
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except ValueError as e:
        LOGGER.error(f"Invalid payload: {str(e)}")
        return Response(
            {"error": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST
        )
    except stripe.SignatureVerificationError as e:
        LOGGER.error(f"Invalid signature: {str(e)}")
        return Response(
            {"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST
        )

    if event["type"] == "customer.subscription.deleted":
        handle_cancelled_subscription(event)
    elif event["type"] == "customer.subscription.updated":
        handle_updated_subscription(event)
    elif event["type"] == "invoice.payment_failed":
        handle_payment_failed(event)
    elif event["type"] == "invoice.payment_succeeded":
        handle_payment_succeeded(event)
    else:
        LOGGER.warning(f"Unhandled event type: {event['type']}")

    return Response({"status": "success"}, status=status.HTTP_200_OK)


def handle_cancelled_subscription(event: dict):
    """
    Handle customer.subscription.deleted event to deactivate the subscription.

    Args:
        event (dict): The Stripe event data containing subscription information.
    """
    subscription_data = event["data"]["object"]
    subscription_id = subscription_data["id"]

    try:
        subscription = Subscription.objects.get(subscription_id=subscription_id)
        subscription.is_active = False
        subscription.save()

        LOGGER.info(f"Subscription {subscription_id} cancelled successfully.")
    except Subscription.DoesNotExist:
        LOGGER.error(f"Subscription {subscription_id} not found.")


def handle_updated_subscription(event: dict):
    """
    Handle customer.subscription.updated event to update subscription details.

    Args:
        event (dict): The Stripe event data containing updated subscription information.
    """
    subscription_data = event["data"]["object"]
    subscription_id = subscription_data["id"]
    plan = PLANS[subscription_data["plan"]["id"]]

    try:
        subscription = Subscription.objects.get(subscription_id=subscription_id)
        subscription.plan = plan
        subscription.save()

        LOGGER.info(f"Subscription {subscription_id} updated successfully.")
    except Subscription.DoesNotExist:
        LOGGER.error(f"Subscription {subscription_id} not found.")


def handle_payment_failed(event: dict):
    """
    Handle invoice.payment_failed event to deactivate the subscription.

    Args:
        event (dict): The Stripe event data containing payment failure information.
    """
    invoice_data = event["data"]["object"]
    subscription_id = invoice_data["subscription"]

    try:
        subscription = Subscription.objects.get(subscription_id=subscription_id)
        subscription.is_active = False
        subscription.save()

        LOGGER.warning(
            f"Payment failed for subscription {subscription_id}. Subscription marked as inactive."
        )
    except Subscription.DoesNotExist:
        LOGGER.error(f"Subscription {subscription_id} not found.")


def handle_payment_succeeded(event: dict):
    """
    Handle invoice.payment_succeeded event to reactivate the subscription.

    Args:
        event (dict): The Stripe event data containing payment success information.
    """
    invoice_data = event["data"]["object"]
    subscription_id = invoice_data["subscription"]

    try:
        subscription = Subscription.objects.get(subscription_id=subscription_id)
        subscription.is_active = True
        subscription.save()

        LOGGER.info(f"Payment succeeded for subscription {subscription_id}.")
    except Subscription.DoesNotExist:
        LOGGER.error(f"Subscription {subscription_id} not found.")
