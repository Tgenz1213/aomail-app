"""
Contains functions for managing contacts and user profile operations for Microsoft Graph API.
"""

import base64
import datetime
import json
import logging
import threading
import time
import urllib.parse
import requests
from collections import defaultdict
from urllib.parse import urlencode
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import UploadedFile
from django.utils.timezone import make_aware
from msal import ConfidentialClientApplication
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import View
from rest_framework.response import Response
from MailAssistant.ai_providers import claude
from MailAssistant.utils.tree_knowledge import Search
from MailAssistant.utils import security
from MailAssistant.utils.security import subscription
from MailAssistant.utils.serializers import (
    EmailDataSerializer,
    EmailScheduleDataSerializer,
)
from MailAssistant.email_providers.microsoft.authentication import (
    get_headers,
    get_social_api,
    refresh_access_token,
)
from MailAssistant.utils import email_processing
from MailAssistant.constants import (
    FREE_PLAN,
    ADMIN_EMAIL_LIST,
    BASE_URL,
    DEFAULT_CATEGORY,
    EMAIL_NO_REPLY,
    ENCRYPTION_KEYS,
    GRAPH_URL,
    MAX_RETRIES,
    MICROSOFT_AUTHORITY,
    MICROSOFT_CLIENT_STATE,
    MICROSOFT_CONFIG,
    MICROSOFT_PROVIDER,
    MICROSOFT_SCOPES,
    REDIRECT_URI_LINK_EMAIL,
    REDIRECT_URI_SIGNUP,
)
from MailAssistant.models import (
    Category,
    Contact,
    Email,
    KeyPoint,
    MicrosoftListener,
    Preference,
    Rule,
    Sender,
    SocialAPI,
)


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


def verify_license(access_token: str) -> bool:
    """
    Verifies if there is a license associated with the account.

    Args:
        access_token (str): The access token used to authenticate the request.

    Returns:
        bool: True if a license is associated with the account, False otherwise.
    """
    graph_endpoint = f"{GRAPH_URL}me/licenseDetails"
    headers = get_headers(access_token)
    response = requests.get(graph_endpoint, headers=headers)

    if response.status_code == 200:
        data: dict = response.json()
        if data["value"] == []:
            return False
        else:
            return True
    return False


def get_email(access_token: str) -> dict:
    """
    Retrieves the primary email of the user from Microsoft Graph API.

    Args:
        access_token (str): Access token required for authentication.

    Returns:
        dict: {'email': <user_email>} if successful,
              {'error': <error_message>} if any error occurs.
    """
    if not access_token:
        return {"error": "Access token is missing"}

    try:
        graph_api_endpoint = f"{GRAPH_URL}me"
        headers = get_headers(access_token)
        response = requests.get(graph_api_endpoint, headers=headers)
        json_data: dict = response.json()

        if response.status_code == 200:
            email = json_data["mail"]
            return {"email": email}
        else:
            error = json_data.get("error_description", response.reason)
            return {"error": f"Failed to get email from Microsoft API: {error}"}

    except Exception as e:
        return {"error": f"Failed to get email from Microsoft API: {str(e)}"}


def get_info_contacts(access_token: str) -> list:
    """
    Fetch the name and the email of the contacts of the user.

    Args:
        access_token (str): The access token used to authenticate the request.

    Returns:
        list: A list of dictionaries containing contact names and their email addresses.
    """
    graph_endpoint = f"{GRAPH_URL}me/contacts"

    try:
        headers = get_headers(access_token)
        params = {"$top": 1000}

        response = requests.get(graph_endpoint, headers=headers, params=params)
        response.raise_for_status()
        response_data: dict = response.json()

        contacts: list[dict] = response_data.get("value", [])
        names_emails = []

        for contact in contacts:
            name = contact.get("displayName")
            email_addresses = [
                email["address"] for email in contact.get("emailAddresses", [])
            ]
            names_emails.append({"name": name, "emails": email_addresses})

        return names_emails

    except Exception as e:
        error = (
            response_data.get("error_description", response.reason)
            if response
            else str(e)
        )
        LOGGER.error(
            f"Failed to retrieve contacts. Error: {str(e)}. Response details: {error}"
        )
        return []


