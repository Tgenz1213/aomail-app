"""
Handles email composition and transfer operations using the Gmail API.

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
from aomail.email_providers.google.email_operations import get_mail_to_db
from aomail.utils import email_processing
from aomail.models import SocialAPI
from base64 import urlsafe_b64encode, urlsafe_b64decode


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


def transfer_email(email_id: str, social_api: SocialAPI, recipients: list[str]) -> bool:
    """
    Transfers an existing email to new recipients using the Gmail API.

    Args:
        email_id (str): The ID of the email to transfer
        social_api (SocialAPI): The social API instance containing user and authentication info
        recipients (list[str]): List of email addresses to send the email to

    Returns:
        bool: True if transfer was successful, False otherwise
    """
    try:
        LOGGER.info(
            f"Initiating email transfer - ID: {email_id} to recipients: {', '.join(recipients)}"
        )
        user = social_api.user
        service = authenticate_service(user, social_api.email, ["gmail"])["gmail"]

        email_data = get_mail_to_db(social_api, email_id)
        subject = email_data["subject"]
        message = email_data["email_html"]
        to = recipients
        cc = []
        bcc = []
        attachments = email_data["attachments"]

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
            for attachment in attachments:
                try:
                    # As we can not forward directly via Gmail API, we must re-download each attachment
                    attachment_data = (
                        service.users()
                        .messages()
                        .attachments()
                        .get(
                            userId="me",
                            messageId=email_id,
                            id=attachment["attachmentId"],
                        )
                        .execute()
                    )

                    file_data = urlsafe_b64decode(
                        attachment_data["data"].encode("UTF-8")
                    )

                    part = MIMEApplication(file_data)
                    part.add_header(
                        "Content-Disposition",
                        "attachment",
                        filename=attachment["attachmentName"],
                    )
                    multipart_message.attach(part)
                    LOGGER.info(
                        f"Successfully attached file: {attachment['attachmentName']}"
                    )
                except Exception as e:
                    LOGGER.error(
                        f"Failed to attach file {attachment['attachmentName']}: {str(e)}"
                    )
                    continue

        raw_message = urlsafe_b64encode(
            multipart_message.as_string().encode("UTF-8")
        ).decode()

        body = {"raw": raw_message}
        service.users().messages().send(userId="me", body=body).execute()

        threading.Thread(
            target=email_processing.save_contacts,
            args=(user, all_recipients),
        ).start()

        LOGGER.info(
            f"Email transfer completed successfully - ID: {email_id} sent to {len(recipients)} recipients"
        )
        return True

    except Exception as e:
        LOGGER.error(f"Email transfer failed - ID: {email_id} - Error: {str(e)}")
        return False
