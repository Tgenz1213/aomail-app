"""
Handles email operations, returns results to frontend, and saves to database.

Endpoints:
- ✅ archive_email: Archive an email.
- ✅ delete_email: Delete an email.
- ✅ delete_emails: Delete emails by priority or IDs.
- ✅ get_answer_later_emails: Retrieve emails flagged for later reply.
- ✅ get_first_email: Get the first email in the database.
- ✅ get_mail_by_id: Retrieve email details by ID.
- ✅ get_user_emails: Retrieve and format user emails by category and priority.
- ✅ retrieve_attachment_data: Get attachment data by email and attachment ID.
- ✅ set_email_not_reply_later: Unmark email for later reply.
- ✅ set_email_read: Mark email as read.
- ✅ set_email_reply_later: Mark email for later reply.
- ✅ set_email_unread: Mark email as unread.


TODO:
- (ANTI scraping/reverse engineering): Add a system that counts the number of 400 erros per user and send warning + ban
- Add a filter function for emails + max_results per page (scam, newsletter, importance, etc) (for reply later & home)
- get_answer_later_emails & get_user_emails can form only 1 function with parameters
"""

import datetime
import json
import logging
import threading
from collections import defaultdict
from django.db.models import Subquery, Exists, OuterRef
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MailAssistant.utils.security import subscription
from MailAssistant.constants import (
    FREE_PLAN,
    GOOGLE_PROVIDER,
    IMPORTANT,
    INFORMATIVE,
    MICROSOFT_PROVIDER,
    USELESS,
)
from MailAssistant.email_providers import google_api, microsoft_api
from MailAssistant.models import (
    CC_sender,
    Category,
    SocialAPI,
    Email,
    Rule,
)
from MailAssistant.utils.serializers import (
    EmailReadUpdateSerializer,
    EmailReplyLaterUpdateSerializer,
)


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)
READ_EMAILS_MARKER = "read"


