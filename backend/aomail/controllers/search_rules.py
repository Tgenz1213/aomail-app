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
                "logical_operator": rule.logical_operator,
                "domains": rule.domains,
                "sender_emails": rule.sender_emails,
                "hasAttachements": rule.has_attachements,
                "categories": rule.categories,
                "priorities": rule.priorities,
                "answers": rule.answers,
                "relevances": rule.relevances,
                "flags": rule.flags,
                "emailDealWith": rule.email_deal_with,
                "actionTransferRecipients": rule.action_transfer_recipients,
                "actionSetTags": rule.action_set_tags,
                "actionMarkAs": rule.action_mark_as,
                "actionDelete": rule.action_delete,
                "actionSetCategory": rule.action_set_category,
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
        dict: A dictionary containing:
            parameters (dict): The parsed parameters.
            sort (str): The sort order.
    """
    parameters: dict = json.loads(request.body)
    order = parameters.get("order", "asc")
    sort = camel_to_snake(parameters.get("sort", "domains"))

    return {"parameters": parameters, "sort": sort, "order": order}


def construct_filters(user: User, parameters: dict) -> dict:
    """
    Constructs a dictionary of filters based on provided user, parameters, and category.

    Args:
        user (User): The user object for whom the filters are being constructed.
        parameters (dict): A dictionary containing various filter parameters.

    Returns:
        dict: A dictionary containing the constructed filters.
    """
    filters = {"user": user}

    if parameters.get("advanced"):
        # TODO: refactor this
        if "categoryName" in parameters:
            category_obj = Category.objects.filter(
                name=parameters["categoryName"], user=user
            )
            if category_obj:
                filters["category"] = category_obj.first()
        if "priority" in parameters:
            filters["priority__icontains"] = parameters["priority"]
        if "senderEmail" in parameters:
            sender_obj = Sender.objects.filter(email=parameters["senderEmail"])
            if sender_obj:
                filters["sender"] = sender_obj.first()
        if "senderName" in parameters:
            sender_obj = Sender.objects.filter(name=parameters["senderName"])
            if sender_obj:
                filters["sender"] = sender_obj.first()
        if "block" in parameters:
            filters["block"] = parameters["block"]

    return filters


def get_sorted_queryset(
    filters: dict, sort: str, order: str, search: str, advanced: bool | None
) -> BaseManager[Rule]:
    """
    Retrieves and sorts the queryset based on provided filters and sort order.

    Args:
        filters (dict): A dictionary containing the filter parameters for the queryset.
        sort (str): Sorting method (e.g., categoryName (default), senderEmail, priority, senderName).
        order (str): Sorting order ("asc" for ascending, "desc" for descending). Default is "asc".
        search (str): Search query for a general search without filters.
        advanced (bool): True for an AND query, default is an OR query.

    Returns:
        BaseManager[QuerySet]: A Django BaseManager for the Rule model's QuerySet.
    """
    sort_maping = {
        "category_name": "category__name",
        "sender_email": "sender__email",
        "sender_name": "sender__name",
        "priority": "priority",
    }
    if advanced:
        queryset = Rule.objects.filter(**filters)
    else:
        query = (
            Q(domains__icontains=search)
            | Q(sender_emails__icontains=search)
            | Q(categories__icontains=search)
            | Q(priorities__icontains=search)
            | Q(answers__icontains=search)
            | Q(relevances__icontains=search)
            | Q(flags__icontains=search)
        )
        queryset = Rule.objects.filter(
            query,
            user=filters["user"],
        )

    # if order == "asc":
    #     queryset = queryset.order_by(F(sort_maping[sort]).asc())
    # else:
    #     queryset = queryset.order_by(F(sort_maping[sort]).desc())

    return queryset


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
