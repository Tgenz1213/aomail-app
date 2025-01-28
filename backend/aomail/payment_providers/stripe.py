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
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from aomail.constants import (
    ALLOW_ALL,
    BASE_URL,
    CREDS_PATH,
    ENV,
    GOOGLE,
    MAX_RETRIES,
    MICROSOFT,
)
from aomail.models import SocialAPI, Subscription
from aomail.utils.security import subscription
from aomail.email_providers.microsoft import webhook as webhook_microsoft
from aomail.email_providers.google import webhook as webhook_google


LOGGER = logging.getLogger(__name__)
STRIPE_CREDS = json.load(open(f"{CREDS_PATH}stripe_creds.json"))
PUBLISHABLE_KEY = STRIPE_CREDS["publishable_key"]
SECRET_KEY = STRIPE_CREDS["secret_key"]
WEBHOOK_SECRET = STRIPE_CREDS[ENV + "_webhook_secret"]
PRODUCTS = {
    "start": {
        "monthly": "price_1QaFTRK8H3QtVm1pHDyJyrp5",
        "yearly": "price_1QaFUCK8H3QtVm1pcEpFL8eI",
    },
    "premium": {
        "monthly": "price_1QaFXTK8H3QtVm1prTpGnDY4",
        "yearly": "price_1QaFaoK8H3QtVm1pgEqJYQ1b",
    },
    # "entreprise": {
    #     "monthly": "price_1Q9nbjK8H3QtVm1piHUqrxEf",
    #     "yearly": "price_1Q9nc3K8H3QtVm1p9qgl2Udi",
    # },
    "prod_RTBrMtXObupyaZ": "start",
    "prod_RTBvgvYNKdE6Sg": "premium",
    # "prod_R1rKdtMxUxyRER": "entreprise",
}


stripe.api_key = SECRET_KEY


def cancel_subscription(subscription: Subscription) -> bool:
    """
    Cancels the user's Stripe subscription and updates the subscription status.

    Args:
        subscription (Subscription): The subscription object that will be canceled.

    Returns:
        bool: True if the cancellation was successful or if the subscription is not found, False otherwise.
    """
    if not subscription.subscription_id:
        return True

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            LOGGER.info(
                f"Attempt {attempt}: Stripe subscription {subscription.subscription_id}"
            )
            canceled_subscription = stripe.Subscription.cancel(
                subscription.subscription_id, prorate=True
            )
            LOGGER.info(
                f"for user {subscription.user.id} successfully canceled: {canceled_subscription}"
            )
            return True

        except stripe.InvalidRequestError as e:
            if e.http_status == 404 and "No such subscription" in str(e):
                LOGGER.warning(
                    f"Attempt {attempt}: Stripe subscription {subscription.subscription_id} not found"
                )
                LOGGER.warning(
                    f"for user {subscription.user.id}. Assuming the user canceled it or webhook issue."
                )
                return True
            else:
                LOGGER.error(
                    f"Attempt {attempt}: Failed to cancel Stripe subscription {subscription.subscription_id} for user {subscription.user.id}: {str(e)}"
                )

        except stripe.StripeError as e:
            LOGGER.error(
                f"Attempt {attempt}: Failed to cancel Stripe subscription {subscription.subscription_id} for user {subscription.user.id}: {str(e)}"
            )

        except Subscription.DoesNotExist:
            LOGGER.error(
                f"Attempt {attempt}: Subscription for user {subscription.user.id} not found in the database."
            )
            return False

        except Exception as e:
            LOGGER.critical(
                f"Attempt {attempt}: An unexpected error occurred while canceling the subscription for user {subscription.user.id}: {e}"
            )

        if attempt < MAX_RETRIES:
            LOGGER.info(
                f"Retrying cancellation (Attempt {attempt + 1} of {MAX_RETRIES})..."
            )

    LOGGER.error(
        f"Failed to cancel Stripe subscription {subscription.subscription_id} for user {subscription.user.id} after {MAX_RETRIES} attempts."
    )
    return False


