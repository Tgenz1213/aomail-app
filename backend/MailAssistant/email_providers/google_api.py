"""
Handles authentication and HTTP requests for the Gmail API.
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
from django.http import HttpRequest
from django.contrib.auth.models import User
import httplib2
import requests
from collections import defaultdict
from django.core.exceptions import ObjectDoesNotExist
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
from MailAssistant.serializers import EmailDataSerializer
from django.core.mail import send_mail
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from MailAssistant.ai_providers import gpt_3_5_turbo, claude, mistral, gpt_4
from MailAssistant.utils import security
from MailAssistant.constants import (
    ADMIN_EMAIL_LIST,
    DEFAULT_CATEGORY,
    EMAIL_NO_REPLY,
    ENCRYPTION_KEYS,
    GOOGLE_CONFIG,
    GOOGLE_CREDS,
    GOOGLE_PROJECT_ID,
    GOOGLE_PROVIDER,
    GOOGLE_TOPIC_NAME,
    IMPORTANT,
    MAX_RETRIES,
    MEDIA_URL,
    REDIRECT_URI_LINK_EMAIL,
    USELESS,
    INFORMATION,
    REDIRECT_URI_SIGNUP,
    GOOGLE_SCOPES,
    MEDIA_ROOT,
    BASE_URL_MA,
)
from MailAssistant.controllers.tree_knowledge import Search
from .. import library
from ..models import (
    Contact,
    KeyPoint,
    Preference,
    Rule,
    SocialAPI,
    BulletPoint,
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


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


######################## AUTHENTIFICATION ########################
def generate_auth_url(request):
    """Generate a connection URL to obtain the authorization code"""
    flow = Flow.from_client_secrets_file(
        GOOGLE_CREDS, scopes=GOOGLE_SCOPES, redirect_uri=REDIRECT_URI_SIGNUP
    )
    authorization_url, _ = flow.authorization_url(
        access_type="offline", include_granted_scopes="true", prompt="consent"
    )

    return redirect(authorization_url)


def exchange_code_for_tokens(authorization_code):
    """Return tokens Exchanged with authorization code"""
    flow = Flow.from_client_secrets_file(
        GOOGLE_CREDS, scopes=GOOGLE_SCOPES, redirect_uri=REDIRECT_URI_SIGNUP
    )
    flow.fetch_token(code=authorization_code)

    credentials = flow.credentials

    if credentials:
        access_token = credentials.token
        refresh_token = credentials.refresh_token

        return access_token, refresh_token
    else:
        return None, None


def auth_url_link_email(request):
    """Generate a connection URL to obtain the authorization code"""
    flow = Flow.from_client_secrets_file(
        GOOGLE_CREDS, scopes=GOOGLE_SCOPES, redirect_uri=REDIRECT_URI_LINK_EMAIL
    )
    authorization_url, _ = flow.authorization_url(
        access_type="offline", include_granted_scopes="true", prompt="consent"
    )

    return redirect(authorization_url)


def link_email_tokens(authorization_code):
    """Return tokens Exchanged with authorization code"""
    flow = Flow.from_client_secrets_file(
        GOOGLE_CREDS, scopes=GOOGLE_SCOPES, redirect_uri=REDIRECT_URI_LINK_EMAIL
    )
    flow.fetch_token(code=authorization_code)

    credentials = flow.credentials

    if credentials:
        access_token = credentials.token
        refresh_token = credentials.refresh_token

        return access_token, refresh_token
    else:
        return None, None


######################## CREDENTIALS ########################
def get_credentials(user: User, email: str) -> credentials.Credentials | None:
    """
    Retrieve and return Google API credentials for the specified user and email.

    Args:
        user (User): The user object.
        email (str): The email address associated with the user's Google account.

    Returns:
        credentials.Credentials or None: The Google API credentials, or None if not found.
    """
    try:
        social_api = SocialAPI.objects.get(user=user, email=email)
        refresh_token_encrypted = social_api.refresh_token
        refresh_token = security.decrypt_text(
            ENCRYPTION_KEYS["SocialAPI"]["refresh_token"], refresh_token_encrypted
        )
        creds_data = {
            "token": social_api.access_token,
            "refresh_token": refresh_token,
            "token_uri": GOOGLE_CONFIG["token_uri"],
            "client_id": GOOGLE_CONFIG["client_id"],
            "client_secret": GOOGLE_CONFIG["client_secret"],
            "scopes": GOOGLE_SCOPES,
        }
        creds = credentials.Credentials.from_authorized_user_info(creds_data)
    except SocialAPI.DoesNotExist:
        LOGGER.error(f"No credentials for user with ID {user.id} and email: {email}")
        creds = None

    return creds


def get_social_api(user: User, email: str) -> SocialAPI | None:
    """
    Retrieve and return the SocialAPI instance for the specified user and email.

    Args:
        user (User): The user object.
        email (str): The email address associated with the user's social API.

    Returns:
        SocialAPI or None: The SocialAPI instance, or None if not found.
    """
    try:
        social_api = SocialAPI.objects.get(user=user, email=email)
        return social_api
    except SocialAPI.DoesNotExist:
        LOGGER.error(
            f"No credentials found for user with ID {user.id} and email {email}"
        )
        return None


def refresh_credentials(
    creds: credentials.Credentials,
) -> credentials.Credentials | None:
    """
    Refresh the given Google API credentials.

    Args:
        creds (credentials.Credentials): The Google API credentials to refresh.

    Returns:
        credentials.Credentials or None: The refreshed credentials, or None if refresh fails.
    """
    try:
        creds.refresh(Request())
    except auth_exceptions.RefreshError as e:
        LOGGER.error(f"Failed to refresh credentials: {str(e)}")
        creds = None
    return creds


def save_credentials(creds: credentials.Credentials, user: User, email: str):
    """
    Update the database with the new access token for the specified user and email.

    Args:
        creds (credentials.Credentials): The updated Google API credentials.
        user (User): The user object.
        email (str): The email address associated with the user's social API.
    """
    try:
        social_api = SocialAPI.objects.get(user=user, email=email)
        social_api.access_token = creds.token
        social_api.save()
    except Exception as e:
        LOGGER.error(f"Failed to save credentials: {str(e)}")


def build_services(creds: credentials.Credentials) -> dict:
    """
    Build and return a dictionary of Google API service endpoints.

    Args:
        creds (credentials.Credentials): The Google API credentials to use for building the services.

    Returns:
        dict: A dictionary of Google API service endpoints.
    """
    services = {
        "gmail": build("gmail", "v1", cache_discovery=False, credentials=creds),
        "calendar": build("calendar", "v3", cache_discovery=False, credentials=creds),
        "people": build("people", "v1", cache_discovery=False, credentials=creds),
    }
    return services


def authenticate_service(user: User, email: str) -> dict | None:
    """
    Authenticate and build Google API services for the specified user and email.

    Args:
        user (User): The user object.
        email (str): The email address associated with the user's Google account.

    Returns:
        dict or None: A dictionary of Google API service endpoints, or None if authentication fails.
    """
    creds = get_credentials(user, email)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds = refresh_credentials(creds)
        if creds:
            save_credentials(creds, user, email)
        else:
            LOGGER.error(
                f"Failed to authenticate for user with ID {user.id} and email: {email}"
            )
            return None

    services = build_services(creds)
    return services


######################## EMAIL REQUESTS ########################
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_email(request: HttpRequest):
    """Sends an email using the Gmail API."""

    try:
        user = request.user
        email = request.POST.get("email")
        service = authenticate_service(user, email)["gmail"]
        serializer = EmailDataSerializer(data=request.POST)

        if serializer.is_valid():
            data = serializer.validated_data
            subject = data["subject"]
            message = data["message"]
            to = data["to"]
            cc = data.get("cc")
            bcc = data.get("bcc")
            attachments = data.get("attachments")
            all_recipients = to

            multipart_message = MIMEMultipart()

            multipart_message["subject"] = subject
            multipart_message["from"] = "me"
            multipart_message["to"] = ", ".join(to)

            if cc:
                multipart_message["cc"] = ", ".join(cc)
                all_recipients += cc
            if bcc:
                multipart_message["bcc"] = ", ".join(bcc)
                all_recipients += bcc

            multipart_message.attach(MIMEText(message, "html"))
            if attachments:
                for uploaded_file in attachments:
                    file_content = uploaded_file.read()
                    part = MIMEApplication(file_content)
                    part.add_header(
                        "Content-Disposition", "attachment", filename=uploaded_file.name
                    )
                    multipart_message.attach(part)

            raw_message = urlsafe_b64encode(
                multipart_message.as_string().encode("UTF-8")
            ).decode()

            body = {"raw": raw_message}
            service.users().messages().send(userId="me", body=body).execute()

            threading.Thread(
                target=library.save_contacts, args=(user, email, all_recipients)
            ).start()

            return Response({"message": "Email sent successfully!"}, status=200)

        else:
            keys = serializer.errors.keys()

            if "to" in keys:
                return Response({"error": "recipient is missing"}, status=400)
            elif "subject" in keys:
                return Response({"error": "subject is missing"}, status=400)
            else:
                return Response({"error": serializer.errors}, status=400)

    except Exception as e:
        LOGGER.error(f"Failed to send email: {str(e)}")
        return Response({"error": str(e)}, status=500)


def delete_email(user, email, email_id) -> dict:
    """Moves the email to the bin of the user"""
    gmail = authenticate_service(user, email)["gmail"]

    if not gmail:
        return {"error": "No gmail service provided"}

    try:
        response = gmail.users().messages().trash(userId="me", id=email_id).execute()

        if "id" in response:
            return {"message": "Email moved to trash successfully!"}
        else:
            LOGGER.error(f"Failed to move email with ID: {email_id} to trash")
            return {"error": f"Failed to move email to trash"}
    except HTTPError as e:
        if "Requested entity was not found" in str(e):
            return {"message": "Email moved to trash successfully!"}
        else:
            LOGGER.error(f"Error when deleting email: {str(e)}")
            return {"error": str(e)}


def set_email_read(user, email, mail_id):
    """Set the status of the email to read on Gmail."""

    services = authenticate_service(user, email)
    services["gmail"].users().messages().modify(
        userId="me", id=mail_id, body={"removeLabelIds": ["UNREAD"]}
    ).execute()


def set_email_unread(user, email, mail_id):
    """Set the status of the email to unread on Gmail."""

    services = authenticate_service(user, email)
    services["gmail"].users().messages().modify(
        userId="me", id=mail_id, body={"addLabelIds": ["UNREAD"]}
    ).execute()


def get_info_contacts(services):
    """Fetch the name and the email of the contacts of the user"""
    service = services["people"]

    # Request a list of all the user's connections (contacts)
    results = (
        service.people()
        .connections()
        .list(
            resourceName="people/me",
            pageSize=1000,  # Adjust the page size as needed
            personFields="names,emailAddresses",
        )
        .execute()
    )

    contacts = results.get("connections", [])

    names_emails = []
    for contact in contacts:
        # Extract the name and email address of each contact
        name = contact.get("names", [{}])[0].get("displayName")
        email_addresses = [
            email["value"] for email in contact.get("emailAddresses", [])
        ]

        names_emails.append({"name": name, "emails": email_addresses})

    return names_emails


def get_mail_to_db(services):
    """Retrieve email information for processing email to database."""

    service = services["gmail"]

    results = (
        service.users()
        .messages()
        .list(userId="me", labelIds=["INBOX"], maxResults=1)
        .execute()
    )
    messages = results.get("messages", [])
    if not messages:
        print("No new messages.")
        return None
    message = messages[0]
    email_id = message["id"]

    msg = service.users().messages().get(userId="me", id=email_id).execute()
    email_data = msg["payload"]["headers"]

    subject = from_info = cc_info = bcc_info = sent_date = None
    for values in email_data:
        name = values["name"]
        if name == "Subject":
            subject = values["value"]
        elif name == "From":
            from_info = parse_name_and_email(values["value"])
        elif name == "Cc":
            cc_info = parse_name_and_email(values["value"])
        elif name == "Bcc":
            bcc_info = parse_name_and_email(values["value"])
        elif name == "Date":
            sent_date = parsedate_to_datetime(values["value"])

    # TODO: delete => and in models too
    web_link = f"https://mail.google.com/mail/u/0/#inbox/{email_id}"

    has_attachments = False
    is_reply = "in-reply-to" in {
        header["name"].lower() for header in msg["payload"]["headers"]
    }
    email_html = ""
    email_txt_html = ""
    email_detect_html = False
    image_files = []
    attachments = []  # List to store attachment metadata

    def process_part(part):
        nonlocal email_html, email_txt_html, email_detect_html, has_attachments, image_files, attachments

        if part["mimeType"] == "text/plain":
            if "data" in part["body"]:
                data = part["body"]["data"]
                decoded_data = base64.urlsafe_b64decode(data.encode("UTF-8")).decode(
                    "utf-8"
                )
                email_txt_html += f"<pre>{decoded_data}</pre>"
        elif part["mimeType"] == "text/html":
            if "data" in part["body"]:
                email_detect_html = True
                data = part["body"]["data"]
                decoded_data = base64.urlsafe_b64decode(data.encode("UTF-8")).decode(
                    "utf-8"
                )
                email_html += decoded_data

                # Find and replace base64 encoded images in the HTML
                img_tags = re.findall(
                    r'<img[^>]+src="data:image/([^;]+);base64,([^"]+)"', decoded_data
                )
                for img_type, img_data in img_tags:
                    timestamp = int(time.time())
                    random_str = "".join(
                        random.choices(string.ascii_letters + string.digits, k=8)
                    )
                    image_filename = f"image_{timestamp}_{random_str}.{img_type}"
                    image_files.append(image_filename)
                    email_html = email_html.replace(
                        f"data:image/{img_type};base64,{img_data}",
                        f"{MEDIA_URL}pictures/{image_filename}",
                    )
        elif part["mimeType"].startswith("image/"):
            timestamp = int(time.time())
            random_str = "".join(
                random.choices(string.ascii_letters + string.digits, k=8)
            )
            image_filename = part.get("filename", f"image_{timestamp}_{random_str}.jpg")
            image_files.append(image_filename)
            email_html += f'<img src="{BASE_URL_MA}pictures/{image_filename}" alt="Embedded Image" />'
            email_txt_html += f'<img src="{BASE_URL_MA}pictures/{image_filename}" alt="Embedded Image" />'
        elif part["mimeType"].startswith("multipart/"):
            if "parts" in part:
                for subpart in part["parts"]:
                    process_part(subpart)
        elif "filename" in part:
            has_attachments = True
            attachment_id = part["body"]["attachmentId"]
            # Add metadata to attachments list
            attachments.append(
                {"attachmentId": attachment_id, "attachmentName": part["filename"]}
            )

    if "parts" in msg["payload"]:
        for part in msg["payload"]["parts"]:
            process_part(part)
    else:
        process_part(msg["payload"])

    if email_detect_html is False:
        email_html = email_txt_html

    # Replace CID references in HTML with local paths
    soup = BeautifulSoup(email_html, "html.parser")
    for img in soup.find_all("img"):
        cid_ref = img["src"].lstrip("cid:")
        for image_file in image_files:
            if cid_ref in image_file:
                img["src"] = f"{BASE_URL_MA}pictures/{os.path.basename(image_file)}"

    cleaned_html = library.html_clear(email_html)
    preprocessed_data = library.preprocess_email(cleaned_html)
    safe_html = soup.prettify()

    return (
        subject,
        from_info,
        preprocessed_data,
        safe_html,
        email_id,
        sent_date,
        web_link,
        has_attachments,
        is_reply,
        cc_info,
        bcc_info,
        image_files,
        attachments,
    )


def get_mail_id(services, int_mail: int) -> str:
    """
    Retrieve the email ID of a specific email from the user's Gmail inbox.

    Args:
        services (dict): A dictionary containing service objects for various APIs.
                         It should include a "gmail" service object.
        int_mail (int): The index of the email in the inbox to retrieve the ID for.

    Returns:
        str: The ID of the specified email if found, otherwise None.
    """
    service = services["gmail"]

    results = service.users().messages().list(userId="me", labelIds=["INBOX"]).execute()
    messages = results.get("messages", [])
    if not messages:
        LOGGER.info("No new messages.")
        return None
    message = messages[int_mail]
    email_id = message["id"]

    return email_id


# TO DELETE IN THE FUTURE ?
def get_mail(services, int_mail=None, id_mail=None):
    """Retrieve email information including subject, sender, content, CC, BCC, and ID"""
    service = services["gmail"]
    plaintext_var = [0]
    plaintext_var[0] = 0

    if int_mail is not None:
        results = (
            service.users().messages().list(userId="me", labelIds=["INBOX"]).execute()
        )
        messages = results.get("messages", [])
        if not messages:
            LOGGER.info("No new messages.")
            return None
        message = messages[int_mail]
        email_id = message["id"]
    elif id_mail is not None:
        email_id = id_mail
    else:
        LOGGER.info("Either int_mail or id_mail must be provided")
        return None

    msg = service.users().messages().get(userId="me", id=email_id).execute()

    subject = from_info = decoded_data = None
    cc_info = bcc_info = []
    email_data = msg["payload"]["headers"]
    web_link = f"https://mail.google.com/mail/u/0/#inbox/{email_id}"

    for values in email_data:
        name = values["name"]
        if name == "Subject":
            subject = values["value"]
        elif name == "From":
            from_info = parse_name_and_email(values["value"])
        elif name == "Cc":
            cc_info = parse_name_and_email(values["value"])
        elif name == "Bcc":
            bcc_info = parse_name_and_email(values["value"])
        elif name == "Date":
            sent_date = parsedate_to_datetime(values["value"])

    if "parts" in msg["payload"]:
        for part in msg["payload"]["parts"]:
            decoded_data_temp = library.process_part(part, plaintext_var)

            print(
                "______________________DATA decoded_data_temp (PARTS) looks like that ______________________________"
            )
            print(decoded_data_temp)
            print(
                "___________________________________________________________________________________"
            )
            if decoded_data_temp:
                decoded_data = library.concat_text(decoded_data, decoded_data_temp)
    elif "body" in msg["payload"]:
        data = msg["payload"]["body"]["data"]

        print(
            "______________________DATA RAW BODY looks like that ______________________________"
        )
        print(data)
        print(
            "___________________________________________________________________________________"
        )

        data = data.replace("-", "+").replace("_", "/")
        decoded_data_temp = base64.b64decode(data).decode("utf-8")
        decoded_data = library.html_clear(decoded_data_temp)

    return (
        subject,
        from_info,
        decoded_data,
        cc_info,
        bcc_info,
        email_id,
        sent_date,
        web_link,
    )


def search_emails_ai(
    services: dict[str, build],
    max_results: int = 100,
    filenames: list = None,
    from_addresses: list = None,
    to_addresses: list = None,
    subject: str = None,
    body: str = None,
    keywords: list = None,
    date_from: str = None,
    search_in: dict = None,
):
    """Searches for emails matching the query."""

    query_parts = []

    if from_addresses:
        from_query = " OR ".join([f"from:{address}" for address in from_addresses])
        query_parts.append(f"({from_query})")
    if to_addresses:
        to_query = " OR ".join([f"to:{address}" for address in to_addresses])
        query_parts.append(f"({to_query})")
    if subject:
        query_parts.append(f"(subject:{subject})")
    if body:
        query_parts.append(f"(body:{body})")
    if search_in:
        search_in_query = " OR ".join(
            [f"in:{folder}" for folder in search_in if search_in[folder]]
        )
        query_parts.append(f"({search_in_query})")

    query = " OR ".join(query_parts)

    query_parts = []
    if filenames:
        file_query = " OR ".join([f"filename:{ext}" for ext in filenames])
        query_parts.append(f"({file_query})")
    if date_from:
        query_parts.append(f"(after:{date_from})")
    if keywords:
        keyword_query = " OR ".join([keyword for keyword in keywords])
        query_parts.append(f'("{keyword_query}")')

    if query_parts:
        query += " AND " + " AND ".join(query_parts)

    # print("\n\nDEBUG query: ", query, "\n\n")

    try:
        service = services["gmail"]
        results = (
            service.users()
            .messages()
            .list(userId="me", q=query, maxResults=max_results)
            .execute()
        )
        messages = results.get("messages", [])

        return [message["id"] for message in messages]

    except Exception as e:
        LOGGER.error(f"Failed to search_emails_ai: {str(e)}")
        return []


def search_emails_manually(
    services: dict,
    search_query: str,
    max_results: int,
    file_extensions: list,
    advanced: bool = False,
    search_in: dict = None,
    from_addresses: list = None,
    to_addresses: list = None,
    subject: str = None,
    body: str = None,
    date_from: str = None,
) -> list:
    """Searches for emails matching the query."""

    def search(query: str):
        try:
            results: dict = (
                service.users()
                .messages()
                .list(userId="me", q=query, maxResults=max_results)
                .execute()
            )

            if results.get("resultSizeEstimate") == 0:
                return []
            return results.get("messages", [])
        except Exception as e:
            LOGGER.error(f"Failed to search emails: {str(e)}")
            return []

    try:
        service = services["gmail"]

        if advanced:
            query_parts = []
            if from_addresses:
                from_query = " OR ".join(
                    [f"from:{address}" for address in from_addresses]
                )
                query_parts.append(f"({from_query})")
            if to_addresses:
                to_query = " OR ".join([f"to:{address}" for address in to_addresses])
                query_parts.append(f"({to_query})")
            if subject:
                query_parts.append(f"(subject:{subject})")
            if body:
                query_parts.append(f"(body:{body})")
            if date_from:
                query_parts.append(f"(after:{date_from})")
            if search_in:
                search_in_query = " OR ".join(
                    [f"in:{folder}" for folder in search_in if search_in[folder]]
                )
                query_parts.append(f"({search_in_query})")
            if file_extensions:
                file_query = " OR ".join([f"filename:{ext}" for ext in file_extensions])
                query_parts.append(f" AND ({file_query})")

            if query_parts:
                query = " OR ".join(query_parts)
                messages = search(query)

        else:
            query_parts = [
                f"(from:{search_query})",
                f"(to:{search_query})",
                f"(subject:{search_query})",
                f"(body:{search_query})",
                f"(filename:{search_query})",
            ]
            query = " OR ".join(query_parts)
            messages = search(query)

        return [message["id"] for message in messages]

    except Exception as e:
        LOGGER.error(f"Failed to search emails: {str(e)}")
        return []


# ----------------------- EMAIL ATTACHMENT -----------------------#
''' TO DELETE : def get_attachment_metadata(user: User, email: str, email_id: int) -> dict:
    """
    Retrieve metadata of all attachments from a specific email using the Gmail API.
    """
    try:
        services = authenticate_service(user, email)

        message = services['gmail'].users().messages().get(userId='me', id=email_id).execute()
        
        attachments_metadata = []

        if 'payload' in message:
            parts = message['payload'].get('parts', [])
            for part in parts:
                if 'filename' in part and part['filename']:
                    attachment_id = part['body']['attachmentId']
                    attachments_metadata.append(
                        {"attachmentName": part['filename'], "attachmentId": attachment_id}
                    )

        return attachments_metadata

    except Exception as e:
        LOGGER.error(f"Failed to get attachments metadata for email ID {email_id}: {str(e)}")
        return []'''


def get_attachment_data(
    user: User, email: str, email_id: str, attachment_id: str
) -> dict:
    try:
        services = authenticate_service(user, email)
        if not services or "gmail" not in services:
            LOGGER.error(
                f"Failed to authenticate Gmail service for user with ID {user.id} and email: {email}"
            )
            LOGGER.error(f"SERVICES : ", services)
            return {}

        gmail_service = services["gmail"]
        message = (
            gmail_service.users().messages().get(userId="me", id=email_id).execute()
        )

        if "payload" in message:
            parts = message["payload"].get("parts", [])
            for part in parts:
                if "body" in part and part["body"].get("attachmentId") == attachment_id:
                    attachment = (
                        gmail_service.users()
                        .messages()
                        .attachments()
                        .get(userId="me", messageId=email_id, id=attachment_id)
                        .execute()
                    )

                    data = attachment["data"]
                    attachment_data = base64.urlsafe_b64decode(data.encode("UTF-8"))
                    return {"attachmentName": part["filename"], "data": attachment_data}

        return {}

    except Exception as e:
        LOGGER.error(
            f"Failed to get attachment data for email ID {email_id} and attachment ID {attachment_id}: {str(e)}"
        )
        return {}


# ----------------------- READ EMAIL -----------------------#
def find_user_in_emails(services, search_query):
    """Search for user in emails based on a query"""
    emails = search_emails(services, search_query)

    if not emails:
        return "No matching emails found."

    return emails


def parse_name_and_email(header_value):
    if not header_value:
        return None, None

    # Regex to extract name and email
    match = re.match(r"(.*)\s*<(.+)>", header_value)
    if match:
        name, email = match.groups()
        return name.strip(), email.strip()
    else:
        # If the format doesn't match, assume the entire value is the email
        return None, header_value.strip()


# V2 : better to check the mail structure (comparing with the input)
def search_emails(services, search_query, max_results=2):
    """Searches for emails addresses in the user's mailbox based on the provided search query in both the subject and body."""
    service = services["gmail"]

    # Fetch the list of emails based on the query
    try:
        results = (
            service.users()
            .messages()
            .list(userId="me", q=search_query, maxResults=max_results)
            .execute()
        )
        messages = results.get("messages", [])
        found_emails = {}

        for message in messages:
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
            headers = msg.get("payload", {}).get("headers", [])
            sender = next(
                (header["value"] for header in headers if header["name"] == "From"),
                None,
            )

            if sender:
                email = sender.split("<")[-1].split(">")[0].strip().lower()
                name = sender.split("<")[0].strip().lower() if "<" in sender else email

                # Additional filtering: Check if the sender email/name matches the search query
                if search_query.lower() in email or search_query.lower() in name:
                    if email and not library.is_no_reply_email(email):
                        found_emails[email] = name

        return found_emails

    except Exception as e:
        LOGGER.error(f"Failed to search emails: {str(e)}")
        return {}


