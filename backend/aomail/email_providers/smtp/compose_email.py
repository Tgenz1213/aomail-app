"""
Handles email composition and transfer operations using SMTP protocol.

Endpoints:
- ✅ send_email: Sends an email.
"""

import logging
from rest_framework import status
from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from aomail.utils.security import subscription
from aomail.constants import ALLOW_ALL
from aomail.models import SocialAPI
from aomail.email_providers.smtp.authentication import connect_to_smtp

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
    user = request.user
    email = request.POST.get("email")
    social_api = SocialAPI.objects.get(user=user, email=email)

    smtp_connection = connect_to_smtp(
        social_api.email,
        social_api.smtp_config.app_password,
        social_api.smtp_config.host,
        social_api.smtp_config.port,
        social_api.smtp_config.encryption,
    )

    if not smtp_connection:
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = request.POST.get("subject")
    msg["From"] = social_api.email

    msg.attach(MIMEText(request.POST.get("message"), "html"))

    smtp_connection.sendmail(
        social_api.email,
        request.POST.getlist("to")
        + request.POST.getlist("cc")
        + request.POST.getlist("bcc"),
        msg.as_string(),
    )
    smtp_connection.quit()

    return Response({"message": "Email sent successfully!"}, status=status.HTTP_200_OK)
