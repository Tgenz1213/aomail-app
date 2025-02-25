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
from aomail.models import Email, SocialAPI, Agent, Signature
from aomail.email_providers.microsoft.email_operations import get_mail_to_db
from aomail.ai_providers.utils import update_tokens_stats
from aomail.ai_providers.google.client import generate_email_response


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

    Args:
        email_id (str): The ID of the email to transfer
        social_api (SocialAPI): The social API credentials object containing authentication info
        recipients (list[str]): List of email addresses to send the email to

    Returns:
        bool: True if email was transferred successfully, False otherwise
    """
    try:
        LOGGER.info(
            f"Initiating email transfer - ID: {email_id} to recipients: {', '.join(recipients)}"
        )

        access_token = refresh_access_token(social_api)
        headers = get_headers(access_token)

        email_data = get_mail_to_db(social_api, email_id)

        subject = email_data["subject"]
        message = email_data["email_html"]
        attachments = email_data["attachments"]

        email_content = {
            "message": {
                "subject": subject,
                "body": {"contentType": "HTML", "content": message},
                "toRecipients": [
                    {"emailAddress": {"address": email}} for email in recipients
                ],
            }
        }

        if attachments:
            email_content["message"]["attachments"] = []

            for attachment in attachments:
                try:
                    # As we can not forward directly via Microsoft API, we must re-download each attachment
                    attachment_url = f"{GRAPH_URL}me/messages/{email_id}/attachments/{attachment['id']}"
                    attachment_response = requests.get(attachment_url, headers=headers)

                    if attachment_response.status_code == 200:
                        attachment_data = attachment_response.json()

                        email_content["message"]["attachments"].append(
                            {
                                "@odata.type": "#microsoft.graph.fileAttachment",
                                "name": attachment["name"],
                                "contentBytes": attachment_data["contentBytes"],
                            }
                        )

                        LOGGER.info(f"Successfully attached file: {attachment['name']}")
                    else:
                        LOGGER.error(
                            f"Failed to get attachment {attachment['name']}: {attachment_response.text}"
                        )
                except Exception as e:
                    LOGGER.error(
                        f"Failed to process attachment {attachment['name']}: {str(e)}"
                    )
                    continue

        graph_endpoint = f"{GRAPH_URL}me/sendMail"
        response = requests.post(graph_endpoint, headers=headers, json=email_content)

        if response.status_code == 202:
            threading.Thread(
                target=email_processing.save_contacts,
                args=(social_api.user, recipients),
            ).start()

            LOGGER.info(
                f"Email transfer completed successfully - ID: {email_id} sent to {len(recipients)} recipients"
            )
            return True
        else:
            response_data = response.json()
            error = response_data.get("error", response.reason)
            LOGGER.error(
                f"Failed to transfer email {email_id}. Error: {error}. Status code: {response.status_code}"
            )
            return False

    except Exception as e:
        LOGGER.error(f"Email transfer failed - ID: {email_id} - Error: {str(e)}")
        return False


def reply_email_microsoft(email_entry: Email, prompt: str) -> bool:
    """
    Replies to an email using the Microsoft Graph API and AI-generated content.

    Args:
        email_entry (Email): The original email object to reply to
        prompt (str): User instructions for generating the reply

    Returns:
        bool: True if reply was sent successfully, False otherwise
    """
    try:
        LOGGER.info(f"Initiating email reply - ID: {email_entry.message_id}")
        agents = Agent.objects.filter(user=email_entry.user, last_used=True)
        signatures = Signature.objects.filter(
            user=email_entry.user, social_api=email_entry.social_api
        )

        signature = signatures.first() if signatures else None
        agent_settings = (
            {
                "ai_template": agents.first().ai_template,
                "email_example": agents.first().email_example,
                "length": agents.first().length,
                "formality": agents.first().formality,
                "language": agents.first().language,
            }
            if agents
            else {}
        )

        response = generate_email_response(
            email_entry.subject,
            email_entry.html_content,
            prompt,
            agent_settings,
            signature,
        )

        update_tokens_stats(email_entry.user, response)

        subject = f"Re: {email_entry.subject}"
        message = response["body"]
        to = [email_entry.from_email]

        social_api = email_entry.social_api
        access_token = refresh_access_token(social_api)
        headers = get_headers(access_token)

        email_content = {
            "message": {
                "subject": subject,
                "body": {"contentType": "HTML", "content": message},
                "toRecipients": [{"emailAddress": {"address": email}} for email in to],
            }
        }

        graph_endpoint = f"{GRAPH_URL}me/sendMail"
        response = requests.post(graph_endpoint, headers=headers, json=email_content)

        if response.status_code == 202:
            threading.Thread(
                target=email_processing.save_contacts,
                args=(email_entry.user, to),
            ).start()

            LOGGER.info(
                f"Reply sent successfully to email ID: {email_entry.message_id}"
            )
            return True
        else:
            response_data = response.json()
            error = response_data.get("error", response.reason)
            LOGGER.error(
                f"Failed to send reply. Error: {error}. Status code: {response.status_code}"
            )
            return False

    except Exception as e:
        LOGGER.error(
            f"Failed to send reply to email ID {email_entry.message_id}: {str(e)}"
        )
        return False