def get_unique_senders(access_token: str) -> dict:
    """
    Fetches unique sender information from Microsoft Graph API messages.

    Args:
        access_token (str): The access token used to authenticate the request.

    Returns:
        dict: A dictionary where keys are email addresses of senders and values are their corresponding names.
    """
    senders_info = {}

    try:
        headers = get_headers(access_token)
        limit = 50
        graph_endpoint = f"{GRAPH_URL}me/messages?$select=sender&$top={limit}"
        response = requests.get(graph_endpoint, headers=headers)
        response_data: dict = response.json()

        if response.status_code == 200:
            messages: list[dict] = response_data.get("value", [])
            for message in messages:
                sender: dict[str, dict] = message.get("sender", {})
                email_address = sender.get("emailAddress", {}).get("address", "")
                name = sender.get("emailAddress", {}).get("name", "")
                senders_info[email_address] = name
        else:
            error = response_data.get("error_description", response.reason)
            LOGGER.error(f"Failed to fetch messages: {error}")

        return senders_info

    except Exception as e:
        LOGGER.error(f"Error fetching senders: {str(e)}")
        return senders_info


@api_view(["GET"])
@subscription([FREE_PLAN])
def get_profile_image(request: HttpRequest) -> Response:
    """
    Retrieves the profile image URL of the user from Microsoft Graph API.

    Args:
        request (HttpRequest): The HTTP request object containing the user and email headers.

    Returns:
        Response: A JSON response containing the profile image URL or an error message.
    """
    user = request.user
    email = request.headers.get("email")
    social_api = get_social_api(user, email)

    if not social_api:
        return Response(
            {"error": "Social API credentials not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    access_token = refresh_access_token(social_api)

    try:
        headers = get_headers(access_token)
        graph_endpoint = f"{GRAPH_URL}me/photo/$value"
        response = requests.get(graph_endpoint, headers=headers)

        if response.status_code == 200:
            photo_data = response.content

            if photo_data:
                # Convert image to URL
                photo_data_base64 = base64.b64encode(photo_data).decode("utf-8")
                photo_url = f"data:image/png;base64,{photo_data_base64}"
                return Response(
                    {"profile_image_url": photo_url}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Profile image not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        else:
            response_data: dict = response.json()
            error = response_data.get("error_description", response.reason)
            LOGGER.error(
                f"Failed to retrieve profile image for user ID {user.id}: {error}"
            )
            return Response(
                {"error": f"Failed to retrieve profile image: {error}"},
                status=response.status_code,
            )

    except Exception as e:
        LOGGER.error(
            f"Failed to retrieve profile image for user ID {user.id}: {str(e)}"
        )
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def set_all_contacts(access_token: str, user: User):
    """
    Retrieves all unique contacts from an email account using Microsoft Graph API and stores them in the database.

    Args:
        access_token (str): Access token for authenticating with Microsoft Graph API.
        user (User): User object representing the owner of the email account.
    """
    LOGGER.info(
        f"Starting to save all contacts from user ID: {user.id} with Microsoft Graph API"
    )
    start = time.time()

    graph_api_contacts_endpoint = f"{GRAPH_URL}me/contacts"
    graph_api_messages_endpoint = f"{GRAPH_URL}me/messages?$top=500"
    headers = get_headers(access_token)

    try:
        all_contacts = defaultdict(set)

        # Part 1: Retrieve contacts from Microsoft Contacts
        response = requests.get(graph_api_contacts_endpoint, headers=headers)
        response.raise_for_status()
        response_data: dict = response.json()
        contacts: list[dict[str, dict]] = response_data.get("value", [])

        for contact in contacts:
            name = contact.get("displayName", "")
            email_address = contact.get("emailAddresses", [{}])[0].get("address", "")
            provider_id = contact.get("id", "")
            all_contacts[(user, name, email_address, provider_id)].add(email_address)

        # Part 2: Retrieve contacts from Outlook messages
        response = requests.get(graph_api_messages_endpoint, headers=headers)
        response.raise_for_status()
        data: dict = response.json()
        messages: list[dict[str, dict[str, dict]]] = data.get("value", [])

        for message in messages:
            sender: str = (
                message.get("from", {}).get("emailAddress", {}).get("address", "")
            )
            if sender:
                name = sender.split("@")[0]
                if (user, name, sender, "") in all_contacts:
                    continue
                else:
                    all_contacts[(user, name, sender, "")].add(sender)

        # Part 3: Save the contacts to the database
        for contact_info, emails in all_contacts.items():
            _, name, email_address, provider_id = contact_info
            for _ in emails:
                email_processing.save_email_sender(
                    user, name, email_address, provider_id
                )

        formatted_time = str(datetime.timedelta(seconds=time.time() - start))
        LOGGER.info(
            f"Retrieved {len(all_contacts)} unique contacts in {formatted_time} from Microsoft Graph API for user ID: {user.id}"
        )

    except Exception as e:
        LOGGER.error(
            f"Error fetching contacts from Microsoft Graph API for user ID {user.id}: {str(e)}"
        )
