"""
Handles webhook notifications from Google API.

Endpoints:
- ✅ receive_mail_notifications: Handles requests containing email notifications.
"""

import base64
import datetime
import logging
import re
import string
import threading
import time
import random
import json
import os
from rest_framework import status
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.models import User
from collections import defaultdict
from django.db import IntegrityError
from django.shortcuts import redirect
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.auth import exceptions as auth_exceptions
from google.auth.transport.requests import Request
from google.oauth2 import credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from httpx import HTTPError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from email.utils import parsedate_to_datetime
from MailAssistant.utils.serializers import EmailDataSerializer
from django.core.mail import send_mail
from django.template.loader import render_to_string
from MailAssistant.ai_providers import claude
from MailAssistant.utils.security import subscription
from MailAssistant.utils import security
from MailAssistant.constants import (
    FREE_PLAN,
    ADMIN_EMAIL_LIST,
    DEFAULT_CATEGORY,
    EMAIL_NO_REPLY,
    ENCRYPTION_KEYS,
    GOOGLE,
    GOOGLE_CONFIG,
    GOOGLE_CREDS,
    GOOGLE_PROJECT_ID,
    GOOGLE_PROVIDER,
    GOOGLE_TOPIC_NAME,
    MAX_RETRIES,
    MEDIA_URL,
    REDIRECT_URI_LINK_EMAIL,
    REDIRECT_URI_SIGNUP,
    GOOGLE_SCOPES,
    BASE_URL_MA,
)
from MailAssistant.utils.tree_knowledge import Search
from MailAssistant.email_providers.google.authentication import authenticate_service
from MailAssistant.utils import email_processing
from MailAssistant.models import (
    Contact,
    KeyPoint,
    Preference,
    Rule,
    SocialAPI,
    Category,
    Email,
    Sender,
    CC_sender,
    BCC_sender,
    Picture,
    Attachment,
)
from base64 import urlsafe_b64encode
from bs4 import BeautifulSoup
from googleapiclient.http import BatchHttpRequest

from MailAssistant.email_providers.utils import email_to_db


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


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
        LOGGER.info(
            "Email notification received from Google API. Starting email processing."
        )
        envelope = json.loads(request.body.decode("utf-8"))
        message_data = envelope["message"]

        decoded_data = base64.b64decode(message_data["data"]).decode("utf-8")
        decoded_json: dict = json.loads(decoded_data)
        email = decoded_json.get("emailAddress")

        try:
            social_api = SocialAPI.objects.get(email=email)
            services = authenticate_service(social_api.user, email)

            def process_email():
                for i in range(MAX_RETRIES):
                    result = email_to_db(GOOGLE, social_api.user, services, social_api)

                    if result:
                        break
                    else:
                        LOGGER.critical(
                            f"[Attempt {i+1}] Failed to process email with AI for email: {email}"
                        )
                        context = {
                            "error": result,
                            "attempt_number": i + 1,
                            "email": email,
                            "email_provider": GOOGLE_PROVIDER,
                            "user": social_api.user,
                        }
                        email_html = render_to_string("ai_failed_email.html", context)
                        # send_mail(
                        #     subject="Critical Alert: Email Processing Failure",
                        #     message="",
                        #     recipient_list=ADMIN_EMAIL_LIST,
                        #     from_email=EMAIL_NO_REPLY,
                        #     html_message=email_html,
                        #     fail_silently=False,
                        # )

            threading.Thread(target=process_email).start()

        except SocialAPI.DoesNotExist:
            LOGGER.error(f"SocialAPI entry not found for the email: {email}")

        return Response({"status": "Notification received"}, status=status.HTTP_200_OK)

    except IntegrityError:
        return Response(
            {"status": "Email already exists in database"}, status=status.HTTP_200_OK
        )

    except Exception as e:
        LOGGER.error(f"Error processing the notification: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        services = authenticate_service(user, email)
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
        services = authenticate_service(user, email)
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
