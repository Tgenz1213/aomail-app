"""
Handles webhook notifications from Google API.

Endpoints:
- ✅ receive_mail_notifications: Handles requests containing email notifications.
"""

import base64
import logging
import threading
import json
from rest_framework import status
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.template.loader import render_to_string
from django.core.mail import send_mail
from aomail.constants import (
    EMAIL_ADMIN,
    EMAIL_NO_REPLY,
    GOOGLE,
    GOOGLE_PROJECT_ID,
    GOOGLE_TOPIC_NAME,
)
from aomail.email_providers.google.authentication import authenticate_service
from aomail.models import SocialAPI, Subscription
from aomail.email_providers.utils import email_to_db
from aomail.controllers.authentication import subscribe_listeners


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


def check_and_resubscribe_to_missing_resources(type_api: str, user: User, email: str):
    """
    Check all subscriptions for the given user and resubscribe to missing resources (email).

    Args:
        type_api (str): The email service API used.
        user (User): The Django User object.
        email (str): The email address of the user.
    """
    subscribe_listeners(type_api, user, email)


@api_view(["POST"])
@permission_classes([AllowAny])
def receive_mail_notifications(request: HttpRequest) -> Response:
    """
    Process email notifications from Google listener.

    Args:
        request (HttpRequest): The HTTP request object containing the email notification data.

    Returns:
        Response: A JSON response indicating the status of the notification processing.
    """
    try:
        envelope = json.loads(request.body.decode("utf-8"))
        message_data = envelope["message"]

        decoded_data = base64.b64decode(message_data["data"]).decode("utf-8")
        decoded_json: dict = json.loads(decoded_data)
        email = decoded_json.get("emailAddress")

        LOGGER.info(
            f"Email notification received from Google API. Starting email processing for: {email}"
        )

        try:
            social_api = SocialAPI.objects.get(email=email)
            subscription = Subscription.objects.get(user=social_api.user)

            if subscription.is_block:
                LOGGER.info(
                    f"User with email: {email} is blocked. Unsubscribing user from Google notifications."
                )
                unsubscribe_from_email_notifications(social_api.user, email)
            else:

                def process_email():
                    result = email_to_db(social_api)

                    if not result:
                        LOGGER.critical(
                            f"[Attempt {1}] Failed to process email with AI for email: {email}"
                        )
                        context = {
                            "error": result,
                            "attempt_number": 1,
                            "email": email,
                            "email_provider": GOOGLE,
                            "user": social_api.user,
                        }
                        email_html = render_to_string("ai_failed_email.html", context)
                        send_mail(
                            subject="Critical Alert: Email Processing Failure",
                            message="",
                            recipient_list=[EMAIL_ADMIN],
                            from_email=EMAIL_NO_REPLY,
                            html_message=email_html,
                            fail_silently=False,
                        )

                threading.Thread(target=process_email).start()

        except SocialAPI.DoesNotExist:
            pass

        return Response({"status": "Notification received"}, status=status.HTTP_200_OK)

    except IntegrityError:
        return Response(
            {"status": "Email already exists in database"}, status=status.HTTP_200_OK
        )

    except Exception as e:
        LOGGER.error(f"Error processing the notification: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def subscribe_to_email_notifications(user: User, email: str) -> bool:
    """
    Subscribe the user to email notifications via Google Gmail API.

    Args:
        user (User): The Django User object.
        email (str): The email address of the user.

    Returns:
        bool: True if subscription was successful, False otherwise.
    """
    try:
        LOGGER.info(
            f"Initiating subscription to Google email notifications for user ID: {user.id} with email: {email}"
        )
        services = authenticate_service(user, email, ["gmail"])
        if services is None:
            return False

        gmail = services["gmail"]

        request_body = {
            "labelIds": ["INBOX"],
            "topicName": f"projects/{GOOGLE_PROJECT_ID}/topics/{GOOGLE_TOPIC_NAME}",
        }

        response = gmail.users().watch(userId="me", body=request_body).execute()

        if "historyId" in response:
            LOGGER.info(
                f"Successfully subscribed to email notifications for user ID {user.id} and email {email}"
            )
            return True
        else:
            LOGGER.error(
                f"Failed to subscribe to email notifications for user with ID: {user.id} and email {email}"
            )
            return False

    except Exception as e:
        LOGGER.error(
            f"An error occurred while subscribing to Google email notifications for user ID: {user.id}: {str(e)}"
        )
        return False


def unsubscribe_from_email_notifications(user: User, email: str) -> bool:
    """
    Unsubscribe the user from all Gmail notifications.

    Args:
        user (User): The Django User object.
        email (str): The email address of the user.

    Returns:
        bool: True if unsubscription was successful, False otherwise.
    """
    try:
        services = authenticate_service(user, email, ["gmail"])
        if services is None:
            return False

        service = services["gmail"]

        response = service.users().stop(userId="me").execute()

        if not response:
            LOGGER.info(
                f"Successfully unsubscribed user ID {user.id} ({email}) from all notifications."
            )
            return True
        else:
            LOGGER.error(
                f"Failed to unsubscribe user ID {user.id} with email: {email}. Response: {response}"
            )
            return False

    except Exception as e:
        LOGGER.error(
            f"An error occurred while unsubscribing user ID {user.id} with email: {email}: {str(e)}"
        )
        return False
