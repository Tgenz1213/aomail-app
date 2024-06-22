"""
Handles category operations, returns results to frontend, and saves to database.

Endpoints available:
- get_user_categories: Retrieve categories associated with the authenticated user.
- update_category: Update an existing category for the authenticated user.
- delete_category: Delete a category associated with the authenticated user.
- get_rules_linked: Retrieve the number of rules linked to a specified category for the authenticated user.
- create_category: Create a new category for the authenticated user.
- get_category_id: Retrieve the ID of a category based on its name for the authenticated user.


TODO:
- (ANTI scraping/reverse engineering): Add a system that counts the number of 400 erros per user and send warning + ban
"""

import json
import logging
from django.http import HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MailAssistant.utils.security import subscription
from MailAssistant.constants import (
    DEFAULT_CATEGORY,
    FREE_PLAN,
)
from MailAssistant.models import (
    Category,
    Rule,
)
from MailAssistant.utils.serializers import (
    CategoryNameSerializer,
    NewCategorySerializer,
)


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


@api_view(["GET"])
@subscription([FREE_PLAN])
def get_user_categories(request: HttpRequest) -> Response:
    """
    Retrieve categories associated with the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: JSON response containing user's categories or an error message.
    """
    user = request.user
    categories = Category.objects.filter(user=user)
    serializer = CategoryNameSerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@subscription([FREE_PLAN])
def update_category(request: HttpRequest) -> Response:
    """
    Update an existing category for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameters in the body:
            categoryName (str): The current name of the category to update.
            description (str): The updated description for the category.

    Returns:
        Response: JSON response containing the updated category data or error messages.
    """
    parameters: dict = json.loads(request.body)
    current_name = parameters.get("categoryName")
    description = parameters.get("description")

    if not current_name:
        return Response(
            {"error": "No category name provided"}, status=status.HTTP_400_BAD_REQUEST
        )
    if not description:
        return Response(
            {"error": "No category description provided"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if current_name == DEFAULT_CATEGORY:
        return Response(
            {"error": f"Cannot modify default category: {DEFAULT_CATEGORY}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if len(current_name) > 50:
        return Response(
            {"error": "Category name length exceeds 50 characters"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if len(description) > 300:
        return Response(
            {"error": "Description length exceeds 300 characters"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        category = Category.objects.get(name=current_name, user=request.user)
    except Category.DoesNotExist:
        return Response(
            {"error": "Category not found"}, status=status.HTTP_400_BAD_REQUEST
        )

    serializer = CategoryNameSerializer(category, data=parameters)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["DELETE"])
@subscription([FREE_PLAN])
def delete_category(request: HttpRequest) -> Response:
    """
    Delete a category associated with the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameter in the body:
            categoryName (str): The name of the category to be deleted.

    Returns:
        Response: JSON response indicating success or failure of deleting the category.
                      Returns an error if the category name is not provided, if attempting to delete the default category,
                      or if the category is not found.
    """
    parameters: dict = json.loads(request.body)
    current_name = parameters.get("categoryName")

    if not current_name:
        return Response(
            {"error": "No category name provided"}, status=status.HTTP_400_BAD_REQUEST
        )
    if current_name == DEFAULT_CATEGORY:
        return Response(
            {"error": f"Cannot delete: {DEFAULT_CATEGORY}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        category = Category.objects.get(name=current_name, user=request.user)
    except Category.DoesNotExist:
        return Response(
            {"error": "Category not found"}, status=status.HTTP_400_BAD_REQUEST
        )

    category.delete()

    return Response(
        {"message": "Category deleted successfully"}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
@subscription([FREE_PLAN])
def get_rules_linked(request: HttpRequest) -> Response:
    """
    Retrieves the number of rules linked to a specified category for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameter in the body:
            categoryName (str): The name of the category to retrieve linked rules for.

    Returns:
        Response: JSON response indicating the number of rules linked to the category.
                      Returns an error if the category name is not provided or if the category is not found.
    """
    parameters: dict = json.loads(request.body)
    current_name = parameters.get("categoryName")
    user = request.user

    if not current_name:
        return Response(
            {"error": "No category name provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        category = Category.objects.get(name=current_name, user=user)
    except Category.DoesNotExist:
        return Response(
            {"error": "Category not found"}, status=status.HTTP_400_BAD_REQUEST
        )
    rules = Rule.objects.filter(category=category, user=user)

    return Response({"nb_rules": len(rules)}, status=status.HTTP_200_OK)


@api_view(["POST"])
@subscription([FREE_PLAN])
def create_category(request: HttpRequest) -> Response:
    """
    Create a new category for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the following JSON data:
            name (str): The name of the category to create.
            description (str): The description of the category (up to 300 characters).

    Returns:
        Response: JSON response with the created category data on success,
                      or error messages on failure (e.g., invalid input, existing category).
    """
    data: dict = json.loads(request.body)
    data["user"] = request.user.id
    name = data.get("name")
    description = data.get("description")

    if not name:
        return Response(
            {"error": "No category name provided"}, status=status.HTTP_400_BAD_REQUEST
        )
    if not description:
        return Response(
            {"error": "No category description provided"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if name == DEFAULT_CATEGORY:
        return Response(
            {"error": f"Cannot create category with name: {DEFAULT_CATEGORY}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if len(name) > 50:
        return Response(
            {"error": "Category name length must be 50 characters or fewer"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if len(description) > 300:
        return Response(
            {"error": "Description length must be 300 characters or fewer"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    existing_category = Category.objects.filter(user=request.user, name=name).exists()

    if existing_category:
        return Response(
            {"error": "Category with this name already exists"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = NewCategorySerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@subscription([FREE_PLAN])
def get_category_id(request: HttpRequest) -> Response:
    """
    Retrieve the ID of a category based on its name for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the following JSON data:
            categoryName (str): The name of the category whose ID is to be retrieved.

    Returns:
        Response: JSON response with the ID of the category on success,
                      or an error message if the category name is not provided or not found.
    """
    parameters: dict = json.loads(request.body)
    user = request.user
    category_name = parameters.get("categoryName")

    if category_name:
        try:
            category = Category.objects.get(name=category_name, user=user)
            return Response({"id": category.id}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response(
                {"error": "Category does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {"error": "No category name provided"}, status=status.HTTP_400_BAD_REQUEST
        )
