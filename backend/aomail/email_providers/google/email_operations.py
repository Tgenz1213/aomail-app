"""
Provides email search and operation functions using Google API.

Endpoints:
- ✅ send_email: Sends an email using the Gmail API. 
- ✅ get_mail: Retrieves email details by index or message ID. 
"""

import base64
import json
import logging
import uuid
from urllib.parse import unquote 
import re
import string
import threading
import time
import random
import os
from rest_framework import status
from django.http import HttpRequest
from django.contrib.auth.models import User
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from httpx import HTTPError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from email.utils import parsedate_to_datetime
from aomail.utils.serializers import EmailDataSerializer
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from aomail.utils.security import subscription
from aomail.constants import (
    ALLOWED_PLANS,
    MEDIA_ROOT,
    MEDIA_URL,
    BASE_URL_MA,
)
from aomail.email_providers.google.authentication import (
    authenticate_service,
)
from aomail.utils import email_processing
from aomail.models import SocialAPI
from base64 import urlsafe_b64encode
from base64 import b64encode, b64decode
from bs4 import BeautifulSoup


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


@api_view(["POST"])
@subscription(ALLOWED_PLANS)
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
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        to = request.POST.getlist("to")
        cc = request.POST.getlist("cc")
        bcc = request.POST.getlist("bcc")
        attachments = request.FILES.getlist("attachments")
        
        if not email or not subject or not message or not to:
            return Response(
                {"error": "Missing required email parameters."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        service = authenticate_service(user, email, ["gmail"])["gmail"]

        multipart_message = MIMEMultipart()
        multipart_message["subject"] = subject
        multipart_message["from"] = "me"
        multipart_message["to"] = ", ".join(to)

        all_recipients = to

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
            target=email_processing.save_contacts,
            args=(user, all_recipients),
        ).start()

        return Response(
            {"message": "Email sent successfully!"}, status=status.HTTP_200_OK
        )

    except Exception as e:
        LOGGER.error(f"Failed to send email: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

        
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
    gmail = authenticate_service(user, email, ["gmail"])["gmail"]

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
            return {"error": "Internal server error"}


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
    service = authenticate_service(user, email, ["gmail"])["gmail"]
    try:
        service["gmail"].users().messages().modify(
            userId="me", id=mail_id, body={"removeLabelIds": ["UNREAD"]}
        ).execute()
        return {"message": "Email marked as read successfully!"}
    except Exception as e:
        LOGGER.error(f"Failed to mark email ID {mail_id} as read: {str(e)}")
        return {"error": "Internal server error"}


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
    service = authenticate_service(user, email, ["gmail"])["gmail"]
    try:
        service["gmail"].users().messages().modify(
            userId="me", id=mail_id, body={"addLabelIds": ["UNREAD"]}
        ).execute()
        return {"message": "Email marked as unread successfully!"}
    except Exception as e:
        LOGGER.error(f"Failed to mark email ID {mail_id} as unread: {str(e)}")
        return {"error": "Internal server error"}


def search_emails_ai(
    services: dict[str, build],
    max_results: int = 100,
    file_extensions: list[str] = None,
    filenames: list[str] = None,
    from_addresses: list[str] = None,
    to_addresses: list[str] = None,
    subject: str = None,
    body: str = None,
    keywords: list[str] = None,
    date_from: str = None,
    search_in: dict[str, bool] = None,
) -> list:
    """
    Searches for emails matching the specified query parameters using the Gmail API.

    Args:
        services (dict[str, build]): A dictionary containing authenticated service instances for various email providers,
                                     including the Gmail service instance under the key "gmail".
        max_results (int, optional): The maximum number of email results to retrieve. Default is 100.
        file_extensions (list[str], optional): A list of file extensions to search for in the attachments.
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

    # Build the main query
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

    # Combine all parts with OR logic
    query = " OR ".join(query_parts)

    # Build the additional filters
    additional_query_parts = []
    if filenames:
        filename_query = " OR ".join([f"filename:{name}" for name in filenames])
        additional_query_parts.append(f"({filename_query})")
    if file_extensions:
        file_ext_query = " OR ".join([f"filename:{ext}" for ext in file_extensions])
        additional_query_parts.append(f"({file_ext_query})")
    if date_from:
        additional_query_parts.append(f"(after:{date_from})")
    if keywords:
        keyword_query = " OR ".join([f'"{keyword}"' for keyword in keywords])
        additional_query_parts.append(f"({keyword_query})")

    # Combine additional filters with AND logic
    if additional_query_parts:
        query += " AND " + " AND ".join(additional_query_parts)

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
        LOGGER.error(f"Failed to search emails from Google API with AI help: {str(e)}")
        return []


def search_emails_manually(
    services: dict[str, build],
    search_query: str = "",
    max_results: int = 100,
    file_extensions: list[str] = None,
    filenames: list[str] = None,
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
        search_query (str, optional): The basic search query string to use for simple searches.
        max_results (int, optional): The maximum number of email results to retrieve. Default is 100.
        file_extensions (list[str], optional): A list of file extensions to search for in the attachments.
        filenames (list[str], optional): A list of filenames to search for in the attachments.
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
        """Executes the search query and retrieves email messages."""
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
        messages = []

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

            # Construct the file extensions and filenames filter
            if file_extensions:
                file_ext_query = " OR ".join(
                    [f"filename:{ext}" for ext in file_extensions]
                )
                query_parts.append(f"({file_ext_query})")
            if filenames:
                file_name_query = " OR ".join(
                    [f"filename:{name}" for name in filenames]
                )
                query_parts.append(f"({file_name_query})")

            # Combine all parts into a single query
            if query_parts:
                query = " AND ".join(query_parts)
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


def get_demo_list(user: User, email: str) -> list[str]:
    """
    Retrieves a list of up to 10 email message IDs from the user's Gmail inbox.

    Args:
        user (User): The user object representing the email account owner.
        email (str): The email address of the user.

    Returns:
        list[str]: A list of up to 10 email message IDs from the inbox.
                   Returns an empty list if no messages are found.
    """
    service = authenticate_service(user, email, ["gmail"])["gmail"]

    results: dict = (
        service.users()
        .messages()
        .list(userId="me", labelIds=["INBOX"], maxResults=10)
        .execute()
    )
    messages = results.get("messages", [])

    return [msg["id"] for msg in messages] if messages else []


def get_mail_to_db(social_api: SocialAPI, email_id: str = None) -> dict:
    """
    Retrieves detailed email information from the Gmail API, processing it for storage in the database.

    Args:
        social_api (SocialAPI): Contains user and email data necessary for authentication and processing.
        email_id (str, optional): Specific email message ID to retrieve.
                                  If not provided, retrieves the most recent email.

    Returns:
        dict: Dictionary containing comprehensive email data needed for further processing and database storage:
            - subject (str): Subject of the email.
            - from_info (tuple[str, str]): Tuple with sender's name and email address.
            - preprocessed_data (str): Cleaned and summarized email content.
            - safe_html (str): HTML content of the email in a safe format.
            - email_id (str): Unique ID of the email message.
            - sent_date (datetime.datetime): Sent date and time of the email.
            - has_attachments (bool): Indicates if the email has attachments.
            - is_reply (bool): Indicates if the email is a reply.
            - cc_info (tuple[str, str] or None): CC recipient's name and email address, or None if absent.
            - bcc_info (tuple[str, str] or None): BCC recipient's name and email address, or None if absent.
            - image_files (list[str]): List of filenames for images embedded in the email.
            - attachments (list[dict]): List of dictionaries containing details about each attachment (ID and name).
    """
    service = authenticate_service(social_api.user, social_api.email, ["gmail"])["gmail"]

    if not email_id:
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

    has_attachments = False
    is_reply = "in-reply-to" in {header["name"].lower() for header in msg["payload"]["headers"]}
    email_html = ""
    email_txt_html = ""
    email_detect_html = False
    image_files = []
    attachments = []
    cid_to_filename = {} 

    def process_part(part: dict[str, str]):
        nonlocal email_html, email_txt_html, email_detect_html, has_attachments, image_files, attachments, cid_to_filename

        if part["mimeType"] == "text/plain":
            if "data" in part["body"]:
                data = part["body"]["data"]
                decoded_data = base64.urlsafe_b64decode(data.encode("UTF-8")).decode("utf-8")
                email_txt_html += f"<pre>{decoded_data}</pre>"
        elif part["mimeType"] == "text/html":
            if "data" in part["body"]:
                email_detect_html = True
                data = part["body"]["data"]
                decoded_data = base64.urlsafe_b64decode(data.encode("UTF-8")).decode("utf-8")
                email_html += decoded_data

                # Find and replace base64 encoded images in the HTML
                img_tags = re.findall(
                    r'<img[^>]+src="data:image/([^;]+);base64,([^"]+)"', decoded_data
                )
                for img_type, img_data in img_tags:
                    image_filename = f"{uuid.uuid4()}.{img_type}"
                    image_files.append(image_filename)

                    img_data_bytes = base64.b64decode(img_data.encode("UTF-8"))
                    image_path = os.path.join(MEDIA_ROOT, "pictures", image_filename)

                    with open(image_path, "wb") as img_file:
                        img_file.write(img_data_bytes)

                    email_html = email_html.replace(
                        f"data:image/{img_type};base64,{img_data}",
                        f"{MEDIA_URL}pictures/{image_filename}",
                    )
        elif part["mimeType"].startswith("image/"):
            # Get the Content-ID
            cid = None
            if "headers" in part:
                for header in part["headers"]:
                    if header["name"].lower() == "content-id":
                        cid = header["value"].strip().strip("<>")
                        cid = unquote(cid).lower()

            img_type = part["mimeType"].split("/")[-1]
            image_filename = f"{uuid.uuid4()}.{img_type}"
            image_files.append(image_filename)

            image_path = os.path.join(MEDIA_ROOT, "pictures", image_filename)

            if "attachmentId" in part["body"]:
                attachment_id = part["body"]["attachmentId"]
                attachment = (
                    service.users()
                    .messages()
                    .attachments()
                    .get(userId="me", messageId=email_id, id=attachment_id)
                    .execute()
                )
                file_data = base64.urlsafe_b64decode(attachment["data"].encode("UTF-8"))
            elif "data" in part["body"]:
                file_data = base64.urlsafe_b64decode(part["body"]["data"].encode("UTF-8"))
            else:
                return

            with open(image_path, "wb") as img_file:
                img_file.write(file_data)

            # Map the CID to the image filename
            if cid:
                cid_to_filename[cid] = image_filename

        elif part["mimeType"].startswith("multipart/"):
            if "parts" in part:
                for subpart in part["parts"]:
                    process_part(subpart)
        elif "filename" in part:
            has_attachments = True
            attachment_id = part["body"]["attachmentId"]
            attachments.append({"attachmentId": attachment_id, "attachmentName": part["filename"]})

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
        src = img.get("src", "")
        if src.startswith("cid:"):
            cid_ref = src[4:].strip().strip("<>").strip()
            cid_ref = unquote(cid_ref).lower()
            LOGGER.info(f"Found CID in HTML: '{cid_ref}'")
            if cid_ref in cid_to_filename:
                img["src"] = f"{BASE_URL_MA}pictures/{cid_to_filename[cid_ref]}?v={uuid.uuid4()}"
            else:
                LOGGER.error(f"CID '{cid_ref}' not found in mapping")

    cleaned_html = email_processing.html_clear(str(soup))
    preprocessed_data = email_processing.preprocess_email(cleaned_html)
    safe_html = soup.prettify()

    return {
        "subject": subject,
        "from_info": from_info,
        "preprocessed_data": preprocessed_data,
        "safe_html": safe_html,
        "email_id": email_id,
        "sent_date": sent_date,
        "has_attachments": has_attachments,
        "is_reply": is_reply,
        "cc_info": cc_info,
        "bcc_info": bcc_info,
        "image_files": image_files,
        "attachments": attachments,
    }


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


def get_mails_batch(services: dict, email_ids: list[str]) -> list[dict]:
    """
    Retrieves email information for a batch of email IDs using the Gmail API.

    Args:
        services (dict): A dictionary containing authenticated service instances for various email providers,
                         including the Gmail service instance under the key "gmail".
        email_ids (list[str]): A list of email IDs to retrieve information for.

    Returns:
        list[dict]: A list of dictionaries, each containing the following information for an email:
            subject (str): Subject of the email.
            from_info (tuple[str, str]): Tuple containing the sender's name and email address.
            email_id (str): ID of the email message.
            has_attachments (bool): Flag indicating whether the email has attachments.
            is_reply (bool): Flag indicating whether the email is a reply.
            cc_info (list[tuple[str, str]]): List of CC recipients (name, email).
            bcc_info (list[tuple[str, str]]): List of BCC recipients (name, email).
    """
    service = services["gmail"]
    batch = service.new_batch_http_request()
    email_info = {}

    def callback(request_id, response, exception):
        if exception is not None:
            LOGGER.error(f"Error fetching email {request_id}: {str(exception)}")
            return

        email_id = request_id
        msg = response

        email_data = msg["payload"]["headers"]
        subject = from_info = cc_info = bcc_info = None
        for values in email_data:
            name = values["name"]
            if name == "Subject":
                subject = values["value"]
            elif name == "From":
                from_info = parse_name_and_email(values["value"])
            elif name == "Cc":
                cc_info = [
                    parse_name_and_email(cc) for cc in values["value"].split(",")
                ]
            elif name == "Bcc":
                bcc_info = [
                    parse_name_and_email(bcc) for bcc in values["value"].split(",")
                ]

        has_attachments = False
        is_reply = "in-reply-to" in {
            header["name"].lower() for header in msg["payload"]["headers"]
        }
        email_html = ""
        email_txt_html = ""

        def process_part(part):
            nonlocal email_html, email_txt_html, has_attachments

            if part["mimeType"] == "text/plain":
                if "data" in part["body"]:
                    data = part["body"]["data"]
                    decoded_data = base64.urlsafe_b64decode(
                        data.encode("UTF-8")
                    ).decode("utf-8")
                    email_txt_html += f"<pre>{decoded_data}</pre>"
            elif part["mimeType"] == "text/html":
                if "data" in part["body"]:
                    data = part["body"]["data"]
                    decoded_data = base64.urlsafe_b64decode(
                        data.encode("UTF-8")
                    ).decode("utf-8")
                    email_html += decoded_data
            elif "filename" in part:
                has_attachments = True

        if "parts" in msg["payload"]:
            for part in msg["payload"]["parts"]:
                process_part(part)
        else:
            process_part(msg["payload"])

        if not email_html:
            email_html = email_txt_html

        email_info[email_id] = {
            "subject": subject,
            "from_info": from_info,
            "email_id": email_id,
            "has_attachments": has_attachments,
            "is_reply": is_reply,
            "cc_info": cc_info,
            "bcc_info": bcc_info,
        }

    # Ensure email_ids are unique
    unique_email_ids = list(set(email_ids))

    for email_id in unique_email_ids:
        try:
            batch.add(
                service.users().messages().get(userId="me", id=email_id),
                callback=callback,
                request_id=email_id,
            )
        except Exception as e:
            LOGGER.error(f"Error adding email {email_id} to batch: {str(e)}")

    try:
        batch.execute()
    except Exception as e:
        LOGGER.error(f"Error executing batch request: {str(e)}")

    return list(email_info.values())


def get_mail(services: dict, int_mail: int = None, id_mail: str = None) -> tuple:
    """
    Retrieve email information including subject, sender, content, CC, BCC, and ID.

    Args:
        services (dict): A dictionary of authenticated service clients (e.g., Gmail API service).
        int_mail (int, optional): Index of the email in the inbox. If specified, overrides `id_mail`.
        id_mail (str, optional): ID of the specific email to retrieve.

    Returns:
        tuple: A tuple containing:
            - subject (str): Subject of the email.
            - from_info (tuple[str, str]): Sender's name and email address.
            - decoded_data (str): Processed email body content.
            - cc_info (list[tuple[str, str]]): CC recipients' names and email addresses.
            - bcc_info (list[tuple[str, str]]): BCC recipients' names and email addresses.
            - email_id (str): ID of the email message.
            - sent_date (datetime.datetime): Date and time the email was sent.
    """
    service = services["gmail"]
    plaintext_var = [0]
    plaintext_var[0] = 0

    if int_mail:
        results = (
            service.users().messages().list(userId="me", labelIds=["INBOX"]).execute()
        )
        messages = results.get("messages", [])
        if not messages:
            return None
        message = messages[int_mail]
        email_id = message["id"]
    elif id_mail:
        email_id = id_mail

    msg = service.users().messages().get(userId="me", id=email_id).execute()

    subject = from_info = decoded_data = None
    cc_info = bcc_info = []
    email_data = msg["payload"]["headers"]

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
            if decoded_data_temp:
                decoded_data = email_processing.concat_text(
                    decoded_data, decoded_data_temp
                )
    elif "body" in msg["payload"]:
        data = msg["payload"]["body"]["data"]
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
    )


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
        dict: A dictionary containing:
            - attachmentName (str): The name of the attachment.
            - data (bytes): The attachment data.
            - Returns an empty dictionary if the attachment is not found.
    """
    try:
        services = authenticate_service(user, email, ["gmail"])
        if not services:
            return {}

        gmail_service = services["gmail"]
        message = (
            gmail_service.users().messages().get(userId="me", id=email_id).execute()
        )

        if "payload" in message:
            parts = message["payload"].get("parts", [])
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

                        data = attachment["data"]
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
