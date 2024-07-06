"""
Contains functions for managing contacts and user profile operations for Google API.
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


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


def get_email(access_token: str, refresh_token: str) -> dict:
    """
    Returns the primary email of the user from Google People API.

    Args:
        access_token (str): The access token for Google API authentication.
        refresh_token (str): The refresh token for Google API authentication.

    Returns:
        dict: {'email': <user_email>} if successful,
              {'error': <error_message>} if any error occurs.
    """
    creds_data = {
        "token": access_token,
        "refresh_token": refresh_token,
        "token_uri": GOOGLE_CONFIG["token_uri"],
        "client_id": GOOGLE_CONFIG["client_id"],
        "client_secret": GOOGLE_CONFIG["client_secret"],
        "scopes": GOOGLE_SCOPES,
    }
    creds = credentials.Credentials.from_authorized_user_info(creds_data)

    try:
        service = build("people", "v1", credentials=creds)
        user_info: dict[str, list[dict]] = (
            service.people()
            .get(resourceName="people/me", personFields="emailAddresses")
            .execute()
        )
        email = user_info.get("emailAddresses", [{}])[0].get("value", "")
        if email:
            return {"email": email}
        else:
            return {"error": "No email found from Microsoft API"}

    except Exception as e:
        return {"error": f"Failed to get email from Microsoft API: {str(e)}"}


def get_info_contacts(services: dict) -> list[dict]:
    """
    Fetches the names and email addresses of the contacts of the user.

    Args:
        services (dict): A dictionary containing various authenticated services,
                         including the 'people' service for fetching contacts.

    Returns:
        list: A list of dictionaries, where each dictionary contains 'name' and 'emails'
              keys. 'name' represents the contact's display name, and 'emails' is a list
              of email addresses associated with the contact.
    """
    service = services["people"]

    results = (
        service.people()
        .connections()
        .list(
            resourceName="people/me",
            pageSize=1000,
            personFields="names,emailAddresses",
        )
        .execute()
    )

    contacts = results.get("connections", [])

    names_emails = []
    for contact in contacts:
        name = contact.get("names", [{}])[0].get("displayName")
        email_addresses = [
            email["value"] for email in contact.get("emailAddresses", [])
        ]
        names_emails.append({"name": name, "emails": email_addresses})

    return names_emails


def set_all_contacts(user: User, email: str):
    """
    Stores all unique contacts of an email account in the database using Google People API and Gmail API.

    Args:
        user (User): User object representing the owner of the email account.
        email (str): Email address of the user.
    """
    LOGGER.info(
        f"Starting to save all contacts from from user ID: {user.id} with Google API"
    )
    start = time.time()

    services = authenticate_service(user, email)
    contacts_service = services["people"]
    gmail = services["gmail"]

    try:
        all_contacts = defaultdict(set)

        # Part 1: Retrieve from Google Contacts
        next_page_token = None
        while True:
            response: dict = (
                contacts_service.people()
                .connections()
                .list(
                    resourceName="people/me",
                    personFields="names,emailAddresses,metadata",
                    pageSize=1000,
                    pageToken=next_page_token,
                )
                .execute()
            )

            connections: list[dict] = response.get("connections", [])
            next_page_token = response.get("nextPageToken")

            for contact in connections:
                names: list[dict] = contact.get("names", [{}])
                email_addresses: list[dict] = contact.get("emailAddresses", [])
                metadata: dict[str, dict] = contact.get("metadata", {})
                contact_id = metadata.get("sources", [{}])[0].get("id", "")
                name = names[0].get("displayName", "") if names else ""

                for email_info in email_addresses:
                    email_address = email_info.get("value", "")
                    if email_address:
                        all_contacts[(name, email_address, user.id, contact_id)].add(
                            email_address
                        )

            if not next_page_token:
                break

        # Part 2: Retrieving from Gmail
        response = gmail.users().messages().list(userId="me", q="").execute()
        messages = response.get("messages", [])

        for msg in messages[:500]:  # Limit to the first 500 messages
            message: dict[str, dict] = (
                gmail.users()
                .messages()
                .get(
                    userId="me",
                    id=msg["id"],
                    format="metadata",
                    metadataHeaders=["From"],
                )
                .execute()
            )
            headers = message.get("payload", {}).get("headers", [])
            from_header = next(
                (item for item in headers if item["name"] == "From"), None
            )
            if from_header:
                from_value: str = from_header["value"]
                if "reply" in from_value.lower():
                    continue

                email_match = re.search(r"[\w\.-]+@[\w\.-]+", from_value)
                name_match = re.search(r'(?:"?([^"]*)"?\s)?', from_value)

                email = email_match.group(0) if email_match else None
                name = (
                    name_match.group(1) if name_match and name_match.group(1) else email
                )

                if not email:
                    continue

                if (name, email, user.id, "") in all_contacts:
                    continue
                else:
                    all_contacts[(name, email, user.id, "")].add(email)

        # Part 3: Add the contacts to the database
        for contact_info, _ in all_contacts.items():
            name, email, _, contact_id = contact_info
            if name and email:
                email_processing.save_email_sender(user, name, email, contact_id)

        formatted_time = str(datetime.timedelta(seconds=time.time() - start))
        LOGGER.info(
            f"Retrieved {len(all_contacts)} unique contacts in {formatted_time} from Google API for user ID: {user.id}"
        )

    except Exception as e:
        LOGGER.error(
            f"Error fetching contacts from Google API for user ID {user.id}: {str(e)}"
        )


def get_unique_senders(services: dict) -> dict:
    """
    Fetches unique sender information from Gmail messages using Gmail API.

    Args:
        services (dict): A dictionary containing the necessary services, with 'gmail' key for Gmail service.

    Returns:
        dict: A dictionary where keys are email addresses of senders and values are their corresponding names.
    """
    service = services["gmail"]
    limit = 50
    results: dict = (
        service.users()
        .messages()
        .list(userId="me", labelIds=["INBOX"], maxResults=limit)
        .execute()
    )
    messages = results.get("messages", [])

    senders_info = {}

    if messages:
        for message in messages:
            try:
                msg = (
                    service.users()
                    .messages()
                    .get(
                        userId="me",
                        id=message["id"],
                        format="metadata",
                        metadataHeaders=["From"],
                    )
                    .execute()
                )
                headers = msg["payload"]["headers"]
                sender_header: str = next(
                    header["value"] for header in headers if header["name"] == "From"
                )

                sender_parts = sender_header.split("<")
                sender_name = sender_parts[0].strip().strip('"')
                sender_email = (
                    sender_parts[-1].split(">")[0].strip()
                    if len(sender_parts) > 1
                    else sender_name
                )

                senders_info[sender_email] = sender_name
            except Exception as e:
                LOGGER.error(
                    f"Error fetching or processing sender: {str(e)}. Message ID: {message['id']}"
                )
                return senders_info

    return senders_info


@api_view(["GET"])
@subscription([FREE_PLAN])
def get_profile_image(request: HttpRequest) -> Response:
    """
    Retrieves the profile image URL of the user from Google People API.

    Args:
        request (HttpRequest): The HTTP request object containing the user and email headers.

    Returns:
        Response: A JSON response containing the profile image URL or an error message.
    """
    user = request.user
    email = request.headers.get("email")
    service = authenticate_service(user, email)["people"]

    try:
        profile = (
            service.people()
            .get(resourceName="people/me", personFields="photos")
            .execute()
        )

        if "photos" in profile:
            photos = profile["photos"]
            if photos:
                photo_url = photos[0]["url"]
                return Response(
                    {"profile_image_url": photo_url}, status=status.HTTP_200_OK
                )

        return Response(
            {"error": "Profile image URL not found in response"},
            status=status.HTTP_404_NOT_FOUND,
        )

    except Exception as e:
        LOGGER.error(f"Error retrieving profile image for user ID {user.id}: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
