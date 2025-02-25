"""
Module to handle the logic of email categorization and prioritization customization.

Endpoints:
- ✅ review_user_description: Reviews and validates the user-provided description for email categorization.
- ✅ generate_categories_scratch: Generates categories based on user-provided topics for email classification.
- ✅ generate_prioritization_scratch: Generates email prioritization guidance based on user input for better categorization.
"""

import json
from rest_framework.decorators import api_view
from aomail.utils.security import block_user, subscription
from django.http import HttpRequest
from aomail.constants import ALLOWED_PLANS
from aomail.ai_providers import llm_functions
from aomail.ai_providers.utils import update_tokens_stats
from rest_framework import status
from rest_framework.response import Response
from aomail.models import Preference


@api_view(["POST"])
@block_user
@subscription(ALLOWED_PLANS)
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
    preference = Preference.objects.get(user=request.user)
    result = llm_functions.review_user_description(
        user_description, preference.llm_provider, preference.llm_model
    )
    update_tokens_stats(request.user, result)

    return Response(result, status=status.HTTP_200_OK)


@api_view(["POST"])
@block_user
@subscription(ALLOWED_PLANS)
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
    preference = Preference.objects.get(user=request.user)
    result = llm_functions.generate_categories_scratch(
        user_topics,
        chat_history,
        preference.llm_provider,
        preference.llm_model,
    )
    update_tokens_stats(request.user, result)

    return Response(result, status=status.HTTP_200_OK)


@api_view(["POST"])
@block_user
@subscription(ALLOWED_PLANS)
def generate_prioritization_scratch(request: HttpRequest) -> dict:
    """
    Generates email prioritization guidance based on user-provided input to optimize categorization.

    Args:
        request (HttpRequest): HTTP request object containing the following JSON body:
            - userInput (dict | str): A dictionary or string with user-provided prioritization guidelines.

    Returns:
        Response: A JSON response with:
            - important (str): Enhanced description of important emails.
            - informative (str): Enhanced description of informative emails.
            - useless (str): Enhanced description of useless emails.
    """
    parameters: dict = json.loads(request.body)
    user_input: str = parameters["userInput"]
    preference = Preference.objects.get(user=request.user)
    result = llm_functions.generate_prioritization_scratch(
        user_input, preference.llm_provider, preference.llm_model
    )
    update_tokens_stats(request.user, result)

    return Response(result, status=status.HTTP_200_OK)
