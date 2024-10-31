"""
Handles searching for labels in the Aomail database, filtering, sorting, and retrieving label-related data.

Endpoints:
- ✅ get_user_label_ids: Retrieves filtered and formatted user label IDs based on specified criteria.
- ✅ get_labels_data: Retrieves formatted label data for display.
- ✅ get_label_pdf: Returns the data of the shipping label PDF.
"""

import os
import json
import logging
from json.decoder import JSONDecodeError
from django.db.models import F, Q
from django.db.models.manager import BaseManager
from django.http import FileResponse, HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from aomail.constants import ALLOWED_PLANS, MEDIA_ROOT
from aomail.models import Label
from aomail.utils.security import subscription
from django.contrib.auth.models import User
from aomail.email_providers.utils import camel_to_snake


LOGGER = logging.getLogger(__name__)


@api_view(["POST"])
@subscription(ALLOWED_PLANS)
def get_label_pdf(request: HttpRequest) -> Response:
    """
    Retrieves a PDF file for a given label ID and returns it as a binary response.

    Args:
        request (HttpRequest): The HTTP request object containing JSON data with the label ID.

    JSON Body:
        id (str): The ID of the label for which to retrieve the PDF.

    Returns:
        Response: A binary response with the PDF data or an error message.
    """
    try:
        user = request.user
        parameters: dict = json.loads(request.body)
        label_id = parameters.get("id")

        if not label_id:
            return Response(
                {"error": "No label ID provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        label = Label.objects.get(id=label_id, user=user)
        pdf_file_path = os.path.join(MEDIA_ROOT, "labels", f"{label.label_name}")

        if not os.path.exists(pdf_file_path):
            return Response(
                {"error": "PDF file not found for the provided label."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return FileResponse(open(pdf_file_path, "rb"), content_type="application/pdf")

    except Label.DoesNotExist:
        return Response(
            {
                "error": "The provided label ID does not belong to the user or does not exist."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        LOGGER.error(f"Error retrieving PDF for label: {str(e)}")
        return Response(
            {"error": "An internal server error occurred. Please try again later."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@subscription(ALLOWED_PLANS)
def get_labels_data(request: HttpRequest) -> Response:
    """
    Retrieves detailed data for multiple labels based on provided label IDs.

    Args:
        request (HttpRequest): The HTTP request object containing JSON data with label IDs.

    JSON Body:
        ids (list): A list of label IDs for which to retrieve data.

    Returns:
        Response: HTTP response object containing a list of formatted label data or an error message.
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
            label = Label.objects.get(id=id, user=user)
            label_data = {
                "id": label.id,
                "itemName": label.item_name,
                "carrier": label.carrier,
                "platform": label.platform,
                "postageDeadlineDate": label.postage_deadline.date(),
                "postageDeadlineTime": label.postage_deadline.strftime("%H:%M"),
            }
            formatted_data.append(label_data)

        return Response(
            {"labelsData": formatted_data},
            status=status.HTTP_200_OK,
        )
    except Label.DoesNotExist:
        return Response(
            {"error": "A Label does not exist"}, status=status.HTTP_400_BAD_REQUEST
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
        LOGGER.error(f"Error retrieving label data: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@subscription(ALLOWED_PLANS)
def get_user_label_ids(request: HttpRequest) -> Response:
    """
    Retrieve filtered user label IDs based on provided criteria and format them grouped by category and priority.

    Args:
        request (HttpRequest): The HTTP request object containing JSON data with filtering parameters.

    JSON Body:
        Optional filters:
            advanced (bool): True if specific filters have been used.
            search (str): Search query for a general search without filters.
            sort (str): Sorting method (e.g., platform, itemName, carrier (default), postageDeadline).
            order (str): Sorting order ("asc" for ascending, "desc" for descending). Default is "asc".
            platform (str): Search query for the platform field.
            itemName (str): Search query for the item name field.
            carrier (str): Search query for the carrier field.
            postageDeadline (datetime): Search query for the postage deadline field.

    Returns:
        Response: JSON response with the following structure:
            {
                "count": int,  # Total number of labels matching the filters.
                "ids": list[int],  # List of label IDs matching the filters.
                "total": int  # Total number of labels associated with the user.
            }
    """
    try:
        user = request.user
        valid_data = validate_and_parse_parameters(request)
        parameters: dict = valid_data["parameters"]
        sort = valid_data["sort"]
        order = valid_data["order"]

        filters = construct_filters(user, parameters)
        queryset = get_sorted_queryset(filters, sort, order, parameters.get("advanced"))
        total = Label.objects.filter(user=user).count()
        count, ids = format_label_data(queryset)

        return Response(
            {
                "count": count,
                "ids": ids,
                "total": total,
            },
            status=status.HTTP_200_OK,
        )

    except JSONDecodeError as e:
        return Response(
            {"error": "Invalid JSON format. Please check the request body."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error: {str(e)}")
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
    order = parameters.get("order", "asc")
    sort = camel_to_snake(parameters.get("sort", "carrier"))

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
        if "postageDeadline" in parameters:
            filters["postage_deadline__lte"] = parameters["postageDeadline"]
        if "platform" in parameters:
            filters["platform__icontains"] = parameters["platform"]
        if "itemName" in parameters:
            filters["item_name__icontains"] = parameters["itemName"]
        if "carrier" in parameters:
            filters["carrier__icontains"] = parameters["carrier"]
    else:
        search = parameters.get("search")
        if search:
            filters["platform__icontains"] = search
            filters["item_name__icontains"] = search
            filters["carrier__icontains"] = search

    return filters


def get_sorted_queryset(
    filters: dict, sort: str, order: str, advanced: bool | None
) -> BaseManager[Label]:
    """
    Retrieves and sorts the queryset based on provided filters and sort order.

    Args:
        filters (dict): A dictionary containing the filter parameters for the queryset.
        sort (str): Sorting method (platform, item_name, carrier, postage_deadline).
        order (str): Sorting order ("asc" for ascending, "desc" for descending). Default is "asc".
        advanced (bool): True for an AND query, default is an OR query.

    Returns:
        BaseManager[QuerySet]: A Django BaseManager for the Label model's QuerySet.
    """
    if advanced:
        queryset = Label.objects.filter(**filters)
    else:
        query = Q()
        for key, value in filters.items():
            if key != "user":
                query |= Q(**{key: value})

        queryset = Label.objects.filter(query, user=filters["user"])

    if order == "asc":
        queryset = queryset.order_by(F(sort).asc())
    else:
        queryset = queryset.order_by(F(sort).desc())

    return queryset


def format_label_data(queryset: BaseManager[Label]) -> tuple:
    """
    Formats label data from the provided queryset and collects label IDs.

    Args:
        queryset (BaseManager): A Django BaseManager containing Label objects.

    Returns:
        tuple: A tuple containing:
            label_count (int): Total number of labels in the queryset.
            label_ids (list): List of label IDs from the queryset.
    """
    count = queryset.count()
    ids = list(queryset.values_list("id", flat=True))
    return count, ids
