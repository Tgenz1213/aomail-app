"""
Module for handling email composition and sending using Microsoft Graph API.

Endpoints:
- ✅ send_schedule_email: Schedule the sending of an email.
- ✅ send_email: Sends an email using the Microsoft Graph API.
"""

import base64
import logging
import threading
import requests
from django.http import HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from aomail.utils.security import subscription
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from aomail.email_providers.microsoft.authentication import (
    get_headers,
    get_social_api,
    refresh_access_token,
)
from aomail.utils import email_processing
from aomail.constants import ALLOW_ALL, GRAPH_URL
from aomail.models import SocialAPI
from aomail.email_providers.microsoft.email_operations import get_mail_to_db


LOGGER = logging.getLogger(__name__)


@api_view(["POST"])
@subscription(ALLOW_ALL)
def send_schedule_email(request: HttpRequest) -> Response:
    """
    Schedule the sending of an email using the Microsoft Graph API with deferred delivery.

    Args:
        request (HttpRequest): HTTP request object containing POST data with email details.

    Returns:
        Response: Response indicating success or error.
    """
    user = request.user
    email = request.POST.get("email")
    subject = request.POST.get("subject")
    message = request.POST.get("message")
    to = request.POST.getlist("to")
    cc = request.POST.getlist("cc")
    bcc = request.POST.getlist("bcc")
    attachments = request.FILES.getlist("attachments")

    social_api = get_social_api(user, email)

    if not social_api:
        return Response(
            {"error": "Social API credentials not found"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    access_token = refresh_access_token(social_api)

    if not email or not subject or not message or not to:
        return Response(
            {"error": "Missing required email parameters."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        graph_endpoint = f"{GRAPH_URL}me/sendMail"
        headers = get_headers(access_token)

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

        raw_message = base64.b64encode(
            multipart_message.as_string().encode("utf-8")
        ).decode("utf-8")

        email_content = {
            "message": {
                "subject": subject,
                "body": {"contentType": "HTML", "content": message},
                "toRecipients": [{"emailAddress": {"address": email}} for email in to],
                "ccRecipients": (
                    [{"emailAddress": {"address": email}} for email in cc] if cc else []
                ),
                "bccRecipients": (
                    [{"emailAddress": {"address": email}} for email in bcc]
                    if bcc
                    else []
                ),
                "attachments": (
                    [
                        {
                            "@odata.type": "#microsoft.graph.fileAttachment",
                            "name": uploaded_file.name,
                            "contentBytes": base64.b64encode(
                                uploaded_file.read()
                            ).decode("utf-8"),
                        }
                        for uploaded_file in attachments
                    ]
                    if attachments
                    else []
                ),
            }
        }

        response = requests.post(graph_endpoint, headers=headers, json=email_content)

        if response.status_code == 202:
            threading.Thread(
                target=email_processing.save_contacts,
                args=(user, all_recipients),
            ).start()
            return Response(
                {"message": "Email scheduled successfully!"},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            response_data: dict = response.json()
            error = response_data.get("error", response.reason)
            LOGGER.error(
                f"Failed to schedule email. API Response: {error}. Status code: {response.status_code}"
            )
            return Response({"error": error}, status=response.status_code)

    except Exception as e:
        LOGGER.error(
            f"Failed to schedule email due to internal error: {str(e)}", exc_info=True
        )
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@subscription(ALLOW_ALL)
def send_email(request: HttpRequest) -> Response:
    """
    Sends an email using the Microsoft Graph API.

    Args:
        request (HttpRequest): HTTP request object containing POST data with email details.

    Returns:
        Response: Response indicating success or error.
    """
    user = request.user
    email = request.POST.get("email")
    subject = request.POST.get("subject")
    message = request.POST.get("message")
    to = request.POST.getlist("to")
    cc = request.POST.getlist("cc")
    bcc = request.POST.getlist("bcc")
    attachments = request.FILES.getlist("attachments")

    social_api = get_social_api(user, email)

    if not social_api:
        return Response(
            {"error": "Social API credentials not found"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    access_token = refresh_access_token(social_api)

    if not email or not subject or not message or not to:
        return Response(
            {"error": "Missing required email parameters."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        graph_endpoint = f"{GRAPH_URL}me/sendMail"
        headers = get_headers(access_token)

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

        raw_message = base64.b64encode(
            multipart_message.as_string().encode("utf-8")
        ).decode("utf-8")

        email_content = {
            "message": {
                "subject": subject,
                "body": {"contentType": "HTML", "content": message},
                "toRecipients": [{"emailAddress": {"address": email}} for email in to],
                "ccRecipients": (
                    [{"emailAddress": {"address": email}} for email in cc] if cc else []
                ),
                "bccRecipients": (
                    [{"emailAddress": {"address": email}} for email in bcc]
                    if bcc
                    else []
                ),
                "attachments": (
                    [
                        {
                            "@odata.type": "#microsoft.graph.fileAttachment",
                            "name": uploaded_file.name,
                            "contentBytes": base64.b64encode(
                                uploaded_file.read()
                            ).decode("utf-8"),
                        }
                        for uploaded_file in attachments
                    ]
                    if attachments
                    else []
                ),
            }
        }

        response = requests.post(graph_endpoint, headers=headers, json=email_content)

        if response.status_code == 202:
            threading.Thread(
                target=email_processing.save_contacts,
                args=(user, all_recipients),
            ).start()
            return Response(
                {"message": "Email sent successfully!"},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            response_data: dict = response.json()
            error = response_data.get("error", response.reason)
            LOGGER.error(
                f"Failed to send email. API Response: {error}. Status code: {response.status_code}"
            )
            return Response({"error": error}, status=response.status_code)

    except Exception as e:
        LOGGER.error(
            f"Failed to send email due to internal error: {str(e)}", exc_info=True
        )
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def transfer_email(email_id: str, social_api: SocialAPI, recipients: list[str]) -> bool:
    """
    Transfer an email to a list of recipients using Microsoft Graph API.

    This function retrieves an existing email by its ID and forwards it to specified recipients.
    It preserves the original email content, subject, and attachments while sending to new recipients.

    Args:
        email_id (str): The ID of the email to transfer
        social_api (SocialAPI): The social API credentials object containing authentication info
        recipients (list[str]): List of email addresses to send the email to

    Returns:
        bool: True if email was transferred successfully, False otherwise
    """
    email_data = get_mail_to_db(social_api, email_id)

    user = social_api.user
    email = email_data["email"]
    subject = email_data["subject"]
    message = email_data["safe_html"]
    to = recipients
    cc = []
    bcc = []
    attachments = email_data["attachments"]

    access_token = refresh_access_token(social_api)

    if not email or not subject or not message or not to:
        LOGGER.error("Missing required email parameters for transfer")
        return False

    try:
        graph_endpoint = f"{GRAPH_URL}me/sendMail"
        headers = get_headers(access_token)

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

        raw_message = base64.b64encode(
            multipart_message.as_string().encode("utf-8")
        ).decode("utf-8")

        email_content = {
            "message": {
                "subject": subject,
                "body": {"contentType": "HTML", "content": message},
                "toRecipients": [{"emailAddress": {"address": email}} for email in to],
                "ccRecipients": (
                    [{"emailAddress": {"address": email}} for email in cc] if cc else []
                ),
                "bccRecipients": (
                    [{"emailAddress": {"address": email}} for email in bcc]
                    if bcc
                    else []
                ),
                "attachments": (
                    [
                        {
                            "@odata.type": "#microsoft.graph.fileAttachment",
                            "name": uploaded_file.name,
                            "contentBytes": base64.b64encode(
                                uploaded_file.read()
                            ).decode("utf-8"),
                        }
                        for uploaded_file in attachments
                    ]
                    if attachments
                    else []
                ),
            }
        }

        response = requests.post(graph_endpoint, headers=headers, json=email_content)

        if response.status_code == 202:
            threading.Thread(
                target=email_processing.save_contacts,
                args=(user, all_recipients),
            ).start()
            LOGGER.info(
                f"Successfully transferred email {email_id} to {len(recipients)} recipients"
            )
            return True
        else:
            response_data: dict = response.json()
            error = response_data.get("error", response.reason)
            LOGGER.error(
                f"Failed to transfer email {email_id}. Error: {error}. Status code: {response.status_code}"
            )
            return False

    except Exception as e:
        LOGGER.error(
            f"Failed to transfer email {email_id} due to internal error: {str(e)}",
            exc_info=True,
        )
        return False
