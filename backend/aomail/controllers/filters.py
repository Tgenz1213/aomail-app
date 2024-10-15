"""
Handles filters operations, returns results to frontend, and saves to database.

Endpoints:
- ✅ get_user_filter: Retrieve filter of the user for a category
- ✅ update_filter: Update an existing filter.
- ✅ delete_filter: Delete a filter.
- ✅ create_filter: Create a new filter.
"""

import json
import logging
from django.http import HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from aomail.utils.security import subscription
from aomail.constants import ALLOWED_PLANS
from aomail.models import Filter, Category
from aomail.utils.serializers import (
    FilterSerializer,
)

######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


@api_view(["POST"])
@subscription([ALLOWED_PLANS])
def get_user_filter(request: HttpRequest) -> Response:
    """
    Retrieve filters of the user for a category.

    Args:
        request (HttpRequest): The HTTP request object containing the following query parameter:
            category (string): The name of the Category to retrieve filters for.

    Returns:
        Response: JSON response containing user's filters or an error message.
    """
    user = request.user
    data: dict = json.loads(request.body)
    category_name = data.get("category")

    if not category_name:
        return Response(
            {"error": "No category name provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        category = Category.objects.get(name=category_name, user=request.user)
        data["category"] = category.id
    except Category.DoesNotExist:
        return Response(
            {"error": "Category does not exist or does not belong to the user"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    filters = Filter.objects.filter(user=user, category=category)
    serializer = FilterSerializer(filters, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@subscription([ALLOWED_PLANS])
def create_filter(request: HttpRequest) -> Response:
    """
    Create a new filter for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the filter data to create.

    Returns:
        Response: JSON response with the created filter data on success,
                  or error messages on failure.
    """
    data: dict = json.loads(request.body)
    data["user"] = request.user.id
    filter_name = data.get("name")
    category_name = data.get("category")

    if not filter_name:
        return Response(
            {"error": "No filter name provided"}, status=status.HTTP_400_BAD_REQUEST
        )
    if not category_name:
        return Response(
            {"error": "No category name provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        category = Category.objects.get(name=category_name, user=request.user)
        data["category"] = category.id
    except Category.DoesNotExist:
        return Response(
            {"error": "Category does not exist or does not belong to the user"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = FilterSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["PUT"])
@subscription([ALLOWED_PLANS])
def update_filter(request: HttpRequest) -> Response:
    """
    Update an existing filter for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the filter data to update.

    Returns:
        Response: JSON response containing the updated filter data or error messages.
    """
    data: dict = json.loads(request.body)
    current_name = data.get("filterName")

    if not current_name:
        return Response(
            {"error": "No filter name provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        filter = Filter.objects.get(name=current_name, user=request.user)
    except Filter.DoesNotExist:
        return Response({"error": "Filter not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = FilterSerializer(filter, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["DELETE"])
@subscription([ALLOWED_PLANS])
def delete_filter(request: HttpRequest) -> Response:
    """
    Delete a filter associated with the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameter in the body:
            filter_id (int): The ID of the filter to be deleted.

    Returns:
        Response: JSON response indicating success or failure of deleting the filter.
    """
    data: dict = json.loads(request.body)
    current_name = data.get("filterName")

    if not current_name:
        return Response(
            {"error": "No filter name provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        filter = Filter.objects.get(name=current_name, user=request.user)
    except Filter.DoesNotExist:
        return Response(
            {"error": "Filter not found"}, status=status.HTTP_400_BAD_REQUEST
        )

    filter.delete()
    return Response(
        {"message": "Filter deleted successfully"}, status=status.HTTP_200_OK
    )
