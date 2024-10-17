"""
Handles email operations, returns results to frontend, and saves to database.

Endpoints:
- ✅ archive_email: Archive an email.
- ✅ delete_email: Delete an email.
- ✅ delete_emails: Delete emails by priority or IDs.
- ✅ get_first_email: Get the first email in the database.
- ✅ get_mail_by_id: Retrieve email details by ID.
- ✅ retrieve_attachment_data: Get attachment data by email and attachment ID.
- ✅ set_email_not_reply_later: Unmark email for later reply.
- ✅ set_email_read: Mark email as read.
- ✅ set_email_reply_later: Mark email for later reply.
- ✅ set_email_unread: Mark email as unread.
"""

import json
import logging
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from aomail.utils.security import subscription
from aomail.constants import ALLOWED_PLANS, GOOGLE, MICROSOFT
from aomail.models import SocialAPI, Email
from aomail.email_providers.google import authentication as auth_google
from aomail.email_providers.microsoft import authentication as auth_microsoft
from aomail.email_providers.microsoft import (
    email_operations as email_operations_microsoft,
)
from aomail.email_providers.google import (
    email_operations as email_operations_google,
)
from aomail.utils.serializers import (
    EmailReadUpdateSerializer,
    EmailReplyLaterUpdateSerializer,
)


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)
READ_EMAILS_MARKER = "read"


@api_view(["GET"])
@subscription(ALLOWED_PLANS)
def get_first_email(request: HttpRequest) -> Response:
    """
    Returns the first email associated with the user in the database.

    Args:
        request (HttpRequest): HTTP request object.

    Returns:
        Response: {"email": "<email_address>"} if an email is found.
    """
    user = request.user
    social_api = SocialAPI.objects.filter(user=user).first()

    return Response({"email": social_api.email}, status=status.HTTP_200_OK)


@api_view(["GET"])
@subscription(ALLOWED_PLANS)
def get_mail_by_id(request: HttpRequest) -> Response:
    """
    Retrieves details of an email by its ID associated with the authenticated user.

    Args:
        request (HttpRequest): HTTP request object containing the email_id parameter in GET.

    Returns:
        Response:
            - Success (HTTP 200 OK): JSON object with email details (subject, decodedData, cc, bcc, date, emailUser).
            - Failure (HTTP 400 BAD REQUEST): Error message if "email_id" is missing.
    """
    user = request.user
    mail_id = request.GET.get("email_id")

    email = get_object_or_404(Email, user=user, provider_id=mail_id)
    social_api = email.social_api
    email_user = social_api.email
    type_api = social_api.type_api

    if mail_id:
        if type_api == GOOGLE:
            services = auth_google.authenticate_service(user, email_user)
            subject, _, decoded_data, cc, bcc, _, date = (
                email_operations_google.get_mail(services, None, mail_id)
            )
        elif type_api == MICROSOFT:
            access_token = auth_microsoft.refresh_access_token(
                auth_microsoft.get_social_api(user, email_user)
            )
            subject, _, decoded_data, cc, bcc, _, date, _ = (
                email_operations_microsoft.get_mail(access_token, None, mail_id)
            )

        if cc:
            cc = tuple(item for item in cc if item is not None)
        if bcc:
            bcc = tuple(item for item in bcc if item is not None)

        return Response(
            {
                "subject": subject,
                "decodedData": decoded_data,
                "cc": cc,
                "bcc": bcc,
                "date": date,
                "emailUser": email_user,
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {"error": "No email ID provided"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def set_email_read(request: HttpRequest, email_id: int) -> Response:
    """
    Marks a specific email as read for the authenticated user.

    Args:
        request (HttpRequest): HTTP request object.
        email_id (int): The ID of the email to mark as read.

    Returns:
        Response: JSON response with the serialized data of the updated email,
                  status=status.HTTP_200_OK if successful.
    """
    user = request.user
    try:
        email = get_object_or_404(Email, user=user, id=email_id)
        email.read = True
        email.read_date = timezone.now()
        email.save()

        social_api = email.social_api
        if social_api:
            if social_api.type_api == GOOGLE:
                email_operations_google.set_email_read(
                    user, social_api.email, email.provider_id
                )
            elif social_api.type_api == MICROSOFT:
                email_operations_microsoft.set_email_read(social_api, email.provider_id)

        serializer = EmailReadUpdateSerializer(email)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@subscription(ALLOWED_PLANS)
def set_email_unread(request: HttpRequest, email_id: int) -> Response:
    """
    Marks a specific email as unread for the authenticated user.

    Args:
        request (HttpRequest): HTTP request object.
        email_id (int): The ID of the email to mark as unread.

    Returns:
        Response: JSON response with the serialized data of the updated email,
                      status=status.HTTP_200_OK if successful.
    """
    user = request.user
    try:
        email = get_object_or_404(Email, user=user, id=email_id)
        email.read = False
        email.read_date = None
        email.save()

        social_api = email.social_api
        if social_api.type_api == GOOGLE:
            email_operations_google.set_email_unread(
                user, social_api.email, email.provider_id
            )
        elif social_api.type_api == MICROSOFT:
            email_operations_microsoft.set_email_unread(social_api, email.provider_id)

        serializer = EmailReadUpdateSerializer(email)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@subscription(ALLOWED_PLANS)
def set_email_reply_later(request: HttpRequest, email_id: int) -> Response:
    """
    Marks a specific email for later reply for the authenticated user.

    Args:
        request (HttpRequest): HTTP request object.
        email_id (int): The ID of the email to mark for later reply.

    Returns:
        Response: JSON response with the serialized data of the updated email,
                      status=status.HTTP_200_OK if successful.
    """
    user = request.user
    try:
        email = get_object_or_404(Email, user=user, id=email_id)
        email.answer_later = True
        email.save()

        serializer = EmailReplyLaterUpdateSerializer(email)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@subscription(ALLOWED_PLANS)
def set_email_not_reply_later(request: HttpRequest, email_id: int) -> Response:
    """
    Unmarks a specific email for later reply for the authenticated user.

    Args:
        request (HttpRequest): HTTP request object.
        email_id (int): The ID of the email to unmark for later reply.

    Returns:
        Response: JSON response with the serialized data of the updated email,
                      status=status.HTTP_200_OK if successful.
    """
    user = request.user
    try:
        email = get_object_or_404(Email, user=user, id=email_id)
        email.answer_later = False
        email.save()

        serializer = EmailReplyLaterUpdateSerializer(email)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# TODO: delete this comment after front-end implementation
# ENDPOINTS TO DELETE ALL USELESS, INFORMATIVE, IMPORTANT EMAILS
@api_view(["POST"])
@subscription(ALLOWED_PLANS)
def delete_emails(request: HttpRequest) -> Response:
    """
    Delete emails based on the priority or specific email IDs provided in the request body.

    Args:
        request (HttpRequest): The HTTP request object containing user and body parameters:
            priority (str): Priority level of emails to delete.
            clean (bool): Flag indicating whether to perform a clean deletion.
            emailIds (list[int]): List of specific email IDs to delete.

    Returns:
        Response: JSON response indicating success or failure of email deletion.
    """
    parameters: dict = json.loads(request.body)
    user = request.user
    priority: str = parameters.get("priority")
    clean: bool = parameters.get("clean")

    if not priority:
        return Response(
            {"error": "No priority provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    if priority == READ_EMAILS_MARKER:
        emails = Email.objects.filter(user=user, read=True)
        for email in emails:
            email.delete()

        return Response(
            {"message": "Read emails deleted successfully"}, status=status.HTTP_200_OK
        )

    if clean:
        emails = Email.objects.filter(user=user, priority=priority)
        for email in emails:
            email.delete()

    else:
        email_ids: list[int] = parameters.get("emailIds", [])
        for email_id in email_ids:
            try:
                email = Email.objects.get(user=user, id=email_id)
                email.delete()
            except Email.DoesNotExist:
                pass

    return Response(
        {"message": "Emails deleted successfully"}, status=status.HTTP_200_OK
    )


@api_view(["DELETE"])
@subscription(ALLOWED_PLANS)
def delete_email(request: HttpRequest, email_id: int) -> Response:
    """
    Deletes an email associated with the authenticated user.

    Args:
        request (HttpRequest): HTTP request object.
        email_id (int): The ID of the email to delete.

    Returns:
        Response: {"message": "Email deleted successfully"} if the email is deleted successfully,
                      or {"error": <error_message>} with status HTTP 500 Internal Server Error if there's an issue.
    """
    try:
        user = request.user
        email = Email.objects.get(user=user, id=email_id)
        social_api = email.social_api
        type_api = social_api.type_api
        provider_id = email.provider_id
        email.delete()

        if type_api == GOOGLE:
            result = email_operations_google.delete_email(
                user, social_api.email, provider_id
            )
        elif type_api == MICROSOFT:
            result = email_operations_microsoft.delete_email(provider_id, social_api)

        if result.get("message", "") == "Email moved to trash successfully!":
            return Response(
                {"message": "Email deleted successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": result.get("error")},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    except Email.DoesNotExist:
        return Response(
            {"error": "Email not found"}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        LOGGER.error(f"Error when deleting email: {str(e)}")
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT"])
@subscription(ALLOWED_PLANS)
def archive_email(request: HttpRequest, email_id: int) -> Response:
    """
    Archives an email associated with the authenticated user.

    Args:
        request (HttpRequest): HTTP request object.
        email_id (int): The ID of the email to archive.

    Returns:
        Response: {"message": "Email archived successfully"} if the email is archived successfully,
                      or {"error": <error_message>} with appropriate status code otherwise.
    """
    try:
        user = request.user
        email = Email.objects.get(user=user, id=email_id)
        email.archive = True
        email.save()
        return Response(
            {"message": "Email archived successfully"}, status=status.HTTP_200_OK
        )
    except Email.DoesNotExist:
        return Response(
            {"error": "Email not found"}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        LOGGER.error(f"Error when archiving email: {str(e)}")
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


####################################################################
######################## UNDER CONSTRUCTION ########################
####################################################################
@api_view(["GET"])
@subscription(ALLOWED_PLANS)
def retrieve_attachment_data(
    request: HttpRequest, email_id: str, attachment_name: str
) -> Response:
    """
    Retrieves email attachment data for a specific email and attachment ID.

    Args:
        request (HttpRequest): The HTTP request object.
        email_id (str): The ID of the email containing the attachment.
        attachment_id (str): The ID of the attachment to retrieve.

    Returns:
        Response: JSON response containing the attachment data.
                      Returns status=status.HTTP_200_OK on success.
    """
    user = request.user
    email = get_object_or_404(Email, user=user, id=email_id)
    social_api = email.social_api

    if social_api.type_api == GOOGLE:
        attachment_data = email_operations_google.get_attachment_data(
            user, social_api.email, email.provider_id, attachment_name
        )
        if attachment_data:
            response = HttpResponse(
                attachment_data["data"], content_type="application/octet-stream"
            )
            response["Content-Disposition"] = (
                f'attachment; filename="{attachment_name}"'
            )
            return response
        else:
            return Response(
                {"error": "Attachment not found"}, status=status.HTTP_404_NOT_FOUND
            )
    elif social_api.type_api == MICROSOFT:
        # TODO: Implement handling for Microsoft API attachments
        return Response(
            {"error": "Microsoft API attachment handling not implemented yet"},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )
