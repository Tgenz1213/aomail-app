"""
TODO: one line description
This module is the stuff that defines how to send and treansfer emails usign Microsoft Graph API

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
from aomail.models import Email


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
            LOGGER.error(f"Failed to schedule email: {error}")
            return Response({"error": error}, status=response.status_code)

    except Exception as e:
        LOGGER.error(f"Failed to send email: {str(e)}")
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
            LOGGER.error(f"Failed to send email: {error}")
            return Response({"error": error}, status=response.status_code)

    except Exception as e:
        LOGGER.error(f"Failed to send email: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