@api_view(["GET"])
@subscription([FREE_PLAN])
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
@subscription([FREE_PLAN])
def get_mail_by_id(request: HttpRequest) -> Response:
    """
    Retrieves details of an email by its ID associated with the authenticated user.

    Args:
        request (HttpRequest): HTTP request object containing the email_id parameter in GET.

    Returns:
        Response:
            {"message": "Authentication successful", "email": {...}} if the email is retrieved successfully.
            {"error": "No email ID provided"} if no email_id parameter is provided in the request.
    """
    user = request.user
    mail_id = request.GET.get("email_id")

    email = get_object_or_404(Email, user=user, provider_id=mail_id)
    social_api = email.social_api
    email_user = social_api.email
    type_api = social_api.type_api

    if mail_id:
        if type_api == "google":
            services = google_api.authenticate_service(user, email_user)
            subject, from_name, decoded_data, cc, bcc, email_id, date, _ = (
                google_api.get_mail(services, None, mail_id)
            )
        elif type_api == "microsoft":
            access_token = microsoft_api.refresh_access_token(
                microsoft_api.get_social_api(user, email_user)
            )
            subject, from_name, decoded_data, cc, bcc, email_id, date, _ = (
                microsoft_api.get_mail(access_token, None, mail_id)
            )

        if cc:
            cc = tuple(item for item in cc if item is not None)
        if bcc:
            bcc = tuple(item for item in bcc if item is not None)

        return Response(
            {
                "message": "Authentication successful",
                "email": {
                    "subject": subject,
                    "from_name": from_name,
                    "decoded_data": decoded_data,
                    "cc": cc,
                    "bcc": bcc,
                    "email_id": email_id,
                    "date": date,
                    "email_receiver": email_user,
                },
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

    email = get_object_or_404(Email, user=user, id=email_id)
    email.read = True
    email.read_date = timezone.now()
    email.save()

    social_api = email.social_api
    if social_api:
        if social_api.type_api == "google":
            google_api.set_email_read(user, social_api.email, email.provider_id)
        elif social_api.type_api == "microsoft":
            microsoft_api.set_email_read(social_api, email.provider_id)

    serializer = EmailReadUpdateSerializer(email)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@subscription([FREE_PLAN])
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

    email = get_object_or_404(Email, user=user, id=email_id)
    email.read = False
    email.read_date = None
    email.save()

    social_api = email.social_api
    if social_api.type_api == "google":
        google_api.set_email_unread(user, social_api.email, email.provider_id)
    elif social_api.type_api == "microsoft":
        microsoft_api.set_email_unread(social_api, email.provider_id)

    serializer = EmailReadUpdateSerializer(email)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@subscription([FREE_PLAN])
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
    email = get_object_or_404(Email, user=user, id=email_id)
    email.answer_later = True
    email.save()

    serializer = EmailReplyLaterUpdateSerializer(email)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@subscription([FREE_PLAN])
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
    email = get_object_or_404(Email, user=user, id=email_id)
    email.answer_later = False
    email.save()

    serializer = EmailReplyLaterUpdateSerializer(email)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
@subscription([FREE_PLAN])
def get_answer_later_emails(request: HttpRequest) -> Response:
    """
    Retrieve emails flagged for answering later by the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the user information.

    Returns:
        Response: JSON response containing the list of emails flagged for answering later,
                      grouped by priority, or an error message if retrieval fails.
    """
    try:
        user = request.user
        emails = (
            Email.objects.filter(user=user, answer_later=True)
            .prefetch_related("category", "cc_senders", "bcc_senders", "attachments")
            .select_related("sender")
        )

        # Annotate emails with rule existence and rule id
        rule_id_subquery = Rule.objects.filter(
            sender=OuterRef("sender"), user=user
        ).values("id")[:1]
        emails = emails.annotate(
            has_rule=Exists(rule_id_subquery), rule_id=Subquery(rule_id_subquery)
        )

        formatted_data = defaultdict(lambda: defaultdict(list))

        current_datetime_utc = timezone.now()
        for email in emails:
            if email.read_date:
                delta_time = current_datetime_utc - email.read_date

                # Delete read email older than 1 week
                if delta_time > datetime.timedelta(weeks=1):
                    email.delete()
                    continue

            email_data = {
                "id": email.id,
                "id_provider": email.provider_id,
                "subject": email.subject,
                "sender": {
                    "email": email.sender.email,
                    "name": email.sender.name,
                },
                "short_summary": email.short_summary,
                "one_line_summary": email.one_line_summary,
                "html_content": email.html_content,
                "cc": [
                    {"email": cc.email, "name": cc.name}
                    for cc in email.cc_senders.all()
                ],
                "bcc": [
                    {"email": bcc.email, "name": bcc.name}
                    for bcc in email.bcc_senders.all()
                ],
                "read": email.read,
                "rule": {
                    "has_rule": email.has_rule,
                    "rule_id": email.rule_id,
                },
                "answer_later": email.answer_later,
                "has_attachments": email.has_attachments,
                "attachments": [
                    {
                        "attachmentName": attachment.name,
                        "attachmentId": attachment.id_api,
                    }
                    for attachment in email.attachments.all()
                ],
                "sent_date": email.date.date() if email.date else None,
                "sent_time": email.date.strftime("%H:%M") if email.date else None,
                "answer": email.answer,
                "relevance": email.relevance,
                "priority": email.priority,
                "flags": {
                    "spam": email.spam,
                    "scam": email.scam,
                    "newsletter": email.newsletter,
                    "notification": email.notification,
                    "meeting": email.meeting,
                },
            }

            formatted_data[email.category.name][email.priority].append(email_data)

        # Ensuring all priorities are present for each category
        all_priorities = {IMPORTANT, INFORMATIVE, USELESS}
        for category in formatted_data:
            for priority in all_priorities:
                formatted_data[category].setdefault(priority, [])

        return Response(formatted_data, status=status.HTTP_200_OK)

    except Exception as e:
        LOGGER.error(f"Error fetching answer-later emails: {str(e)}")
        return Response(
            {"error": "Failed to retrieve answer-later emails."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# TODO: delete this comment after front-end implementation
# ENDPOINTS TO DELETE ALL USELESS, INFORMATIVE, IMPORTANT EMAILS
@api_view(["POST"])
@subscription([FREE_PLAN])
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
@subscription([FREE_PLAN])
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

        if type_api == "google":
            result = google_api.delete_email(user, social_api.email, provider_id)
        elif type_api == "microsoft":
            result = microsoft_api.delete_email(provider_id, social_api)

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
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@subscription([FREE_PLAN])
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
        email.delete()
        return Response(
            {"message": "Email archived successfully"}, status=status.HTTP_200_OK
        )
    except Email.DoesNotExist:
        return Response(
            {"error": "Email not found"}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        LOGGER.error(f"Error when archiving email: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import HttpRequest
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from collections import defaultdict
import json
import datetime
from django.db.models import Q
from django.db import models


# TODO: create a endpoint get_emails_data (returns data for a list of ids (between 25 and 100 ids max))
# TODO: change the name

# sort
# Newest First/Oldest First = order by date

# ALL potential filters # TODO: fix my potential enlgish typing mistakes
# THIS IS THE BEGINNING OF THE DOCUMENTAION
{
    "emailProvider": list[str],
    "subject": str,
    "senderEmail": str,
    "senderName": str,
    "CCEmails": list[str],
    "CCNames": list[str],
    "emailAdresses": list[str],
    "read": bool,
    "sentDate": models.DateTimeField,
    "readDate": models.DateTimeField,
    "answer": list[str],
    "relevance": list[str],
    "priority": list[str],
    "spam": bool,
    "scam": bool,
    "newsletter": bool,
    "notification": bool,
    "meeting": bool,
}


@api_view(["POST"])
@permission_classes([AllowAny])
def get_user_emails_with_filter(request: HttpRequest) -> Response:
    try:
        parameters: dict = json.loads(request.body)
        category: str = parameters["category"]
        result_per_page: int = parameters["resultPerPage"]
        if not 25 <= result_per_page <= 100:
            return Response(
                {"error": "resultPerPage must be an integer between 25 and 100 included"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the user from the request
        user = 1  # leave it hardcoded for testing

        filters = {"user": user, "answer_later": False}

        category_obj = Category.objects.get(name=category)
        filters["category"] = category_obj

        # List of boolean fields we want to filter
        boolean_fields = [
            "scam",
            "spam",
            "newsletter",
            "notification",
            "meeting",
            "read",
            "hasAttachments",
        ]
        for field in boolean_fields:
            if field in parameters:
                filters[field] = parameters[field]

        # Additional filters
        if "priority" in parameters:
            filters["priority__in"] = parameters["priority"]
        if "emailProvider" in parameters:
            filters["email_provider__in"] = parameters["emailProvider"]
        if "subject" in parameters:
            filters["subject__icontains"] = parameters["subject"]
        if "senderEmail" in parameters:
            filters["sender__email__icontains"] = parameters["senderEmail"]
        if "senderName" in parameters:
            filters["sender__name__icontains"] = parameters["senderName"]
        if "sentDate" in parameters:
            filters["date__gte"] = parameters["sentDate"]
        if "readDate" in parameters:
            filters["read_date__gte"] = parameters["readDate"]
        if "answer" in parameters:
            filters["answer__in"] = parameters["answer"]
        if "relevance" in parameters:
            filters["relevance__in"] = parameters["relevance"]
        if "emailAddresses" in parameters:
            social_apis = SocialAPI.objects.filter(
                email__in=parameters["emailAddresses"], user=user
            )
            filters["social_api__in"] = social_apis
        if "CCEmails" in parameters:
            filters["cc_senders__email__in"] = parameters["CCEmails"]
        if "CCNames" in parameters:
            filters["cc_senders__name__in"] = parameters["CCNames"]

        # Make the query
        queryset = Email.objects.filter(**filters)
        rule_id_subquery = Rule.objects.filter(
            sender=OuterRef("sender"), user=user
        ).values("id")[:1]
        queryset = queryset.annotate(
            has_rule=Exists(rule_id_subquery), rule_id=Subquery(rule_id_subquery)
        )
        # Apply sorting
        queryset.order_by("-date")

        email_count = queryset.count()
        email_ids = []
        formatted_data = defaultdict(lambda: defaultdict(list))
        nb_email_treated = 0

        current_datetime_utc = timezone.now()
        for email in queryset:
            if email.read_date:
                delta_time = current_datetime_utc - email.read_date

                # Delete read email older than 1 week
                if delta_time > datetime.timedelta(weeks=1):
                    email.delete()
                    continue

            if nb_email_treated < result_per_page:
                email_data = {
                    "id": email.id,
                    "id_provider": email.provider_id,
                    "subject": email.subject,
                    "sender": {
                        "email": email.sender.email,
                        "name": email.sender.name,
                    },
                    "short_summary": email.short_summary,
                    "one_line_summary": email.one_line_summary,
                    # "html_content": email.html_content,
                    "cc": [
                        {"email": cc.email, "name": cc.name}
                        for cc in email.cc_senders.all()
                    ],
                    "bcc": [
                        {"email": bcc.email, "name": bcc.name}
                        for bcc in email.bcc_senders.all()
                    ],
                    "read": email.read,
                    "rule": {
                        "has_rule": email.has_rule,
                        "rule_id": email.rule_id,
                    },
                    "answer_later": email.answer_later,
                    "has_attachments": email.has_attachments,
                    "attachments": [
                        {
                            "attachmentName": attachment.name,
                            "attachmentId": attachment.id_api,
                        }
                        for attachment in email.attachments.all()
                    ],
                    "sent_date": email.date.date() if email.date else None,
                    "sent_time": email.date.strftime("%H:%M") if email.date else None,
                    "answer": email.answer,
                    "relevance": email.relevance,
                    "priority": email.priority,
                    "flags": {
                        "spam": email.spam,
                        "scam": email.scam,
                        "newsletter": email.newsletter,
                        "notification": email.notification,
                        "meeting": email.meeting,
                    },
                }
                formatted_data[email.category.name][email.priority].append(email_data)
                nb_email_treated += 1

            email_ids.append(email.id)

        return Response(
            {"count": email_count, "data": formatted_data, "ids": email_ids},
            status=status.HTTP_200_OK,
        )
    except Category.DoesNotExist:
        return Response(
            {"error": "Invalid category"}, status=status.HTTP_400_BAD_REQUEST
        )
    except KeyError:
        return Response(
            {"error": "Invalid JSON keys in request body"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except TypeError:
        return Response(
            {"error": "resultPerPage must be an integer"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON in request body"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )



# import uuid
# import random

# EMAIL_PROVIDERS = [GOOGLE_PROVIDER, MICROSOFT_PROVIDER]


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def get_user_emails_with_filter(request: HttpRequest) -> Response:
#     try:
#         parameters = json.loads(request.body)
#         user = 1  # Hardcoded for testing

#         # Create the queryset with all filters applied
#         filters = {"user": user, "answer_later": False}
#         queryset = Email.objects.filter(**filters).order_by("-date")
#         first_email = queryset.first()

#         if first_email:
#             for i in range(999):
#                 email = Email.objects.create(
#                     user=first_email.user,
#                     social_api=first_email.social_api,
#                     provider_id=str(uuid.uuid4()),  # Generating a unique UUID
#                     subject=first_email.subject,
#                     sender=first_email.sender,
#                     short_summary=first_email.short_summary,
#                     one_line_summary="this is a one line summary",
#                     html_content=first_email.html_content,
#                     date=timezone.now()
#                     + datetime.timedelta(
#                         days=random.randint(-1825, 1825)
#                     ),  # Random date within ±5 years
#                     read_date=timezone.now()
#                     + datetime.timedelta(
#                         days=random.randint(-1825, 1825)
#                     ),  # Random date within ±5 years
#                     has_attachments=random.choice([True, False]),
#                     answer=random.choice(
#                         [
#                             "Answer Required",
#                             "Might Require Answer",
#                             "No Answer Required",
#                         ]
#                     ),
#                     relevance=random.choice(
#                         ["Highly Relevant", "Possibly Relevant", "Not Relevant"]
#                     ),
#                     priority=random.choice([IMPORTANT, INFORMATIVE, USELESS]),
#                     scam=random.choice([True, False]),
#                     spam=random.choice([True, False]),
#                     newsletter=random.choice([True, False]),
#                     notification=random.choice([True, False]),
#                     meeting=random.choice([True, False]),
#                     category=first_email.category,
#                     email_provider=random.choice(EMAIL_PROVIDERS),
#                 )
#                 CC_sender.objects.create(
#                     mail_id=email,
#                     email=random.choice(
#                         [
#                             "augustin.rolet.pro@gmail.com",
#                             "augustin@MailAssistant.onmicrosoft.com",
#                         ]
#                     ),
#                     name="name",
#                 )
#                 print(f"Created email {i + 1}/999")

#         return Response(
#             {"message": "Emails filtered and duplicated successfully"},
#             status=status.HTTP_200_OK,
#         )
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@subscription([FREE_PLAN])
def get_user_emails(request: HttpRequest) -> Response:
    """
    Retrieves and formats user emails grouped by category and priority.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: A JSON response containing formatted user emails grouped by category and priority.
                  Each email entry includes details such as ID, provider ID, sender information,
                  subject, content, attachments, date, time, read status, rules applied, and other metadata.
                  Returns status=status.HTTP_200_OK on success.
    """
    user = request.user
    emails = (
        Email.objects.filter(user=user)
        .prefetch_related("category", "cc_senders", "bcc_senders", "attachments")
        .select_related("sender")
    )

    # Annotate emails with rule existence and rule id
    rule_id_subquery = Rule.objects.filter(sender=OuterRef("sender"), user=user).values(
        "id"
    )[:1]
    emails = emails.annotate(
        has_rule=Exists(rule_id_subquery), rule_id=Subquery(rule_id_subquery)
    )

    formatted_data = defaultdict(lambda: defaultdict(list))

    current_datetime_utc = timezone.now()
    for email in emails:
        if email.read_date:
            delta_time = current_datetime_utc - email.read_date

            # Delete read email older than 1 week
            if delta_time > datetime.timedelta(weeks=1):
                email.delete()
                continue

        email_data = {
            "id": email.id,
            "id_provider": email.provider_id,
            "subject": email.subject,
            "sender": {
                "email": email.sender.email,
                "name": email.sender.name,
            },
            "short_summary": email.short_summary,
            "one_line_summary": email.one_line_summary,
            "html_content": email.html_content,
            "cc": [
                {"email": cc.email, "name": cc.name} for cc in email.cc_senders.all()
            ],
            "bcc": [
                {"email": bcc.email, "name": bcc.name}
                for bcc in email.bcc_senders.all()
            ],
            "read": email.read,
            "rule": {
                "has_rule": email.has_rule,
                "rule_id": email.rule_id,
            },
            "answer_later": email.answer_later,
            "has_attachments": email.has_attachments,
            "attachments": [
                {
                    "attachmentName": attachment.name,
                    "attachmentId": attachment.id_api,
                }
                for attachment in email.attachments.all()
            ],
            "sent_date": email.date.date() if email.date else None,
            "sent_time": email.date.strftime("%H:%M") if email.date else None,
            "answer": email.answer,
            "relevance": email.relevance,
            "priority": email.priority,
            "flags": {
                "spam": email.spam,
                "scam": email.scam,
                "newsletter": email.newsletter,
                "notification": email.notification,
                "meeting": email.meeting,
            },
        }

        formatted_data[email.category.name][email.priority].append(email_data)

    # Ensuring all priorities are present for each category
    all_priorities = {IMPORTANT, INFORMATIVE, USELESS}
    for category in formatted_data:
        for priority in all_priorities:
            formatted_data[category].setdefault(priority, [])

    return Response(formatted_data, status=status.HTTP_200_OK)


####################################################################
######################## UNDER CONSTRUCTION ########################
####################################################################
@api_view(["GET"])
@subscription([FREE_PLAN])
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

    if social_api.type_api == "google":
        attachment_data = google_api.get_attachment_data(
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
            return Response({"error": "Attachment not found"}, status=404)
    elif social_api.type_api == "microsoft":
        # TODO: Implement handling for Microsoft API attachments
        return Response(
            {"error": "Microsoft API attachment handling not implemented yet"},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )
