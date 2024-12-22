"""
Handles category operations, returns results to frontend, and saves to database.

Endpoints:
- ✅ get_user_categories: Retrieve categories of the user.
- ✅ update_category: Update an existing category.
- ✅ delete_category: Delete a category.
- ✅ get_dependencies: Retrieve the number of rules and emails linked to a specified category.
- ✅ create_category: Create a new category.
- ✅ get_category_id: Retrieve the ID of a category based on its name.
- ✅ create_categories: Create multiple categories for the authenticated user from a dictionary or list.
"""

import json
import logging
from django.http import HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from aomail.utils.security import subscription
from aomail.constants import (
    ALLOW_ALL,
    DEFAULT_CATEGORY,
)
from aomail.models import (
    Category,
    Email,
    Rule,
)
from aomail.utils.serializers import (
    CategoryNameSerializer,
    NewCategorySerializer,
)


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


@api_view(["GET"])
@subscription(ALLOW_ALL)
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
@subscription(ALLOW_ALL)
def update_category(request: HttpRequest) -> Response:
    """
    Update an existing category for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameters in the body:
            categoryName (str): The current name of the category to update.
            newCategoryName (str, optional): The new name of the category to update.
            description (str, optional): The updated description for the category.

    Returns:
        Response: JSON response containing the updated category data or error messages.
    """
    parameters: dict = json.loads(request.body)
    current_name = parameters.get("categoryName")
    new_name = parameters.get("newCategoryName")
    description = parameters.get("description")

    if not current_name:
        return Response(
            {"error": "No category name provided"}, status=status.HTTP_400_BAD_REQUEST
        )
    if current_name == DEFAULT_CATEGORY:
        return Response(
            {"error": f"Cannot modify default category: {DEFAULT_CATEGORY}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if new_name and len(new_name) > 50:
        return Response(
            {"error": "New category name length exceeds 50 characters"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if description and len(description) > 300:
        return Response(
            {"error": "Description length exceeds 300 characters"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        category = Category.objects.get(name=current_name, user=request.user)
    except Category.DoesNotExist:
        return Response(
            {"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND
        )

    update_data = {}
    if new_name:
        update_data["name"] = new_name
    if description:
        update_data["description"] = description

    if not update_data:
        return Response(
            {"error": "No updates provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    serializer = CategoryNameSerializer(category, data=update_data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["DELETE"])
@subscription(ALLOW_ALL)
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
@subscription(ALLOW_ALL)
def get_dependencies(request: HttpRequest) -> Response:
    """
    Retrieves the number of rules and emails linked to a specified category for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameter in the body:
            - categoryName (str): The name of the category to retrieve linked rules and emails for.

    Returns:
        Response: JSON response containing:
            - nbRules (int): The number of rules linked to the specified category.
            - nbEmails (int): The number of emails linked to the specified category.
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

    rules_count = Rule.objects.filter(category=category, user=user).count()
    emails_count = Email.objects.filter(category=category, user=user).count()

    return Response(
        {"nbRules": rules_count, "nbEmails": emails_count}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
@subscription(ALLOW_ALL)
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
@subscription(ALLOW_ALL)
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

@api_view(["POST"])
@subscription(ALLOWED_PLANS)
def create_categories(request: HttpRequest) -> Response:
    """
    Create multiple categories for the authenticated user from a dictionary or list.

    Args:
        request (HttpRequest): The HTTP request object containing the following JSON data:
            categories (dict|list): Either:
                - Dictionary where keys are category names and values are descriptions
                  Format: {'category_name': 'category_description', ...}
                - List of dictionaries with name and description
                  Format: [{'name': 'category_name', 'description': 'category_description'}, ...]

    Returns:
        Response: JSON response with the created categories data on success,
                 or error messages on failure.
    """
    data: dict = json.loads(request.body)
    categories_data = data.get("categories", {})
    
    if not categories_data:
        return Response(
            {"error": "No categories provided"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    created_categories = []
    errors = []

    if not Category.objects.filter(user=request.user, name=DEFAULT_CATEGORY).exists():
        try:
            Category.objects.create(
                name=DEFAULT_CATEGORY,
                description="",
                user=request.user,
            )
        except Exception as e:
            LOGGER.error(f"Error creating default category: {str(e)}")
            errors.append("Error creating default category")

    if isinstance(categories_data, list):
        categories_dict = {
            item.get('name', ''): item.get('description', '')
            for item in categories_data
        }
    else:
        categories_dict = categories_data

    for name, description in categories_dict.items():
        if not name or not description:
            errors.append(f"Missing name or description for category")
            continue
            
        if name == DEFAULT_CATEGORY:
            errors.append(f"Cannot create category with name: {DEFAULT_CATEGORY}")
            continue
            
        if len(name) > 50:
            errors.append(f"Category name '{name}' exceeds 50 characters")
            continue
            
        if len(description) > 300:
            errors.append(f"Description for '{name}' exceeds 300 characters")
            continue

        if Category.objects.filter(user=request.user, name=name).exists():
            errors.append(f"Category '{name}' already exists")
            continue

        try:
            category_data = {
                "name": name,
                "description": description,
                "user": request.user.id
            }
            
            serializer = NewCategorySerializer(data=category_data)
            if serializer.is_valid():
                serializer.save()
                created_categories.append(serializer.data)
            else:
                errors.append(f"Invalid data for category '{name}': {serializer.errors}")
                
        except Exception as e:
            LOGGER.error(f"Error creating category '{name}': {str(e)}")
            errors.append(f"Error creating category '{name}'")

    response_data = {
        "created_categories": created_categories,
        "errors": errors
    }
    
    if created_categories:
        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {"error": "No categories were created", "details": errors},
            status=status.HTTP_400_BAD_REQUEST
        )
