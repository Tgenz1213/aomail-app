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
from aomail.constants import FREE_PLAN
from aomail.models import Filter, SocialAPI, Category
from aomail.utils.serializers import (
    FilterListSerializer,
    FilterCreateSerializer,
    FilterUpdateSerializer,
)

######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


@api_view(["GET"])
@subscription([FREE_PLAN])
def get_user_filter(request: HttpRequest) -> Response:
    """
    Retrieve filters of the user for a category.

    Args:
        request (HttpRequest): The HTTP request object containing the following query parameter:
            category_id (int): The ID of the Category to retrieve filters for.

    Returns:
        Response: JSON response containing user's filters or an error message.
    """
    user = request.user
    category_id = request.GET.get("category_id")

    if not category_id:
        return Response(
            {"error": "category_id is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        category = Category.objects.get(id=category_id, user=user)
    except Category.DoesNotExist:
        return Response(
            {"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND
        )

    filters = Filter.objects.filter(user=user, category=category)
    serializer = FilterListSerializer(filters, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@subscription([FREE_PLAN])
def create_filter(request: HttpRequest) -> Response:
    """
    Create a new filter for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the filter data to create.

    Returns:
        Response: JSON response with the created filter data on success,
                  or error messages on failure.
    """
    data = json.loads(request.body)
    data["user"] = request.user.id

    serializer = FilterCreateSerializer(data=data, context={"request": request})
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["PUT"])
@subscription([FREE_PLAN])
def update_filter(request: HttpRequest) -> Response:
    """
    Update an existing filter for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the filter data to update.

    Returns:
        Response: JSON response containing the updated filter data or error messages.
    """
    data = json.loads(request.body)
    filter_id = data.get("id")

    if not filter_id:
        return Response(
            {"error": "No filter ID provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        filter_obj = Filter.objects.get(id=filter_id, user=request.user)
    except Filter.DoesNotExist:
        return Response({"error": "Filter not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = FilterUpdateSerializer(
        filter_obj, data=data, partial=True, context={"request": request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["DELETE"])
@subscription([FREE_PLAN])
def delete_filter(request: HttpRequest) -> Response:
    """
    Delete a filter associated with the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameter in the body:
            filter_id (int): The ID of the filter to be deleted.

    Returns:
        Response: JSON response indicating success or failure of deleting the filter.
    """
    data = json.loads(request.body)
    filter_id = data.get("filter_id")

    if not filter_id:
        return Response(
            {"error": "No filter ID provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        filter_obj = Filter.objects.get(id=filter_id, user=request.user)
    except Filter.DoesNotExist:
        return Response({"error": "Filter not found"}, status=status.HTTP_404_NOT_FOUND)

    filter_obj.delete()
    return Response(
        {"message": "Filter deleted successfully"}, status=status.HTTP_200_OK
    )