######################## PROFILE REQUESTS ########################
def set_all_contacts(user, email):
    """Stores all unique contacts of an email account in DB"""
    start = time.time()

    services = authenticate_service(user, email)
    contacts_service = services["people"]
    gmail = services["gmail"]

    try:
        all_contacts = defaultdict(set)

        # Part 1: Retrieve from Google Contacts
        next_page_token = None
        while True:
            response = (
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

        # Part 2: Retrieving from Gmail
        response = gmail.users().messages().list(userId="me", q="").execute()
        messages = response.get("messages", [])

        for msg in messages[:500]:  # Limit to the first 500 messages
            message = (
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
                from_value = from_header["value"]
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
                library.save_email_sender(user, name, email, contact_id)

        formatted_time = str(datetime.timedelta(seconds=time.time() - start))
        LOGGER.info(
            f"Retrieved {len(all_contacts)} unique contacts in {formatted_time}"
        )

    except Exception as e:
        LOGGER.error(f"Error fetching contacts: {str(e)}")


def get_unique_senders(services) -> dict:
    """Fetches unique sender information from Gmail messages"""
    service = services["gmail"]
    limit = 50
    results = (
        service.users()
        .messages()
        .list(userId="me", labelIds=["INBOX"], maxResults=limit)
        .execute()
    )
    messages = results.get("messages", [])

    senders_info = {}

    if not messages:
        LOGGER.info("No messages found")
    else:
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
                sender_header = next(
                    header["value"] for header in headers if header["name"] == "From"
                )

                # Extracting the email address and name
                sender_parts = sender_header.split("<")
                sender_name = sender_parts[0].strip().strip('"')
                sender_email = (
                    sender_parts[-1].split(">")[0].strip()
                    if len(sender_parts) > 1
                    else sender_name
                )

                # Store the sender's name with the email address as the key
                senders_info[sender_email] = sender_name
            except Exception as e:
                LOGGER.error(
                    f"Error processing message with ID {message['id']}: {str(e)}"
                )

    return senders_info


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile_image(request: HttpRequest):
    """Returns the profile image of the user"""
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
                return Response({"profile_image_url": photo_url})

        return Response(
            {"profile_image_url": "Profile image URL not found in response"}, status=404
        )

    except Exception as e:
        return Response(
            {"error": f"Error retrieving profile image: {str(e)}"}, status=505
        )


def get_email(access_token: str, refresh_token: str) -> str | None:
    """
    Returns the primary email of the user.

    Args:
        access_token (str): The access token for Google API authentication.
        refresh_token (str): The refresh token for Google API authentication.

    Returns:
        str or None: The primary email address of the user, or None if an error occurs.
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
        service = build('people', 'v1', credentials=creds)
        user_info: dict[str, list[dict]] = (
            service.people()
            .get(resourceName="people/me", personFields="emailAddresses")
            .execute()
        )
        email = user_info.get("emailAddresses", [{}])[0].get("value", "")
        return email

    except Exception as e:
        LOGGER.error(f"Could not get email: {str(e)}")
        return None


######################## GOOGLE LISTENER ########################
def subscribe_to_email_notifications(user, email) -> bool:
    """Subscribe the user to email notifications for a specific topic in Google."""

    try:
        LOGGER.info(
            f"Initiating the subscription to Google listener for: {user} with email: {email}"
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
                f"Successfully subscribed to email notifications for user {user.username} and email {email}"
            )
            return True
        else:
            LOGGER.error(
                f"Failed to subscribe to email notifications for user with ID: {user.id} and email {email}"
            )
            return False

    except Exception as e:
        LOGGER.error(
            f"An error occurred while subscribing to email notifications: {str(e)}"
        )
        return False


def unsubscribe_from_email_notifications(user, email) -> bool:
    """Unsubscribe the user from all Gmail notifications."""

    try:
        services = authenticate_service(user, email)
        if services is None:
            LOGGER.error(
                f"Failed to get service to unsubscribe {user} with email: {email}"
            )
            return False

        service = services["gmail"]

        response = service.users().stop(userId=email).execute()

        if not response:
            LOGGER.info(
                f"Successfully unsubscribed {user} ({email}) from all notifications."
            )
            return True
        else:
            LOGGER.error(
                f"Failed to unsubscribe {user} ({email}). Response: {response}"
            )
            return False

    except Exception as e:
        LOGGER.error(f"An error occurred while unsubscribing: {str(e)}")
        return False


@api_view(["POST"])
@permission_classes([AllowAny])
def receive_mail_notifications(request):
    """Process email notifications from Google listener"""

    try:
        print("!!! [GOOGLE] EMAIL RECEIVED !!!")
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
                    result = email_to_db(social_api.user, services, social_api)

                    if result:
                        break
                    else:
                        LOGGER.critical(
                            f"[Attempt n°{i+1}] Failed to process email with AI for email: {email}"
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

        return Response(status=200)

    except IntegrityError:
        LOGGER.error(f"Email already exists in database")
        return Response(status=200)

    except Exception as e:
        LOGGER.error(f"Error processing the notification: {str(e)}")
        return Response({"error": str(e)}, status=500)


def email_to_db(user, services, social_api: SocialAPI):
    """Saves email notifications from Google listener to database"""

    (
        subject,
        from_name,
        decoded_data,
        safe_html,
        email_id,
        sent_date,
        web_link,
        has_attachments,
        is_reply,
        cc_info,
        bcc_info,
        image_files,
        attachments,
    ) = get_mail_to_db(services)

    if Email.objects.filter(provider_id=email_id).exists():
        return True

    user_description = (
        social_api.user_description if social_api.user_description != None else ""
    )
    language = Preference.objects.get(user=user).language

    if not Email.objects.filter(provider_id=email_id).exists():
        sender = Sender.objects.filter(email=from_name[1]).first()

        if not decoded_data:
            return "No decoded data"

        category_dict = library.get_db_categories(user)
        category = Category.objects.get(name=DEFAULT_CATEGORY, user=user)
        rules = Rule.objects.filter(sender=sender)
        rule_category = None

        if rules.exists():
            print("---------- FOUND SOME RULES FOR THIS EMAIL ---------")
            for rule in rules:
                if rule.block:
                    print("---------- THIS EMAIL ADDRESS HAS BEEN BLOCKED ---------")
                    return True

                if rule.category:
                    print("---------- SETTING RULE CATEGORY... ---------")
                    category = rule.category
                    rule_category = True

        if is_reply:
            email_content = library.preprocess_email(decoded_data)

            # summarize conversation with Search
            user_id = user.id
            search = Search(user_id)
            email_id = get_mail_id(services, 0)
            conversation_summary = search.summarize_conversation(
                subject, email_content, user_description, language
            )
        else:
            # summarize single email with Search
            email_content = library.preprocess_email(decoded_data)

            user_id = user.id
            search = Search(user_id)
            email_id = get_mail_id(services, 0)
            email_summary = search.summarize_email(
                subject, email_content, user_description, language
            )

        (
            topic,
            importance_dict,
            answer,
            summary_list,
            sentence,
            relevance,
        ) = claude.categorize_and_summarize_email(
            subject, decoded_data, category_dict, user_description
        )

        if (
            importance_dict["UrgentWorkInformation"] >= 50
        ):  # MAYBE TO UPDATE TO >50 =>  To test
            importance = IMPORTANT
        elif (
            importance_dict["Promotional"] <= 50
            and importance_dict["RoutineWorkUpdates"] > 10
        ):  # To avoid some error that might put a None promotional email in Useless => Ask Theo before Delete
            importance = INFORMATION
        else:
            max_percentage = 0
            for key, value in importance_dict.items():
                if value > max_percentage:
                    importance = key
                    if importance == "Promotional" or importance == "News":
                        importance = USELESS
                    elif (
                        importance == "RoutineWorkUpdates"
                        or importance == "InternalCommunications"
                    ):
                        importance = INFORMATION
                    elif importance == "UrgentWorkInformation":
                        importance = IMPORTANT
                    max_percentage = importance_dict[key]
            if max_percentage == 0:
                importance = INFORMATION

        if not rule_category:
            if topic in category_dict:
                category = Category.objects.get(name=topic, user=user)

        if not sender:
            sender_name, sender_email = from_name[0], from_name[1]
            if not sender_name:
                sender_name = sender_email

            sender = Sender.objects.filter(email=sender_email).first()
            if not sender:
                sender = Sender.objects.create(email=sender_email, name=sender_name)

        try:
            email_entry = Email.objects.create(
                social_api=social_api,
                provider_id=email_id,
                email_provider=GOOGLE_PROVIDER,
                email_short_summary=sentence,
                content=decoded_data,
                html_content=safe_html,
                subject=subject,
                priority=importance,
                read=False,
                answer_later=False,
                sender=sender,
                category=category,
                user=user,
                date=sent_date,
                web_link=web_link,
                has_attachments=has_attachments,
                answer=answer,
                relevance=relevance,
            )

            if is_reply:
                conversation_summary_category = conversation_summary["category"]
                conversation_summary_organization = conversation_summary["organization"]
                conversation_summary_topic = conversation_summary["topic"]
                keypoints: dict = conversation_summary["keypoints"]

                for index, keypoints_list in keypoints.items():
                    for keypoint in keypoints_list:
                        KeyPoint.objects.create(
                            is_reply=True,
                            position=index,
                            category=conversation_summary_category,
                            organization=conversation_summary_organization,
                            topic=conversation_summary_topic,
                            content=keypoint,
                            email=email_entry,
                        )
            else:
                email_summary_category = email_summary["category"]
                email_summary_organization = email_summary["organization"]
                email_summary_topic = email_summary["topic"]

                for keypoint in email_summary["keypoints"]:
                    KeyPoint.objects.create(
                        is_reply=False,
                        category=email_summary_category,
                        organization=email_summary_organization,
                        topic=email_summary_topic,
                        content=keypoint,
                        email=email_entry,
                    )

            contact_name, contact_email = from_name[0], from_name[1]
            Contact.objects.get_or_create(
                user=user, email=contact_email, username=contact_name
            )

            if cc_info:
                for email, name in cc_info:
                    CC_sender.objects.create(
                        mail_id=email_entry, email=email, name=name
                    )

            if bcc_info:
                for email, name in bcc_info:
                    BCC_sender.objects.create(
                        mail_id=email_entry, email=email, name=name
                    )

            if image_files:
                for image_path in image_files:
                    Picture.objects.create(mail_id=email_entry, picture=image_path)

            if summary_list:
                for point in summary_list:
                    BulletPoint.objects.create(content=point, email=email_entry)

            if attachments:
                for attachment in attachments:
                    Attachment.objects.create(
                        mail_id=email_entry,
                        name=attachment["attachmentName"],
                        id_api=attachment["attachmentId"],
                    )
            return True

        except Exception as e:
            LOGGER.error(
                f"An error occurred when trying to create an email with ID {email_id}: {str(e)}"
            )
            return str(e)
