"""
Handles authentication and HTTP requests for the Gmail API.

TODO:
- add @subscription decorator
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
from MailAssistant.utils.tree_knowledge import Search
from ..utils import email_processing 
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
def generate_auth_url(request: HttpRequest) -> HttpResponseRedirect:
    """
    Generate a connection URL to obtain the authorization code.

    Args:
        request (HttpRequest): HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the Google authorization URL.
    """
    try:
        ip = security.get_ip_with_port(request)
        LOGGER.info(f"Initiating Google OAuth flow from IP: {ip}")

        flow = Flow.from_client_secrets_file(
            GOOGLE_CREDS, scopes=GOOGLE_SCOPES, redirect_uri=REDIRECT_URI_SIGNUP
        )
        authorization_url, _ = flow.authorization_url(
            access_type="offline", include_granted_scopes="true", prompt="consent"
        )
        LOGGER.info(
            f"Successfully redirected to Google authorization URL from IP: {ip}"
        )
        return redirect(authorization_url)

    except Exception as e:
        LOGGER.error(f"Error generating Google OAuth URL: {str(e)}")


def exchange_code_for_tokens(
    authorization_code: str,
) -> tuple[str, str] | tuple[None, None]:
    """
    Exchange authorization code for access and refresh tokens.

    Args:
        authorization_code (str): Authorization code obtained from the OAuth2 flow.

    Returns:
        tuple: A tuple containing the access token and refresh token if successful,
               otherwise (None, None) if credentials are not obtained.
    """
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


def auth_url_link_email(request: HttpRequest) -> HttpResponseRedirect:
    """
    Generates a connection URL to obtain the authorization code for linking an email account.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects the user to the generated authorization URL.
    """
    try:
        ip = security.get_ip_with_port(request)
        LOGGER.info(f"Initiating Google OAuth flow from IP: {ip}")

        flow = Flow.from_client_secrets_file(
            GOOGLE_CREDS, scopes=GOOGLE_SCOPES, redirect_uri=REDIRECT_URI_LINK_EMAIL
        )
        authorization_url, _ = flow.authorization_url(
            access_type="offline", include_granted_scopes="true", prompt="consent"
        )
        LOGGER.info(
            f"Successfully redirected to Google authorization URL from IP: {ip}"
        )
        return redirect(authorization_url)

    except Exception as e:
        LOGGER.error(f"Error generating Google OAuth URL: {str(e)}")


def link_email_tokens(authorization_code: str) -> tuple[str, str] | tuple[None, None]:
    """
    Exchange authorization code for access and refresh tokens.

    Args:
        authorization_code (str): Authorization code obtained from the OAuth2 flow.

    Returns:
        tuple: A tuple containing the access token and refresh token if successful,
               otherwise (None, None) if credentials are not obtained.
    """
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
def send_email(request: HttpRequest) -> Response:
    """
    Sends an email using the Gmail API.

    Args:
        request (HttpRequest): HTTP request object containing POST data with email details.

    Returns:
        Response: Response indicating success or error.
    """
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
                target=email_processing.save_contacts, args=(user, email, all_recipients)
            ).start()

            return Response(
                {"message": "Email sent successfully!"}, status=status.HTTP_200_OK
            )

        else:
            keys = serializer.errors.keys()

            if "to" in keys:
                return Response(
                    {"error": "recipient is missing"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif "subject" in keys:
                return Response(
                    {"error": "subject is missing"}, status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                )

    except Exception as e:
        LOGGER.error(f"Failed to send email: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def delete_email(user: User, email: str, email_id: str) -> dict:
    """
    Moves the email with the specified ID to the bin of the user's Gmail account.

    Args:
        user (User): The authenticated user object.
        email (str): The email address associated with the Gmail service.
        email_id (str): The ID of the email to be moved to trash.

    Returns:
        dict: A dictionary containing either a success message or an error message.
    """
    gmail = authenticate_service(user, email)["gmail"]

    if not gmail:
        return {"error": "No gmail service provided"}

    try:
        response = gmail.users().messages().trash(userId="me", id=email_id).execute()

        if "id" in response:
            return {"message": "Email moved to trash successfully!"}
        else:
            LOGGER.error(f"Failed to move email with ID: {email_id} to trash")
            return {"error": "Failed to move email to trash"}
    except HTTPError as e:
        if "Requested entity was not found" in str(e):
            return {"message": "Email moved to trash successfully!"}
        else:
            LOGGER.error(
                f"Error when deleting email for user ID: {user.id}. Error: {str(e)}"
            )
            return {"error": str(e)}


def set_email_read(user: User, email: str, mail_id: str) -> dict:
    """
    Sets the status of the email with the specified ID to 'read' on Gmail.

    Args:
        user (User): The authenticated user object.
        email (str): The email address associated with the Gmail service.
        mail_id (str): The ID of the email to mark as read.

    Returns:
        dict: A dictionary indicating the result of the operation
    """
    services = authenticate_service(user, email)
    try:
        services["gmail"].users().messages().modify(
            userId="me", id=mail_id, body={"removeLabelIds": ["UNREAD"]}
        ).execute()
        return {"message": "Email marked as read successfully!"}
    except Exception as e:
        LOGGER.error(f"Failed to mark email ID {mail_id} as read: {str(e)}")
        return {"error": str(e)}


def set_email_unread(user: User, email: str, mail_id: str) -> dict:
    """
    Sets the status of the email with the specified ID to 'unread' on Gmail.

    Args:
        user (User): The authenticated user object.
        email (str): The email address associated with the Gmail service.
        mail_id (str): The ID of the email to mark as unread.

    Returns:
        dict: A dictionary indicating the result of the operation
    """
    services = authenticate_service(user, email)
    try:
        services["gmail"].users().messages().modify(
            userId="me", id=mail_id, body={"addLabelIds": ["UNREAD"]}
        ).execute()
        return {"message": "Email marked as unread successfully!"}
    except Exception as e:
        LOGGER.error(f"Failed to mark email ID {mail_id} as unread: {str(e)}")
        return {"error": str(e)}


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


def get_mail_to_db(services):
    """Retrieve email information for processing email to database."""

    service = services["gmail"]

    results: dict = (
        service.users()
        .messages()
        .list(userId="me", labelIds=["INBOX"], maxResults=1)
        .execute()
    )
    messages = results.get("messages", [])
    if not messages:
        return None

    message = messages[0]
    email_id = message["id"]

    msg: dict[str, dict[str, dict[str]]] = (
        service.users().messages().get(userId="me", id=email_id).execute()
    )
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
    attachments = []

    def process_part(part: dict[str, str]):
        nonlocal email_html, email_txt_html, email_detect_html, has_attachments, image_files, attachments

        if part["mimeType"] == "text/plain":
            if "data" in part["body"]:
                data: str = part["body"]["data"]
                decoded_data = base64.urlsafe_b64decode(data.encode("UTF-8")).decode(
                    "utf-8"
                )
                email_txt_html += f"<pre>{decoded_data}</pre>"
        elif part["mimeType"] == "text/html":
            if "data" in part["body"]:
                email_detect_html = True
                data: str = part["body"]["data"]
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
            print("---------------------------->", part)
            attachment_id = part["body"]["attachmentId"]
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

    cleaned_html = email_processing.html_clear(email_html)
    preprocessed_data = email_processing.preprocess_email(cleaned_html)
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


def get_mail_to_db(services: dict) -> tuple:
    """
    Retrieve email information from the Gmail API for processing and storing in the database.

    Args:
        services (dict): A dictionary containing authenticated service instances for various email providers,
                         including the Gmail service instance under the key "gmail".

    Returns:
        tuple: A tuple containing email information required for further processing and database storage:
            str: Subject of the email.
            tuple[str, str]: Tuple containing the sender's name and email address.
            str: Preprocessed email content (cleaned and summarized).
            str: Safe HTML version of the email content.
            str: ID of the email message.
            datetime.datetime: Sent date and time of the email.
            str: Web link to view the email in Gmail. (TODO: delete and update doc)
            bool: Flag indicating whether the email has attachments.
            bool: Flag indicating whether the email is a reply.
    """
    service = services["gmail"]

    results: dict = (
        service.users()
        .messages()
        .list(userId="me", labelIds=["INBOX"], maxResults=1)
        .execute()
    )
    messages = results.get("messages", [])
    if not messages:
        return None

    message = messages[0]
    email_id = message["id"]

    # Retrieve the detailed message content
    msg: dict[str, dict[str, dict[str]]] = (
        service.users().messages().get(userId="me", id=email_id).execute()
    )
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
    attachments = []

    def process_part(part: dict[str, str]):
        """
        Processes a part of the email to extract and decode its content, handling various MIME types.

        Args:
            part (dict[str, str]): A dictionary containing information about the email part, including its MIME type and body.
        """
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
            attachments.append(
                {"attachmentId": attachment_id, "attachmentName": part["filename"]}
            )

    # Process all parts of the email
    if "parts" in msg["payload"]:
        for part in msg["payload"]["parts"]:
            process_part(part)
    else:
        process_part(msg["payload"])

    # Use plain text version if no HTML version is detected
    if email_detect_html is False:
        email_html = email_txt_html

    # Replace CID references in HTML with local paths
    soup = BeautifulSoup(email_html, "html.parser")
    for img in soup.find_all("img"):
        cid_ref = img["src"].lstrip("cid:")
        for image_file in image_files:
            if cid_ref in image_file:
                img["src"] = f"{BASE_URL_MA}pictures/{os.path.basename(image_file)}"

    cleaned_html = email_processing.html_clear(email_html)
    preprocessed_data = email_processing.preprocess_email(cleaned_html)
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


def get_mail_id(services: dict, int_mail: int) -> str:
    """
    Retrieve the email ID of a specific email from the user's Gmail inbox.

    Args:
        services (dict): A dictionary containing service objects for various APIs,
                         including a "gmail" service object.
        int_mail (int): The index of the email in the inbox to retrieve the ID for.

    Returns:
        str: The ID of the specified email if found, otherwise None.
    """
    service = services["gmail"]

    results: dict = (
        service.users().messages().list(userId="me", labelIds=["INBOX"]).execute()
    )
    messages = results.get("messages", [])
    if not messages:
        return None

    return messages[int_mail]["id"]


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
    """
    Searches for emails matching the specified query parameters using the Gmail API.

    Args:
        services (dict[str, build]): A dictionary containing authenticated service instances for various email providers,
                                     including the Gmail service instance under the key "gmail".
        max_results (int, optional): The maximum number of email results to retrieve. Default is 100.
        filenames (list[str], optional): A list of filenames to search for in the attachments.
        from_addresses (list[str], optional): A list of sender email addresses to filter emails.
        to_addresses (list[str], optional): A list of recipient email addresses to filter emails.
        subject (str, optional): A subject string to filter emails.
        body (str, optional): A body string to filter emails.
        keywords (list[str], optional): A list of keywords to search for in the email body.
        date_from (str, optional): A date string in the format 'YYYY-MM-DD' to filter emails received after this date.
        search_in (dict[str, bool], optional): A dictionary specifying the folders to search in. Possible keys are:
            spams: Search in spam/junk folder.
            deleted_emails: Search in deleted items folder.
            drafts: Search in drafts folder.
            sent_emails: Search in sent items folder.

    Returns:
        list[str]: A list of email IDs that match the search criteria.
    """
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

    try:
        service = services["gmail"]
        results: dict = (
            service.users()
            .messages()
            .list(userId="me", q=query, maxResults=max_results)
            .execute()
        )
        messages = results.get("messages", [])

        return [message["id"] for message in messages]

    except Exception as e:
        LOGGER.error(f"Failed to search emails from Google API with Ao help: {str(e)}")
        return []


def search_emails_manually(
    services: dict[str, build],
    search_query: str,
    max_results: int = 100,
    file_extensions: list[str] = None,
    advanced: bool = False,
    search_in: dict[str, bool] = None,
    from_addresses: list[str] = None,
    to_addresses: list[str] = None,
    subject: str = None,
    body: str = None,
    date_from: str = None,
) -> list[str]:
    """
    Searches for emails matching the specified query parameters using the Gmail API.

    Args:
        services (dict[str, build]): A dictionary containing authenticated service instances for various email providers,
                                     including the Gmail service instance under the key "gmail".
        search_query (str): The basic search query string to use for simple searches.
        max_results (int, optional): The maximum number of email results to retrieve. Default is 100.
        file_extensions (list[str], optional): A list of file extensions to search for in the attachments.
        advanced (bool, optional): Flag indicating whether to use advanced search parameters. Default is False.
        search_in (dict[str, bool], optional): A dictionary specifying the folders to search in. Possible keys are:
            spams: Search in spam/junk folder.
            deleted_emails: Search in deleted items folder.
            drafts: Search in drafts folder.
            sent_emails: Search in sent items folder.
        from_addresses (list[str], optional): A list of sender email addresses to filter emails.
        to_addresses (list[str], optional): A list of recipient email addresses to filter emails.
        subject (str, optional): A subject string to filter emails.
        body (str, optional): A body string to filter emails.
        date_from (str, optional): A date string in the format 'YYYY-MM-DD' to filter emails received after this date.

    Returns:
        list[str]: A list of email IDs that match the search criteria.
    """

    def search(query: str) -> list:
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
            LOGGER.error(
                f"Failed to execute the search emails query from Google API: {str(e)}"
            )
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
                    [f"in:{folder}" for folder, include in search_in.items() if include]
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
        LOGGER.error(f"Failed to search emails from Google API: {str(e)}")
        return []


# ----------------------- EMAIL ATTACHMENT -----------------------#
def get_attachment_data(
    user: User, email: str, email_id: str, attachment_name: str
) -> dict:
    """
    Retrieves the data for a specific attachment from an email using the Gmail API.

    Args:
        user (User): The user object containing authentication details.
        email (str): The email address of the user.
        email_id (str): The ID of the email containing the attachment.
        attachment_name (str): The name of the attachment to retrieve.

    Returns:
        dict: A dictionary containing the attachment name and data, or an empty dictionary if not found.
    """
    try:
        services = authenticate_service(user, email)
        if not services or "gmail" not in services:
            return {}

        gmail_service = services["gmail"]
        message: dict[str, dict] = (
            gmail_service.users().messages().get(userId="me", id=email_id).execute()
        )

        if "payload" in message:
            parts: list[dict[str, dict]] = message["payload"].get("parts", [])
            for part in parts:
                part_filename = part.get("filename", "")
                if part_filename == attachment_name:
                    attachment_id = part.get("body", {}).get("attachmentId", "")
                    if attachment_id:
                        attachment = (
                            gmail_service.users()
                            .messages()
                            .attachments()
                            .get(userId="me", messageId=email_id, id=attachment_id)
                            .execute()
                        )

                        data: str = attachment["data"]
                        attachment_data = base64.urlsafe_b64decode(data.encode("UTF-8"))
                        return {
                            "attachmentName": part["filename"],
                            "data": attachment_data,
                        }

        return {}

    except Exception as e:
        LOGGER.error(
            f"Failed to get attachment data for email ID {email_id} and attachment {attachment_name}: {str(e)}"
        )
        return {}


# ----------------------- READ EMAIL -----------------------#
def parse_name_and_email(header_value: str) -> tuple[str | None, str]:
    """
    Parses the name and email address from a given email header value.

    Args:
        header_value (str): The header value containing either just an email address or both a name and an email address.

    Returns:
        tuple: A tuple containing the parsed name and email address:
            str or None: The parsed name, if available, otherwise None.
            str: The parsed email address, or the original header value if no name was found.
    """
    if not header_value:
        return None, None

    match = re.match(r"(.*)\s*<(.+)>", header_value)
    if match:
        name, email = match.groups()
        return name.strip(), email.strip()
    else:
        return None, header_value.strip()


def search_emails(services: dict, search_query: str, max_results=2):
    """
    Searches for email addresses in the user's mailbox based on the provided search query in both the subject and body.

    Args:
        services (dict): A dictionary containing authenticated service instances for various email providers,
                         including the Gmail service instance under the key "gmail".
        search_query (str): The search query string to search for in email subjects and bodies.
        max_results (int, optional): Maximum number of email results to retrieve. Defaults to 2.

    Returns:
        dict: A dictionary mapping found email addresses (keys) to corresponding sender names (values).
    """
    service = services["gmail"]

    try:
        results: dict = (
            service.users()
            .messages()
            .list(userId="me", q=search_query, maxResults=max_results)
            .execute()
        )
        messages = results.get("messages", [])
        found_emails = {}

        for message in messages:
            msg: dict = (
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
            sender: str = next(
                (header["value"] for header in headers if header["name"] == "From"),
                None,
            )

            if sender:
                email = sender.split("<")[-1].split(">")[0].strip().lower()
                name = sender.split("<")[0].strip().lower() if "<" in sender else email

                # Additional filtering: Check if the sender email/name matches the search query
                if search_query.lower() in email or search_query.lower() in name:
                    if email and not email_processing.is_no_reply_email(email):
                        found_emails[email] = name

        return found_emails

    except Exception as e:
        LOGGER.error(
            f"Failed to search emails from Google API. Query: {search_query}. Error: {str(e)}"
        )
        return {}


######################## PROFILE REQUESTS ########################
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
@permission_classes([IsAuthenticated])
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


######################## GOOGLE LISTENER ########################
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
                    result = email_to_db(social_api.user, services, social_api)

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


def email_to_db(user: User, services, social_api: SocialAPI) -> bool | str:
    """
    Saves email notifications from Google listener to the database.

    Args:
        user (User): The user object for whom the email is being saved.
        services: The authenticated Google API services.
        social_api (SocialAPI): The SocialAPI instance associated with the user.

    Returns:
        bool | str: True if the email was successfully saved, False if there was an issue saving the email,
                    or an error message if an exception occurred.
    """
    LOGGER.info(
        f"Starting the process of saving email from Google API to database for user ID: {user.id}"
    )

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
        social_api.user_description if social_api.user_description else ""
    )
    language = Preference.objects.get(user=user).language

    if not decoded_data:
        LOGGER.info(
            f"No decoded data retrieved from Google API for user ID: {user.id} and email ID: {email_id}"
        )
        return "No decoded data"

    sender = Sender.objects.filter(email=from_name[1]).first()
    category_dict = email_processing.get_db_categories(user)
    category = Category.objects.get(name=DEFAULT_CATEGORY, user=user)
    rules = Rule.objects.filter(sender=sender)
    rule_category = None

    if rules.exists():
        for rule in rules:
            if rule.block:
                return True

            if rule.category:
                category = rule.category
                rule_category = True

    email_content = email_processing.preprocess_email(decoded_data)
    search = Search(user.id)

    if is_reply:
        conversation_summary = search.summarize_conversation(
            subject, email_content, user_description, language
        )
    else:
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

    importance = None

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

    if not rule_category and topic in category_dict:
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
                CC_sender.objects.create(mail_id=email_entry, email=email, name=name)

        if bcc_info:
            for email, name in bcc_info:
                BCC_sender.objects.create(mail_id=email_entry, email=email, name=name)

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

        LOGGER.info(
            f"Email ID: {email_id} saved to database successfully for user ID: {user.id} using Google API"
        )
        return True

    except Exception as e:
        LOGGER.error(
            f"An error occurred when trying to create an email with ID {email_id} for user ID: {user.id}: {str(e)}"
        )
        return str(e)


###########################################################################
######################## TO DELETE IN THE FUTURE ? ########################
###########################################################################
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
            return None
        message = messages[int_mail]
        email_id = message["id"]
    elif id_mail is not None:
        email_id = id_mail
    else:
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
            decoded_data_temp = email_processing.process_part(part, plaintext_var)

            print(
                "______________________DATA decoded_data_temp (PARTS) looks like that ______________________________"
            )
            print(decoded_data_temp)
            print(
                "___________________________________________________________________________________"
            )
            if decoded_data_temp:
                decoded_data = email_processing.concat_text(decoded_data, decoded_data_temp)
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
        decoded_data = email_processing.html_clear(decoded_data_temp)

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
