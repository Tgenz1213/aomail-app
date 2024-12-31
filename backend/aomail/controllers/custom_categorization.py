"""
Module to handle the logic of email categorization customization

Endpoints:
- ✅ review_user_description: Reviews and validates the user-provided description for email categorization.
"""

import json
from rest_framework.decorators import api_view
from aomail.utils.security import subscription
from django.http import HttpRequest
from aomail.constants import ALLOW_ALL
from aomail.ai_providers import gemini
from aomail.ai_providers.utils import update_tokens_stats
from rest_framework import status
from rest_framework.response import Response


@api_view(["POST"])
@subscription(ALLOW_ALL)
def review_user_description(request: HttpRequest) -> dict:
    """
    Reviews and validates the user-provided description for email categorization.

    Args:
        request (HttpRequest): HTTP request object containing the user description.
            Expects a JSON body with:
                user_description (str): The description provided by the user for categorizing emails.

    Returns:
        Response: A JSON response with validation result and feedback message.
    """
    parameters: dict = json.loads(request.body)
    user_description: str = parameters["description"]
    result = gemini.review_user_description(user_description)
    update_tokens_stats(request.user, result)

    return Response(result, status=status.HTTP_200_OK)
