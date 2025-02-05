"""
Handles searching for rules in the Aomail database, filtering, sorting, and retrieving rules-related data.

Endpoints:
- ✅ get_user_rule_ids: Retrieves filtered and formatted user rule IDs based on specified criteria.
- ✅ get_rules_data: Retrieves formatted rules data for display.

⚠️This module is deprecated and under refactoring
"""

import json
import logging
from django.db.models import F, Q
from django.db.models.manager import BaseManager
from django.http import HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from aomail.constants import ALLOW_ALL
from aomail.models import Category, Rule, Sender
from aomail.utils.security import subscription
from django.contrib.auth.models import User
from aomail.email_providers.utils import camel_to_snake


LOGGER = logging.getLogger(__name__)


@api_view(["POST"])
@subscription(ALLOW_ALL)
def get_rules_data(request: HttpRequest) -> Response:
    """
    Retrieves detailed data for multiple rules based on provided rule IDs.

    Args:
        request (HttpRequest): The HTTP request object containing JSON data with rule IDs.

    JSON Body:
        ids (list): A list of rule IDs (integers) for which to retrieve data, limited to between 0 and 100 elements.

    Returns:
        Response: HTTP response object with a status and either:
            - 'rulesData' containing a list of dictionaries with rule details for each ID.
            - An 'error' message in case of invalid input or retrieval issues.
    """
    try:
        user = request.user
        parameters: dict = json.loads(request.body)
        ids = parameters.get("ids")

        if not (0 <= len(ids) <= 100):
            return Response(
                {"error": "IDs must be provided as a list with 0 to 100 elements"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        formatted_data = []

        for id in ids:
            rule = Rule.objects.get(id=id, user=user)

            rule_data = {
                "id": rule.id,
                "logicalOperator": rule.logical_operator,
                "domains": rule.domains,
                "senderEmails": rule.sender_emails,
                "hasAttachements": rule.has_attachements,
                "categories": rule.categories,
                "priorities": rule.priorities,
                "answers": rule.answers,
                "relevances": rule.relevances,
                "flags": rule.flags,
                "emailDealWith": rule.email_deal_with,
                "actionTransferRecipients": rule.action_transfer_recipients,
                "actionSetFlags": rule.action_set_flags,
                "actionMarkAs": rule.action_mark_as,
                "actionDelete": rule.action_delete,
                "actionSetCategory": (
                    rule.action_set_category.name if rule.action_set_category else None
                ),
                "actionSetPriority": rule.action_set_priority,
                "actionSetRelevance": rule.action_set_relevance,
                "actionSetAnswer": rule.action_set_answer,
                "actionReplyPrompt": rule.action_reply_prompt,
                "actionReplyRecipients": rule.action_reply_recipients,
            }
            formatted_data.append(rule_data)

        return Response(
            {"rulesData": formatted_data},
            status=status.HTTP_200_OK,
        )
    except Rule.DoesNotExist:
        return Response(
            {"error": "A Rule does not exist"}, status=status.HTTP_400_BAD_REQUEST
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
        LOGGER.error(f"Error retrieving rule data: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@subscription(ALLOW_ALL)
def get_user_rule_ids(request: HttpRequest) -> Response:
    """
    Retrieves rules associated with the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing JSON data with filtering parameters.

    JSON Body:
        Optional filters:
            advanced (bool): True if specific filters have been used.
            search (str): Search query for a general search without filters.
            sort (str): Sorting method (e.g., categoryName (default), senderEmail, priority, senderName).
            order (str): Sorting order ("asc" for ascending, "desc" for descending). Default is "asc".
            block (bool): Filter by whether the rule blocks the sender.
            categoryName (str): Filter by the name of the category associated with the rule.
            priority (str): Filter by the rule's priority level.
            senderName (str): Filter by the sender's name.
            senderEmail (str): Filter by the sender's email address.


    Returns:
        Response: JSON response with the following structure:
            {
                "count": int,  # Total number of rules matching the filters.
                "ids": list[int],  # List of rule IDs matching the filters.
                "total": int  # Total number of rules associated with the user.
            }
    """
    try:
        user = request.user
        valid_data = validate_and_parse_parameters(request)
        parameters: dict = valid_data["parameters"]
        sort = valid_data["sort"]
        order = valid_data["order"]

        filters = construct_filters(user, parameters)
        queryset = get_sorted_queryset(
            filters,
            sort,
            order,
            parameters.get("search", ""),
            parameters.get("advanced"),
        )

        total = Rule.objects.filter(user=user).count()
        count, ids = format_rules_data(queryset)

        return Response(
            {
                "count": count,
                "ids": ids,
                "total": total,
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        LOGGER.error(f"An unexpected error occurred: {str(e)}")
        return Response(
            {"error": "Internal Server Error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def validate_and_parse_parameters(request: HttpRequest) -> dict:
    """
    Validates and parses the request parameters.

    Args:
        request (HttpRequest): The HTTP request object containing JSON data with filtering parameters.

    Returns:
        dict: A dictionary containing validated parameters, sort field, and order.
    """
    parameters: dict = json.loads(request.body)

    # Validate order
    order = parameters.get("order", "asc").lower()
    if order not in ["asc", "desc"]:
        order = "asc"

    # Convert camelCase to snake_case and validate sort field
    sort = camel_to_snake(parameters.get("sort", "domains"))
    valid_sort_fields = [
        "domains",
        "sender_emails",
        "categories",
        "priorities",
        "answers",
        "relevances",
        "flags",
        "email_deal_with",
        "has_attachements",
        "logical_operator",
    ]
    if sort not in valid_sort_fields:
        sort = "domains"

    return {"parameters": parameters, "sort": sort, "order": order}


def construct_filters(user: User, parameters: dict) -> dict:
    """
    Constructs a dictionary of filters based on provided parameters.

    Args:
        user (User): The user object for whom the filters are being constructed.
        parameters (dict): A dictionary containing various filter parameters.

    Returns:
        dict: A dictionary containing the constructed filters.
    """
    filters = {"user": user}

    if parameters.get("advanced"):
        # Email Triggers
        if "domains" in parameters and parameters["domains"]:
            filters["domains__contains"] = parameters["domains"]
        if "senderEmails" in parameters and parameters["senderEmails"]:
            filters["sender_emails__contains"] = parameters["senderEmails"]
        if "hasAttachments" in parameters:
            filters["has_attachements"] = parameters["hasAttachments"]

        # AI Processing Triggers
        if "categories" in parameters and parameters["categories"]:
            filters["categories__contains"] = parameters["categories"]
        if "priorities" in parameters and parameters["priorities"]:
            filters["priorities__contains"] = parameters["priorities"]
        if "answers" in parameters and parameters["answers"]:
            filters["answers__contains"] = parameters["answers"]
        if "relevance" in parameters and parameters["relevance"]:
            filters["relevances__contains"] = parameters["relevance"]
        if "flags" in parameters and parameters["flags"]:
            filters["flags__contains"] = parameters["flags"]
        if "emailDealWith" in parameters and parameters["emailDealWith"]:
            filters["email_deal_with__icontains"] = parameters["emailDealWith"]

        # Logical Operator
        if "logicalOperator" in parameters:
            filters["logical_operator"] = parameters["logicalOperator"]

    return filters


def get_sorted_queryset(
    filters: dict, sort: str, order: str, search: str, advanced: bool | None
) -> BaseManager[Rule]:
    """
    Retrieves and sorts the queryset based on provided filters and sort order.

    Args:
        filters (dict): A dictionary containing the filter parameters for the queryset.
        sort (str): Field to sort by (e.g., domains, sender_emails, etc.).
        order (str): Sorting order ("asc" for ascending, "desc" for descending).
        search (str): Search query for a general search without filters.
        advanced (bool): True for an AND query, default is an OR query.

    Returns:
        BaseManager[QuerySet]: A Django BaseManager for the Rule model's QuerySet.
    """
    # Define valid sort fields and their mappings
    sort_mapping = {
        "domains": "domains",
        "senderEmails": "sender_emails",
        "categories": "categories",
        "priorities": "priorities",
        "answers": "answers",
        "relevances": "relevances",
        "flags": "flags",
        "emailDealWith": "email_deal_with",
        "hasAttachements": "has_attachements",
        "logicalOperator": "logical_operator",
    }

    # Use default sort if provided sort field is invalid
    sort_field = sort_mapping.get(sort, "domains")

    if advanced:
        # Create Q objects for each filter
        q_objects = Q()
        for field, value in filters.items():
            if field != "user":  # Skip the user filter as it's always applied
                q_objects &= Q(**{field: value})

        # Apply user filter and Q objects
        queryset = Rule.objects.filter(user=filters["user"]).filter(q_objects)
    else:
        # Update search query to match all available trigger fields
        query = Q()
        if search:
            query = (
                Q(domains__icontains=search)
                | Q(sender_emails__icontains=search)
                | Q(categories__icontains=search)
                | Q(priorities__icontains=search)
                | Q(answers__icontains=search)
                | Q(relevances__icontains=search)
                | Q(flags__icontains=search)
                | Q(email_deal_with__icontains=search)
            )
        queryset = Rule.objects.filter(query & Q(user=filters["user"]))

    # Apply sorting
    if order == "desc":
        sort_field = f"-{sort_field}"

    return queryset.order_by(sort_field)


def format_rules_data(queryset: BaseManager[Rule]) -> tuple:
    """
    Formats rule data from the provided queryset and collects rule IDs.

    Args:
        queryset (BaseManager): A Django BaseManager containing Rule objects.

    Returns:
        tuple: A tuple containing:
            rule_count (int): Total number of rules in the queryset.
            rule_ids (list): List of rule IDs from the queryset.
    """
    count = queryset.count()
    ids = list(queryset.values_list("id", flat=True))
    return count, ids
