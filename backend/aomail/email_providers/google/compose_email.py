"""
TODO: one line description
This module is the stuff that defines how to send and treansfer emails usign gmail api

Endpoints:
- ✅ send_email: Sends an email using the Gmail API. 
"""

import logging
import threading
from rest_framework import status
from django.http import HttpRequest
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view
from aomail.utils.security import subscription
from aomail.constants import ALLOW_ALL
from aomail.email_providers.google.authentication import (
    authenticate_service,
)
from aomail.utils import email_processing
from aomail.models import Email
from base64 import urlsafe_b64encode


LOGGER = logging.getLogger(__name__)


@api_view(["POST"])
@subscription(ALLOW_ALL)
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


def transfer_email(email_entry: Email, recipients: list[str]):
    """
    Transfer an email to a list of recipients
    """
    pass
