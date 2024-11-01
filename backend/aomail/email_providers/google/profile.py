"""
Contains functions for managing contacts and user profile operations for Google API.

Endpoints:
- ✅  get_profile_image: Retrieves the profile image URL of the user.
"""

import datetime
import logging
import re
import time
from rest_framework import status
from django.http import HttpRequest
from django.contrib.auth.models import User
from collections import defaultdict
from google.oauth2 import credentials
from googleapiclient.discovery import build
from rest_framework.decorators import api_view
from rest_framework.response import Response
from aomail.utils.security import subscription
from aomail.constants import (
    ALLOWED_PLANS,
    GOOGLE_CONFIG,
    GOOGLE_SCOPES,
)
from aomail.email_providers.google.authentication import authenticate_service
from aomail.utils import email_processing


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
            return {"error": "No email found from Google API"}

    except Exception as e:
        LOGGER.error(f"Error retrieving user email from Google API. Error: {str(e)}.")
        return {"error": "Internal server error"}


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
    Stores all unique contacts from the latest 5,000 emails and contacts in the database using Google People API and Gmail API.

    Args:
        user (User): User object representing the owner of the email account.
        email (str): Email address of the user.
    """
    LOGGER.info(
        f"Starting to save all contacts from user ID: {user.id} with Google API"
    )
    start = time.time()

    def refresh_services():
        """Authenticate and return the necessary Google API services."""
        return authenticate_service(user, email, ["people", "gmail"])

    services = refresh_services()
    contacts_service = services["people"]
    gmail = services["gmail"]

    try:
        all_contacts = defaultdict(set)
        email_count = 0

        def make_service_call(service_function):
            nonlocal contacts_service, gmail
            for attempt in range(2):
                try:
                    return service_function()
                except Exception as e:
                    if attempt == 0:
                        LOGGER.warning(
                            f"Service authorization failed, retrying with refreshed token. Error: {str(e)}"
                        )
                        new_services = refresh_services()
                        contacts_service = new_services["people"]
                        gmail = new_services["gmail"]
                    else:
                        LOGGER.error("Request failed after token refresh.")
                        raise Exception(
                            "Token refresh failed, cannot continue request."
                        )

        # Part 1: Retrieve contacts from Google Contacts
        next_page_token = None
        while True:

            def fetch_contacts():
                """Fetch connections from Google Contacts."""
                return (
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

            response = make_service_call(fetch_contacts)
            connections = response.get("connections", [])
            next_page_token = response.get("nextPageToken")

            for contact in connections:
                names = contact.get("names", [{}])
                email_addresses = contact.get("emailAddresses", [])
                metadata = contact.get("metadata", {})
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

        # Part 2: Retrieve the latest emails from Gmail, up to 5,000 messages
        messages_endpoint = gmail.users().messages().list(userId="me", q="")
        while email_count < 5000:
            response = make_service_call(lambda: messages_endpoint.execute())
            messages = response.get("messages", [])

            for msg in messages:
                if email_count >= 5000:
                    break

                message = make_service_call(
                    lambda: gmail.users()
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
                    from_value = from_header["value"]
                    if "reply" in from_value.lower():
                        continue

                    email_match = re.search(r"[\w\.-]+@[\w\.-]+", from_value)
                    name_match = re.search(r'(?:"?([^"]*)"?\s)?', from_value)

                    email = email_match.group(0) if email_match else None
                    name = (
                        name_match.group(1)
                        if name_match and name_match.group(1)
                        else email
                    )

                    if email and (name, email, user.id, "") not in all_contacts:
                        all_contacts[(name, email, user.id, "")].add(email)

                email_count += 1

            # Pagination for Gmail messages
            if "nextPageToken" in response and email_count < 5000:
                messages_endpoint = (
                    gmail.users()
                    .messages()
                    .list(userId="me", pageToken=response["nextPageToken"])
                )
            else:
                break

        # Part 3: Save contacts to the database
        for contact_info in all_contacts.keys():
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


@api_view(["GET"])
@subscription(ALLOWED_PLANS)
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
    service = authenticate_service(user, email, ["people"])["people"]

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
                    {"profileImageUrl": photo_url}, status=status.HTTP_200_OK
                )

        return Response(
            {"error": "Profile image URL not found in response"},
            status=status.HTTP_404_NOT_FOUND,
        )

    except Exception as e:
        LOGGER.error(f"Error retrieving profile image for user ID {user.id}: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
