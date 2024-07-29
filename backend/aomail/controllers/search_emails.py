"""
Handles searching emails among Aomail database, filtering, sorting, and retrieving email content.

Endpoints:
- ✅ get_user_emails: Retrieves filtered and formatted user emails grouped by category and priority.
- ✅ get_email_content: Retrieves HTML content of a specific email for display.
- ✅ get_emails_data: Retrieves formatted email data to be displayed.


TODO:
- (ANTI scraping/reverse engineering): Add a system that counts the number of 400 erros per user and send warning + ban
"""

import json
import logging
from collections import defaultdict
from datetime import timedelta
from django.db.models import Exists, OuterRef, Q, Subquery
from django.db.models.manager import BaseManager
from django.http import HttpRequest
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from aomail.constants import FREE_PLAN
from aomail.models import Category, SocialAPI, Email, Rule
from aomail.utils.security import subscription
from django.contrib.auth.models import User
from aomail.models import (
    Category,
    SocialAPI,
    Email,
    Rule,
)


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


@api_view(["POST"])
@subscription([FREE_PLAN])
def get_emails_data(request: HttpRequest) -> Response:
    """
    Retrieves detailed data for multiple emails based on provided email IDs.

    Args:
        request (HttpRequest): The HTTP request object containing JSON data with email IDs.

    Returns:
        Response: HTTP response object containing formatted data categorized by email categories
                  and priorities.
    """
    try:
        user = request.user
        parameters: dict = json.loads(request.body)
        email_ids = parameters.get("ids")

        if not (25 <= len(email_ids) <= 100):
            return Response(
                {"error": "IDs must be provided as a list with 25 to 100 elements"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        formatted_data = defaultdict(lambda: defaultdict(list))
        queryset = Email.objects.filter(id__in=email_ids)
        rule_id_subquery = Rule.objects.filter(
            sender=OuterRef("sender"), user=user
        ).values("id")[:1]
        queryset = queryset.annotate(
            has_rule=Exists(rule_id_subquery), rule_id=Subquery(rule_id_subquery)
        )

        for email in queryset:
            email_data = {
                "id": email.id,
                "subject": email.subject,
                "sender": {
                    "email": email.sender.email,
                    "name": email.sender.name,
                },
                "shortSummary": email.short_summary,
                "oneLineSummary": email.one_line_summary,
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
                    "hasRule": email.has_rule,
                    "ruleId": email.rule_id,
                },
                "hasAttachments": email.has_attachments,
                "attachments": [
                    {
                        "attachmentName": attachment.name,
                        "attachmentId": attachment.id_api,
                    }
                    for attachment in email.attachments.all()
                ],
                "sentDate": email.date.date() if email.date else None,
                "sentTime": email.date.strftime("%H:%M") if email.date else None,
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

        return Response(
            {"data": formatted_data},
            status=status.HTTP_200_OK,
        )
    except Email.DoesNotExist:
        return Response(
            {"error": "An email does not exist"}, status=status.HTTP_400_BAD_REQUEST
        )
    except TypeError:
        return Response(
            {"error": "IDs must be provided as a list with 25 to 100 elements"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON in request body"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        LOGGER.error(f"Error retrieving emails data from ids: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@subscription([FREE_PLAN])
def get_email_content(request: HttpRequest) -> Response:
    """
    Retrieves the HTML content of an email based on the provided email ID.

    Args:
        request (HttpRequest): The HTTP request object containing JSON data with the email ID.

    Returns:
        Response: HTTP response object containing either the HTML content of the email
                  or an error message with appropriate status code.
    """
    parameters: dict = json.loads(request.body)
    email_id = parameters.get("id")

    if not email_id:
        return Response(
            {"error": "id not provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        email = Email.objects.get(id=email_id)
        return Response({"content": email.html_content}, status=status.HTTP_200_OK)
    except Email.DoesNotExist:
        return Response(
            {"error": "email does not exist"}, status=status.HTTP_400_BAD_REQUEST
        )
    except TypeError:
        return Response(
            {"error": "id must be an integer"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON in request body"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        LOGGER.error(f"Error retrieving email content from id: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def validate_and_parse_parameters(request: HttpRequest) -> dict:
    """
    Validates and parses the request parameters.

    Args:
        request (HttpRequest): The HTTP request object containing JSON data with filtering parameters.

    Returns:
        dict: A dictionary containing:
            parameters (dict): The parsed parameters.
            result_per_page (int): The number of results per page.
            sort (str): The sort order.
    """
    parameters: dict = json.loads(request.body)
    result_per_page = parameters["resultPerPage"]
    sort = parameters.get("sort", "asc")

    if not 25 <= result_per_page <= 100:
        raise ValueError(
            "resultPerPage must be an integer between 25 and 100 inclusive"
        )

    return {
        "parameters": parameters,
        "result_per_page": result_per_page,
        "sort": sort,
    }


def construct_filters(user: User, parameters: dict) -> dict:
    """
    Constructs a dictionary of filters based on provided user, parameters, and category.

    Args:
        user (User): The user ID for whom the filters are being constructed.
        parameters (dict): A dictionary containing various filter parameters.

    Returns:
        dict: A dictionary containing the constructed filters.
    """
    filters = {"user": user}

    if parameters.get("advanced"):
        flags = [
            "scam",
            "spam",
            "newsletter",
            "notification",
            "meeting",
            "read",
        ]
        for flag in flags:
            if flag in parameters:
                filters[flag] = parameters[flag]

        if "category" in parameters:
            category_obj = Category.objects.get(name=parameters["category"])
            filters["category"] = category_obj
        if "archive" in parameters:
            filters["archive"] = parameters["archive"]
        if "hasAttachments" in parameters:
            filters["has_attachments"] = parameters["hasAttachments"]
        if "replyLater" in parameters:
            filters["answer_later"] = parameters["replyLater"]
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

    else:
        category_obj = Category.objects.get(name=parameters["category"])
        filters["category"] = category_obj
        subject = parameters["subject"]
        filters["subject__icontains"] = subject
        filters["sender__email__icontains"] = subject
        filters["sender__name__icontains"] = subject
        filters["cc_senders__email__icontains"] = subject
        filters["cc_senders__name__icontains"] = subject

    return filters


def get_sorted_queryset(
    filters: dict, sort: str, advanced: bool | None
) -> BaseManager[Email]:
    """
    Retrieves and sorts the queryset based on provided filters and sort order.

    Args:
        filters (dict): A dictionary containing the filter parameters for the queryset.
        sort (str): Sorting order ("asc" for ascending, "desc" for descending).
        advanced (bool): True for a AND query, default OR query.

    Returns:
        BaseManager[QuerySet]: A Django BaseManager for the Email model's QuerySet.
    """
    if advanced:
        queryset = Email.objects.filter(**filters)
    else:
        query = Q()
        for key, value in filters.items():
            if key != "user" and key != "category":
                query |= Q(**{key: value})

        queryset = Email.objects.filter(
            query, user=filters["user"], category=filters["category"]
        )

    rule_id_subquery = Rule.objects.filter(
        sender=OuterRef("sender"), user=filters["user"]
    ).values("id")[:1]
    queryset = queryset.annotate(
        has_rule=Exists(rule_id_subquery), rule_id=Subquery(rule_id_subquery)
    )
    if sort == "asc":
        queryset = queryset.order_by("-date")
    else:
        queryset = queryset.order_by("date")

    return queryset


def format_email_data(queryset: BaseManager[Email], result_per_page: int) -> tuple:
    """
    Formats email data from the provided queryset and collects email IDs.

    Args:
        queryset (BaseManager): A Django BaseManager containing Email objects.
        result_per_page (int): Number of email results per page.

    Returns:
        tuple: A tuple containing:
            email_count (int): Total number of emails in the queryset.
            formatted_data (defaultdict): Formatted email data grouped by category and priority.
            email_ids (list): List of email IDs from the queryset.
    """
    email_count = queryset.count()
    email_ids = []
    formatted_data = defaultdict(lambda: defaultdict(list))
    nb_email_treated = 0
    current_datetime_utc = timezone.now()

    for email in queryset:
        if email.read:
            delta_time = current_datetime_utc - email.read_date

            # archive emails older than 1 week
            if delta_time > timedelta(weeks=1):
                email.archive = True
                email.save()
                continue

        if nb_email_treated < result_per_page:
            email_data = {
                "id": email.id,
                "subject": email.subject,
                "sender": {
                    "email": email.sender.email,
                    "name": email.sender.name,
                },
                "shortSummary": email.short_summary,
                "oneLineSummary": email.one_line_summary,
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
                    "hasRule": email.has_rule,
                    "ruleId": email.rule_id,
                },
                "archive": email.archive,
                "hasAttachments": email.has_attachments,
                "attachments": [
                    {
                        "attachmentName": attachment.name,
                        "attachmentId": attachment.id_api,
                    }
                    for attachment in email.attachments.all()
                ],
                "sentDate": email.date.date() if email.date else None,
                "sentTime": email.date.strftime("%H:%M") if email.date else None,
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

    return email_count, formatted_data, email_ids


@api_view(["POST"])
@subscription([FREE_PLAN])
def get_user_emails(request: HttpRequest) -> Response:
    """
    Retrieves filtered user emails based on provided criteria and formats them grouped by category and priority.

    Args:
        request (HttpRequest): The HTTP request object containing JSON data with filtering parameters.

    JSON Body:
        Mandatory params:
            resultPerPage (int): Number of results per page (must be between 25 and 100)

        Optional filters:
            advanced (bool): True if specific filters have been used.
            sort (str): Sorting order ("asc" for ascending, "desc" for descending). Default is "asc".
            emailProvider (list[str]): List of email providers to filter by.
            subject (str): Keyword to filter by email subject.
            senderEmail (str): Keyword to filter by sender's email.
            senderName (str): Keyword to filter by sender's name.
            CCEmails (list[str]): List of email addresses to filter by CC recipients.
            CCNames (list[str]): List of names to filter by CC recipients.
            category (str): The category of emails to filter by.
            emailAddresses (list[str]): List of email addresses to filter by any associated email.
            archive (bool): Filter by archive status.
            replyLater (bool): Filter by reply later status.
            read (bool): Filter by read/unread status.
            sentDate (datetime): Filter by sent date (emails sent on or after this date).
            readDate (datetime): Filter by read date (emails read on or after this date).
            answer (list[str]): Filter by answer status.
            relevance (list[str]): Filter by relevance status.
            priority (list[str]): Filter by priority status.
            hasAttachments (bool): Filter by emails with attachments.
            spam (bool): Filter by spam status.
            scam (bool): Filter by scam status.
            newsletter (bool): Filter by newsletter status.
            notification (bool): Filter by notification status.
            meeting (bool): Filter by meeting status.

    Returns:
        Response: JSON response with the following structure:
            {
                "count": int,  # Total number of emails matching the filters.
                "data": dict,  # Filtered and formatted email data grouped by category and priority, limited to max results.
                "ids": list[int]  # List of email IDs matching the filters.
            }
    """
    try:
        user = request.user
        valid_data = validate_and_parse_parameters(request)
        parameters: dict = valid_data["parameters"]
        result_per_page = valid_data["result_per_page"]
        sort = valid_data["sort"]

        filters = construct_filters(user, parameters)
        queryset = get_sorted_queryset(filters, sort, parameters.get("advanced"))
        email_count, formatted_data, email_ids = format_email_data(
            queryset, result_per_page
        )

        return Response(
            {"count": email_count, "data": formatted_data, "ids": email_ids},
            status=status.HTTP_200_OK,
        )
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
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
    except Exception as e:
        LOGGER.error(f"Error filtering and sorting emails: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
