"""
Handles searching for rules in the Aomail database, filtering, sorting, and retrieving rules-related data.

Endpoints:
- ✅ get_user_rule_ids: Retrieves filtered and formatted user rule IDs based on specified criteria.
- ✅ get_rules_data: Retrieves formatted rules data for display.
"""

import json
import logging
from django.db.models import F, Q
from django.db.models.manager import BaseManager
from django.http import HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from aomail.constants import ALLOWED_PLANS
from aomail.models import Category, Rule, Sender
from aomail.utils.security import subscription
from django.contrib.auth.models import User
from aomail.email_providers.utils import camel_to_snake


LOGGER = logging.getLogger(__name__)


@api_view(["POST"])
@subscription(ALLOWED_PLANS)
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
            category_name = rule.category.name if rule.category else None
            category_id = rule.category.id if rule.category else None
            sender_name = rule.sender.name if rule.sender else None
            sender_email = rule.sender.email if rule.sender else None

            rule_data = {
                "id": rule.id,
                "priority": rule.priority,
                "categoryId": category_id,
                "category": category_name,
                "username": sender_name,
                "email": sender_email,
                "block": rule.block,
                "infoAI": rule.info_AI,
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
@subscription(ALLOWED_PLANS)
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
    sort = camel_to_snake(parameters.get("sort", "categoryName"))

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
        if "categoryName" in parameters:
            category_obj = Category.objects.get(
                name=parameters["categoryName"], user=user
            )
            filters["category"] = category_obj
        if "priority" in parameters:
            filters["priority__icontains"] = parameters["priority"]
        if "senderEmail" in parameters:
            sender_obj = Sender.objects.get(email=parameters["senderEmail"], user=user)
            filters["sender"] = sender_obj
        if "senderName" in parameters:
            sender_obj = Sender.objects.get(name=parameters["senderName"], user=user)
            filters["sender"] = sender_obj
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
            Q(category__name__icontains=search)
            | Q(sender__email__icontains=search)
            | Q(sender__name__icontains=search)
            | Q(priority__icontains=search)
        )
        queryset = Rule.objects.filter(
            query,
            user=filters["user"],
        )

    if order == "asc":
        queryset = queryset.order_by(F(sort_maping[sort]).asc())
    else:
        queryset = queryset.order_by(F(sort_maping[sort]).desc())

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