@api_view(["POST"])
@subscription(ALLOW_ALL)
def create_checkout_session(request: HttpRequest):
    """
    Creates a Stripe Checkout session for a subscription.

    Args:
        request (HttpRequest): The HTTP request object containing product and frequency.

    Returns:
        Response: A JSON response containing the session ID or an error message.
    """
    try:
        user = request.user
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
            success_url=f"{BASE_URL}subscription?stripe-payment-success=true",
            cancel_url=f"{BASE_URL}subscription?stripe-payment-success=false",
            mode="subscription",
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
            metadata={"user_id": user.id, "plan": product},
        )

        return Response(
            {"id": checkout_session.id},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([AllowAny])
@csrf_exempt
def webhook(request: HttpRequest) -> Response:
    """
    Unified Stripe webhook listener that processes various Stripe events.
    """
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", None)
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except ValueError as e:
        LOGGER.error(f"Stripe webhook invalid payload: {str(e)}")
        return Response(
            {"error": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST
        )
    except stripe.SignatureVerificationError as e:
        LOGGER.error(f"Stripe webhook Invalid signature: {str(e)}")
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
    elif event["type"] == "checkout.session.completed":
        handle_checkout_session_completed(event)
    else:
        LOGGER.warning(f"Unhandled event type: {event['type']}")

    return Response({"status": "success"}, status=status.HTTP_200_OK)


def handle_checkout_session_completed(event: dict):
    """
    Handle checkout.session.completed event.

    This function activates a subscription after a successful checkout session.
    It updates the user's subscription status and the selected plan in the database.
    """

    LOGGER.info(f"Received Stripe webhook for event: {event['type']}")

    try:
        payload: dict = event["data"]["object"]
        metadata: dict = payload.get("metadata")

        if not metadata:
            LOGGER.warning(
                f"Received empty metadata in checkout.session.completed event. Payload: {payload}"
            )
            return

        plan = metadata.get("plan")
        user_id = metadata.get("user_id")

        if not user_id or not plan:
            LOGGER.warning(f"Metadata missing 'user_id' or 'plan'. Payload: {payload}")
            return

        user = User.objects.get(id=user_id)
        subscription = Subscription.objects.get(user=user)

        subscription.is_trial = False
        subscription.is_active = True
        subscription.subscription_id = payload.get("subscription")
        subscription.plan = plan
        subscription.save()

        # Resubscribe user to email notifications in case
        social_apis = SocialAPI.objects.filter(user=user)
        for social_api in social_apis:
            if social_api.type_api == GOOGLE:
                webhook_google.check_and_resubscribe_to_missing_resources(
                    social_api.type_api, user, social_api.email
                )
            elif social_api.type_api == MICROSOFT:
                webhook_microsoft.check_and_resubscribe_to_missing_resources(
                    user, social_api.email
                )

        LOGGER.info(
            f"Payment succeeded for user ID {user.id}, Plan: {plan} activated successfully."
        )

    except User.DoesNotExist:
        LOGGER.error(f"User with ID {user_id} not found. Payload: {payload}")
    except Subscription.DoesNotExist:
        LOGGER.error(
            f"Subscription for user ID {user_id} not found. Payload: {payload}"
        )
    except Exception as e:
        LOGGER.error(
            f"Error processing checkout.session.completed: {str(e)}. Payload: {payload}"
        )


def handle_cancelled_subscription(event: dict):
    """
    Handle customer.subscription.deleted event.

    This function deactivates a user's subscription in the application when Stripe sends a cancellation event.
    If the subscription exists in the database, it is marked as inactive.
    """

    LOGGER.info(f"Received Stripe webhook for event: {event['type']}")

    try:
        subscription_data = event["data"]["object"]
        subscription_id = subscription_data["id"]

        subscription = Subscription.objects.get(subscription_id=subscription_id)
        subscription.is_active = False
        subscription.save()

        LOGGER.info(
            f"Subscription {subscription_id} for user ID {subscription.user.id} cancelled successfully."
        )

    except Subscription.DoesNotExist:
        LOGGER.warning(
            f"Subscription ID {subscription_id} not found in the database. Ignoring cancellation event."
        )
    except Exception as e:
        LOGGER.error(
            f"Error handling subscription cancellation: {str(e)}. Subscription data: {subscription_data}"
        )


def handle_updated_subscription(event: dict):
    """
    Handle customer.subscription.updated event.

    This function updates the subscription plan when Stripe sends an update event.
    The new plan is reflected in the user's subscription in the application.
    """

    LOGGER.info(f"Received Stripe webhook for event: {event['type']}")

    try:
        subscription_data = event["data"]["object"]
        subscription_id = subscription_data["id"]
        product_id = subscription_data["plan"]["product"]
        plan = PRODUCTS[product_id]

        subscription = Subscription.objects.get(subscription_id=subscription_id)
        subscription.plan = plan
        subscription.save()

        # Resubscribe user to email notifications in case
        social_apis = SocialAPI.objects.filter(user=subscription.user)
        for social_api in social_apis:
            if social_api.type_api == GOOGLE:
                webhook_google.check_and_resubscribe_to_missing_resources(
                    social_api.type_api, subscription.user, social_api.email
                )
            elif social_api.type_api == MICROSOFT:
                webhook_microsoft.check_and_resubscribe_to_missing_resources(
                    subscription.user, social_api.email
                )

        LOGGER.info(
            f"Subscription {subscription_id} for user ID {subscription.user.id} updated to {plan} plan successfully."
        )
    except (KeyError, Subscription.DoesNotExist) as e:
        LOGGER.error(f"Failed to update subscription {subscription_id}: {str(e)}")
    except Exception as e:
        LOGGER.error(
            f"Unexpected error while updating subscription {subscription_id}: {str(e)}"
        )


def handle_payment_failed(event: dict):
    """
    Handle invoice.payment_failed event.

    This function marks a subscription as inactive in the application when a payment fails.
    If the subscription is found, it is deactivated.
    """

    LOGGER.info(f"Received Stripe webhook for event: {event['type']}")

    try:
        invoice_data = event["data"]["object"]
        subscription_id = invoice_data["subscription"]

        subscription = Subscription.objects.get(subscription_id=subscription_id)
        subscription.is_active = False
        subscription.save()

        LOGGER.warning(
            f"Payment failed for subscription {subscription_id} for user ID {subscription.user.id}. Subscription marked as inactive."
        )
    except Subscription.DoesNotExist:
        LOGGER.error(
            f"Subscription ID {subscription_id} not found in the database. Unable to mark as inactive."
        )
    except Exception as e:
        LOGGER.error(
            f"Error handling payment_failed event: {str(e)}. Invoice data: {invoice_data}"
        )


def handle_payment_succeeded(event: dict):
    """
    Handle the invoice.payment_succeeded event.

    This function reactivates a subscription when an invoice is successfully paid.
    If the subscription is found in the database, it is marked as active again.
    """

    LOGGER.info(f"Received Stripe webhook for event: {event['type']}")

    try:
        invoice_data = event["data"]["object"]
        subscription_id = invoice_data["subscription"]

        subscription = Subscription.objects.get(subscription_id=subscription_id)
        subscription.is_active = True
        subscription.save()

        LOGGER.info(
            f"Subscription {subscription_id} for user ID {subscription.user.id} reactivated successfully."
        )
    except Subscription.DoesNotExist:
        LOGGER.warning(
            f"Subscription ID {subscription_id} not found in the database. Ignoring payment_succeeded event."
        )
    except Exception as e:
        LOGGER.error(
            f"Error handling payment_succeeded event: {str(e)}. Invoice data: {invoice_data}"
        )
