"""
Module to handle the logic of email categorization customization

Endpoints:
- ✅ review_user_description: Reviews and validates the user-provided description for email categorization.
- ✅ generate_categories_scratch: Generates categories based on user-provided topics for email classification.
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


@api_view(["POST"])
@subscription(ALLOW_ALL)
def generate_categories_scratch(request: HttpRequest) -> dict:
    """
    Generates email categories based on user-provided topics for automatic email classification.

    Args:
        request (HttpRequest): HTTP request object containing the user topics.
            Expects a JSON body with:
                userTopics (str | list): A list or string of topics provided by the user.
                chatHistory (list): A list of messages between user and AI.

    Returns:
        Response: A JSON response with generated categories, descriptions, and feedback.
    """
    parameters: dict = json.loads(request.body)
    user_topics: str = parameters["userTopics"]
    chat_history: str = parameters.get("chatHistory")
    result = gemini.generate_categories_scratch(user_topics, chat_history)
    update_tokens_stats(request.user, result)

    return Response(result, status=status.HTTP_200_OK)
