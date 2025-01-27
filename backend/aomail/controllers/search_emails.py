"""
Handles searching emails among Aomail database, filtering, sorting, and retrieving email content.

Endpoints:
- ✅ get_user_emails_ids: Retrieves filtered and formatted user emails ids grouped by category and priority.
- ✅ get_email_content: Retrieves HTML content of a specific email for display.
- ✅ get_emails_data: Retrieves formatted email data to be displayed.
"""

import json
import logging
from collections import defaultdict
from django.db.models import Exists, OuterRef, Q, Subquery
from django.db.models.manager import BaseManager
from django.http import HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from aomail.constants import ALLOW_ALL, ENCRYPTION_KEYS
from aomail.models import Category, SocialAPI, Email, Rule
from aomail.utils.security import subscription, decrypt_text
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
@subscription(ALLOW_ALL)
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

        if not (0 <= len(email_ids) <= 100):
            return Response(
                {"error": "IDs must be provided as a list with 0 to 100 elements"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        formatted_data = defaultdict(lambda: defaultdict(list))
        queryset = Email.objects.filter(id__in=email_ids, user=user)
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
                "providerId": email.provider_id,
                "shortSummary": decrypt_text(
                    ENCRYPTION_KEYS["Email"]["short_summary"], email.short_summary
                ),
                "oneLineSummary": decrypt_text(
                    ENCRYPTION_KEYS["Email"]["one_line_summary"], email.one_line_summary
                ),
                "cc": [
                    {"email": cc.email, "name": cc.name}
                    for cc in email.cc_senders.all()
                ],
                "bcc": [
                    {"email": bcc.email, "name": bcc.name}
                    for bcc in email.bcc_senders.all()
                ],
                "read": email.read,
                "answerLater": email.answer_later,
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
                "archive": email.archive,
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
            {"error": "IDs must be provided as a list with 0 to 100 elements"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON in request body"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        LOGGER.error(f"Error retrieving emails data from ids: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@subscription(ALLOW_ALL)
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
        email = Email.objects.get(user=request.user, id=email_id)
        decrypted_content = decrypt_text(
            ENCRYPTION_KEYS["Email"]["html_content"], email.html_content
        )
        return Response({"content": decrypted_content}, status=status.HTTP_200_OK)
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
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def validate_and_parse_parameters(request: HttpRequest) -> dict:
    """
    Validates and parses the request parameters.

    Args:
        request (HttpRequest): The HTTP request object containing JSON data with filtering parameters.

    Returns:
        dict: A dictionary containing:
            parameters (dict): The parsed parameters.
            sort (str): The sort order.
    """
    parameters: dict = json.loads(request.body)
    sort = parameters.get("sort", "asc")

    return {
        "parameters": parameters,
        "sort": sort,
    }


def construct_filters(user: User, parameters: dict) -> tuple[dict, Q]:
    """
    Constructs a dictionary of filters and a Q object for OR conditions based on provided user and parameters.

    Args:
        user (User): The user ID for whom the filters are being constructed.
        parameters (dict): A dictionary containing various filter parameters.

    Returns:
        tuple: A tuple containing:
            - dict: A dictionary containing the AND filters.
            - Q: A Q object containing the OR filters.
    """
    and_filters = {"user": user}
    or_filters = Q()
    or_filters_search = Q()

    if parameters.get("advanced"):
        if "priority" in parameters:
            priorities = parameters["priority"]
            and_filters["priority__in"] = priorities

        if "read" in parameters:
            if not parameters["read"]:
                and_filters["read"] = False

        flag_filter = Q()
        flags = ["scam", "spam", "newsletter", "notification", "meeting"]
        for flag in flags:
            if parameters.get(flag):
                flag_filter |= Q(**{flag: True})
        if flag_filter:
            or_filters |= flag_filter

        if "category" in parameters:
            category_obj = Category.objects.get(name=parameters["category"], user=user)
            and_filters["category"] = category_obj
        if "archive" in parameters:
            and_filters["archive"] = parameters["archive"]
        if "hasAttachments" in parameters:
            and_filters["has_attachments"] = parameters["hasAttachments"]
        if "replyLater" in parameters:
            and_filters["answer_later"] = parameters["replyLater"]
        if "emailProvider" in parameters:
            and_filters["email_provider__in"] = parameters["emailProvider"]
        if "subject" in parameters:
            and_filters["subject__icontains"] = parameters["subject"]
        if "senderEmail" in parameters:
            and_filters["sender__email__icontains"] = parameters["senderEmail"]
        if "senderName" in parameters:
            and_filters["sender__name__icontains"] = parameters["senderName"]
        if "sentDate" in parameters:
            and_filters["date__gte"] = parameters["sentDate"]
        if "readDate" in parameters:
            and_filters["read_date__gte"] = parameters["readDate"]
        if "answer" in parameters:
            and_filters["answer__in"] = parameters["answer"]
        if "relevance" in parameters:
            and_filters["relevance__in"] = parameters["relevance"]
        if "emailAddresses" in parameters:
            social_apis = SocialAPI.objects.filter(
                email__in=parameters["emailAddresses"], user=user
            )
            and_filters["social_api__in"] = social_apis
        if "CCEmails" in parameters:
            and_filters["cc_senders__email__in"] = parameters["CCEmails"]
        if "CCNames" in parameters:
            and_filters["cc_senders__name__in"] = parameters["CCNames"]
        if "search" in parameters:
            search = parameters.get("search", "")
            or_filters_search |= (
                Q(subject__icontains=search)
                | Q(sender__email__icontains=search)
                | Q(sender__name__icontains=search)
                | Q(cc_senders__email__icontains=search)
                | Q(cc_senders__name__icontains=search)
            )

    else:
        if "category" in parameters:
            category_obj = Category.objects.get(name=parameters["category"], user=user)
            and_filters["category"] = category_obj
        search = parameters.get("search", "")
        or_filters |= (
            Q(subject__icontains=search)
            | Q(sender__email__icontains=search)
            | Q(sender__name__icontains=search)
            | Q(cc_senders__email__icontains=search)
            | Q(cc_senders__name__icontains=search)
        )

    return and_filters, or_filters, or_filters_search


def get_sorted_queryset(
    and_filters: dict, or_filters: Q, or_filters_search: Q, sort: str, user: User
) -> BaseManager[Email]:
    queryset = Email.objects.filter(**and_filters)

    if or_filters:
        queryset = queryset.filter(or_filters, user=user)

    if or_filters_search:
        queryset = queryset.filter(or_filters_search, user=user)

    rule_id_subquery = Rule.objects.filter(
        sender=OuterRef("sender"), user=and_filters["user"]
    ).values("id")[:1]

    queryset = queryset.annotate(
        has_rule=Exists(rule_id_subquery), rule_id=Subquery(rule_id_subquery)
    )

    return queryset


def format_email_data(queryset: BaseManager[Email]) -> tuple:
    """
    Formats email data from the provided queryset and collects email IDs.

    Args:
        queryset (BaseManager): A Django BaseManager containing Email objects.
        result_per_page (int): Number of email results per page.

    Returns:
        tuple: A tuple containing:
            email_count (int): Total number of emails in the queryset.
            email_ids (list): List of email IDs from the queryset.
    """
    priority_order = ["important", "informative", "useless"]
    email_ids = []

    for priority in priority_order:
        priority_unread_ids = list(
            queryset.filter(priority=priority, read=False)
            .order_by("-date")
            .values_list("id", flat=True)
        )
        email_ids.extend(priority_unread_ids)

    for priority in priority_order:
        priority_read_ids = list(
            queryset.filter(priority=priority, read=True)
            .order_by("-date")
            .values_list("id", flat=True)
        )
        email_ids.extend(priority_read_ids)

    email_count = len(email_ids)
    return email_count, email_ids


@api_view(["POST"])
@subscription(ALLOW_ALL)
def get_user_emails_ids(request: HttpRequest) -> Response:
    """
    Retrieves filtered user emails ids based on provided criteria and formats them grouped by category and priority.

    Args:
        request (HttpRequest): The HTTP request object containing JSON data with filtering parameters.

    JSON Body:
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
                "ids": list[int]  # List of email IDs matching the filters.
            }
    """
    try:
        user = request.user
        valid_data = validate_and_parse_parameters(request)
        parameters: dict = valid_data["parameters"]
        sort = valid_data["sort"]

        and_filters, or_filters, or_filters_search = construct_filters(user, parameters)
        queryset = get_sorted_queryset(
            and_filters, or_filters, or_filters_search, sort, user
        )
        email_count, email_ids = format_email_data(queryset)

        return Response(
            {"count": email_count, "ids": email_ids},
            status=status.HTTP_200_OK,
        )
    except ValueError as e:
        return Response(
            {"error": "Internal server error"}, status=status.HTTP_400_BAD_REQUEST
        )
    except KeyError:
        return Response(
            {"error": "Invalid JSON keys in request body"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        LOGGER.error(f"Error filtering and sorting emails: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@subscription(ALLOW_ALL)
def get_email_counts(request: HttpRequest) -> Response:
    """
    Retrieves the count of unread emails by priority and the number of read emails for the authenticated user,
    based on provided filtering criteria.

    Args:
        request (HttpRequest): The HTTP request object containing JSON data with filtering parameters.

    JSON Body:
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
        Response: JSON response containing the counts and lists of email IDs.
            {
                "useless_count": int,
                "useless_ids": list[int],
                "important_count": int,
                "important_ids": list[int],
                "informative_count": int,
                "informative_ids": list[int],
                "read_count": int,
                "read_ids": list[int],
            }
    """
    try:
        user = request.user
        valid_data = validate_and_parse_parameters(request)
        parameters: dict = valid_data["parameters"]

        and_filters, or_filters, or_filters_search = construct_filters(user, parameters)

        queryset = Email.objects.filter(user=user)

        if and_filters:
            queryset = queryset.filter(**and_filters)
        if or_filters:
            queryset = queryset.filter(or_filters)
        if or_filters_search:
            queryset = queryset.filter(or_filters_search)

        # Fetch email querysets for each category
        useless_emails = queryset.filter(priority="useless", read=False)
        important_emails = queryset.filter(priority="important", read=False)
        informative_emails = queryset.filter(priority="informative", read=False)
        read_emails = queryset.filter(read=True, archive=False)

        counts = {
            "useless_count": useless_emails.count(),
            "useless_ids": list(useless_emails.values_list('id', flat=True)),
            "important_count": important_emails.count(),
            "important_ids": list(important_emails.values_list('id', flat=True)),
            "informative_count": informative_emails.count(),
            "informative_ids": list(informative_emails.values_list('id', flat=True)),
            "read_count": read_emails.count(),
            "read_ids": list(read_emails.values_list('id', flat=True)),
        }

        return Response(counts, status=status.HTTP_200_OK)

    except ValueError as e:
        LOGGER.error(f"ValueError in get_email_counts: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except KeyError:
        LOGGER.error("KeyError in get_email_counts: Missing keys in request data")
        return Response(
            {"error": "Invalid JSON keys in request body"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error in get_email_counts: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
