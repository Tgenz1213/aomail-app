"""
Handles user settings operations, returns results to frontend, and saves to database.

Endpoints:
- ✅ get_user_details: Returns the username of the authenticated user.
- ✅ get_user_language: Retrieve the language.
- ✅ get_user_theme: Retrieve the theme.
- ✅ get_user_timezone: Retrieve the timezone.
- ✅ set_user_language: Set the language.
- ✅ set_user_theme: Set the theme.
- ✅ set_user_timezone: Set the timezone.
- ✅ update_password: Update the password.
- ✅ update_username: Update the username.
- ✅ prioritization: Update the prioritization.
- ✅ get_user_guidelines: Retrieve the user's current guidelines for email prioritization.
- ✅ user_llm_settings: Retrieve, update, or create the LLM settings for the authenticated user.
"""

import json
import logging
from django.contrib.auth.models import User
from django.http import HttpRequest
from datetime import timedelta
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from aomail.utils.security import subscription
from aomail.constants import ALLOW_ALL
from aomail.models import Preference, Subscription
from aomail.ai_providers.prompts import (
    CATEGORIZE_AND_SUMMARIZE_EMAIL_PROMPT,
    CATEGORIZE_AND_SUMMARIZE_EMAIL_PROMPT_VARIABLES,
    GENERATE_EMAIL_PROMPT,
    GENERATE_EMAIL_PROMPT_VARIABLES,
    GENERATE_EMAIL_RESPONSE_PROMPT,
    GENERATE_EMAIL_RESPONSE_PROMPT_VARIABLES,
    GENERATE_RESPONSE_KEYWORDS_PROMPT,
    GENERATE_RESPONSE_KEYWORDS_PROMPT_VARIABLES,
    IMPROVE_EMAIL_DRAFT_PROMPT,
    IMPROVE_EMAIL_DRAFT_PROMPT_VARIABLES,
    IMPROVE_EMAIL_RESPONSE_PROMPT,
    IMPROVE_EMAIL_RESPONSE_PROMPT_VARIABLES,
)


LOGGER = logging.getLogger(__name__)
LANGUAGES = ["french", "american", "german", "russian", "spanish", "chinese", "indian"]
THEMES = ["dark", "light"]


@api_view(["POST"])
@subscription(ALLOW_ALL)
def update_username(request: HttpRequest) -> Response:
    """
    Update the username for the authenticated user.

    Args:
        request (HttpRequest): HTTP request object containing the new username in the request body.
            Expects JSON body with:
                username (str): The new username to update for the authenticated user.

    Returns:
        Response: Either {"success": "Username updated successfully."} if the update is successful,
                    or {"error": "Details of the specific error."} if there's an issue with the update.
    """
    parameters: dict = json.loads(request.body)
    user = request.user
    new_username = parameters.get("username")

    if not new_username:
        return Response(
            {"error": "No new username provided"}, status=status.HTTP_400_BAD_REQUEST
        )
    if len(new_username) > 150:
        return Response(
            {"error": "Maximum length of username is 150 characters"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    elif User.objects.filter(username=new_username).exists():
        return Response(
            {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
        )
    elif " " in new_username:
        return Response(
            {"error": "Username must not contain spaces"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.username = new_username
    user.save()

    return Response({"success": "Username updated successfully"})


@api_view(["POST"])
@subscription(ALLOW_ALL)
def update_password(request: HttpRequest) -> Response:
    """
    Update the password for the authenticated user.

    Args:
        request (HttpRequest): HTTP request object containing the new password in the request body.
            Expects JSON body with:
                password (str): The new password to update for the authenticated user.

    Returns:
        Response: Either {"success": "Password updated successfully."} if the update is successful,
                    or {"error": "Details of the specific error."} if there's an issue with the update.
    """
    parameters: dict = json.loads(request.body)
    user = request.user
    new_password = parameters.get("password")

    if not new_password:
        return Response(
            {"error": "No new password provided."}, status=status.HTTP_400_BAD_REQUEST
        )
    elif not (8 <= len(new_password) <= 32):
        return Response(
            {"error": "Password length must be between 8 and 32 characters"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.set_password(new_password)
    user.save()

    return Response({"success": "Password updated successfully."})


@api_view(["GET"])
@subscription(ALLOW_ALL)
def get_user_language(request: HttpRequest) -> Response:
    """
    Retrieve the language setting for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: JSON response with the user's language setting on success,
                      or an error message on failure.
    """
    user = request.user

    try:
        language = Preference.objects.get(user=user).language
        return Response({"language": language}, status=status.HTTP_200_OK)
    except Exception as e:
        LOGGER.error(
            f"Unexpected error occurred when retrieving user language: {str(e)}"
        )
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@subscription(ALLOW_ALL)
def set_user_language(request: HttpRequest) -> Response:
    """
    Set the language for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameter in the body:
            language (str): The language code to set for the user.

    Returns:
        Response: JSON response indicating success or failure of setting the user's language.
    """
    parameters: dict = json.loads(request.body)
    user = request.user
    language: str = parameters.get("language")

    if not language:
        return Response(
            {"error": "No language provided"}, status=status.HTTP_400_BAD_REQUEST
        )
    if language not in LANGUAGES:
        return Response(
            {"error": "Language not allowed"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        preferences = Preference.objects.get(user=user)
        preferences.language = language
        preferences.save()
        return Response(
            {"message": "Language updated successfully"}, status=status.HTTP_200_OK
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error occurred when changing user language: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@subscription(ALLOW_ALL)
def get_user_theme(request: HttpRequest) -> Response:
    """
    Retrieve the theme setting for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: JSON response with the user's theme setting on success,
                      or an error message on failure.
    """
    user = request.user
    try:
        theme = Preference.objects.get(user=user).theme
        return Response({"theme": theme}, status=status.HTTP_200_OK)
    except Exception as e:
        LOGGER.error(f"Failed to retrieve user theme: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@subscription(ALLOW_ALL)
def set_user_theme(request: HttpRequest) -> Response:
    """
    Set the theme for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameter in the body:
            theme (str): The theme to set for the user.

    Returns:
        Response: JSON response indicating success or failure of setting the user's theme.
    """
    parameters: dict = json.loads(request.body)
    user = request.user
    theme = parameters.get("theme")

    if not theme:
        return Response(
            {"error": "No theme provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    if theme not in THEMES:
        return Response(
            {"error": "Theme not allowed"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        preference = Preference.objects.get(user=user)
        preference.theme = theme
        preference.save()
        return Response(
            {"message": "Theme updated successfully"}, status=status.HTTP_200_OK
        )
    except Exception as e:
        LOGGER.error(f"Failed to update user theme: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@subscription(ALLOW_ALL)
def get_user_timezone(request: HttpRequest) -> Response:
    """
    Retrieve the timezone setting for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: JSON response with the user's timezone setting on success,
                      or an error message on failure.
    """
    user = request.user
    try:
        timezone = Preference.objects.get(user=user).timezone
        return Response({"timezone": timezone}, status=status.HTTP_200_OK)
    except Exception as e:
        LOGGER.error(f"Failed to retrieve user timezone: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@subscription(ALLOW_ALL)
def set_user_timezone(request: HttpRequest) -> Response:
    """
    Set the timezone for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameter in the body:
            timezone (str): The timezone to set for the user.

    Returns:
        Response: JSON response indicating success or failure of setting the user's timezone.
    """
    parameters: dict = json.loads(request.body)
    user = request.user
    timezone = parameters.get("timezone")

    if not timezone:
        return Response(
            {"error": "No timezone provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        preference = Preference.objects.get(user=user)
        preference.timezone = timezone
        preference.save()
        return Response(
            {"message": "Timezone updated successfully"}, status=status.HTTP_200_OK
        )
    except Exception as e:
        LOGGER.error(f"Failed to update timezone: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@subscription(ALLOW_ALL)
def get_user_details(request: HttpRequest) -> Response:
    """Returns the username of authenticated user."""
    return Response({"username": request.user.username}, status=status.HTTP_200_OK)


@api_view(["GET"])
@subscription(ALLOW_ALL)
def get_user_plan(request: HttpRequest) -> Response:
    """Returns the subscription plan of the authenticated user."""
    user = request.user
    subscription = get_object_or_404(Subscription, user=user)
    trial_period = timedelta(days=14)

    return Response(
        {
            "plan": subscription.plan,
            "isTrial": subscription.is_trial,
            "isActive": subscription.is_active,
            "createdAt": subscription.created_at,
            "expiresThe": (
                subscription.created_at + trial_period
                if subscription.is_trial
                else None
            ),
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@subscription(ALLOW_ALL)
def prioritization(request: HttpRequest) -> Response:
    """
    Update the user's email prioritization guidelines based on the input received.

    Args:
        request (HttpRequest): The HTTP request containing the following parameters:
            - importantGuidelines (str): Description of important emails.
            - informativeGuidelines (str): Description of informative emails.
            - uselessGuidelines (str): Description of useless emails.

    Returns:
        Response: A JSON response indicating the success or failure of updating the prioritization guidelines.
    """
    parameters: dict = json.loads(request.body)

    important_guidelines = parameters.get("importantGuidelines")
    informative_guidelines = parameters.get("informativeGuidelines")
    useless_guidelines = parameters.get("uselessGuidelines")

    preference = get_object_or_404(Preference, user=request.user)

    if important_guidelines:
        preference.important_guidelines = important_guidelines
    if informative_guidelines:
        preference.informative_guidelines = informative_guidelines
    if useless_guidelines:
        preference.useless_guidelines = useless_guidelines
    preference.save()

    return Response(
        {"message": "Guidelines updated successfully"}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@subscription(ALLOW_ALL)
def get_user_guidelines(request: HttpRequest) -> Response:
    """
    Retrieve the current email prioritization guidelines for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: JSON response containing the user's current guidelines for email prioritization.
    """
    try:
        preference = Preference.objects.get(user=request.user)
        return Response(
            {
                "importantGuidelines": preference.important_guidelines,
                "informativeGuidelines": preference.informative_guidelines,
                "uselessGuidelines": preference.useless_guidelines,
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        LOGGER.error(f"Failed to retrieve user guidelines: {str(e)}")
        return Response(
            {"error": "Failed to retrieve guidelines"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET", "PUT", "DELETE"])
@subscription(ALLOW_ALL)
def user_llm_settings(request: HttpRequest) -> Response:
    """
    Retrieve, update, or create the LLM settings for the authenticated user.
    """
    if request.method == "GET":
        return get_user_llm_settings(request)
    elif request.method == "PUT":
        return update_user_llm_settings(request)
    elif request.method == "DELETE":
        return reset_user_llm_settings(request)


def get_user_llm_settings(request: HttpRequest) -> Response:
    """
    Retrieve the LLM settings for the authenticated user.
    """
    preference = get_object_or_404(Preference, user=request.user)

    return Response(
        {
            "llmProvider": preference.llm_provider,
            "llmModel": (
                preference.llm_model if preference.llm_model else "gemini-1.5-flash"
            ),
            # todo return a dict {prompt: "", variables: []} for all + update the frontend to use it
            "improveEmailDraftPrompt": (
                preference.improve_email_draft_prompt
                if preference.improve_email_draft_prompt
                else IMPROVE_EMAIL_DRAFT_PROMPT
            ),
            "improveEmailResponsePrompt": (
                preference.improve_email_response_prompt
                if preference.improve_email_response_prompt
                else IMPROVE_EMAIL_RESPONSE_PROMPT
            ),
            "categorizeAndSummarizeEmailPrompt": (
                preference.categorize_and_summarize_email_prompt
                if preference.categorize_and_summarize_email_prompt
                else CATEGORIZE_AND_SUMMARIZE_EMAIL_PROMPT
            ),
            "generateEmailResponsePrompt": (
                preference.generate_email_response_prompt
                if preference.generate_email_response_prompt
                else GENERATE_EMAIL_RESPONSE_PROMPT
            ),
            "generateEmailPrompt": (
                preference.generate_email_prompt
                if preference.generate_email_prompt
                else GENERATE_EMAIL_PROMPT
            ),
            "generateResponseKeywordsPrompt": (
                preference.generate_response_keywords_prompt
                if preference.generate_response_keywords_prompt
                else GENERATE_RESPONSE_KEYWORDS_PROMPT
            ),
        },
        status=status.HTTP_200_OK,
    )


def update_user_llm_settings(request: HttpRequest) -> Response:
    """
    Update the LLM settings for the authenticated user.
    """
    subscription = Subscription.objects.get(user=request.user)

    if subscription.is_trial:
        return Response(
            {"error": "You can only edit the prompts with a paid plan"},
            status=status.HTTP_403_FORBIDDEN,
        )

    parameters: dict = json.loads(request.body)
    preference = get_object_or_404(Preference, user=request.user)

    if parameters.get("llmProvider"):
        preference.llm_provider = parameters.get("llmProvider")
    if parameters.get("llmModel"):
        preference.llm_model = parameters.get("llmModel")

    improve_email_draft_prompt = parameters.get("improveEmailDraftPrompt")
    if improve_email_draft_prompt and all(
        f"{{{variable}}}" in improve_email_draft_prompt
        for variable in IMPROVE_EMAIL_DRAFT_PROMPT_VARIABLES
    ):
        preference.improve_email_draft_prompt = improve_email_draft_prompt

    improve_email_response_prompt = parameters.get("improveEmailResponsePrompt")
    if improve_email_response_prompt and all(
        f"{{{variable}}}" in improve_email_response_prompt
        for variable in IMPROVE_EMAIL_RESPONSE_PROMPT_VARIABLES
    ):
        preference.improve_email_response_prompt = improve_email_response_prompt

    categorize_and_summarize_email_prompt = parameters.get(
        "categorizeAndSummarizeEmailPrompt"
    )
    if categorize_and_summarize_email_prompt and all(
        f"{{{variable}}}" in categorize_and_summarize_email_prompt
        for variable in CATEGORIZE_AND_SUMMARIZE_EMAIL_PROMPT_VARIABLES
    ):
        preference.categorize_and_summarize_email_prompt = (
            categorize_and_summarize_email_prompt
        )

    generate_email_response_prompt = parameters.get("generateEmailResponsePrompt")
    if generate_email_response_prompt and all(
        f"{{{variable}}}" in generate_email_response_prompt
        for variable in GENERATE_EMAIL_RESPONSE_PROMPT_VARIABLES
    ):
        preference.generate_email_response_prompt = generate_email_response_prompt

    generate_email_prompt = parameters.get("generateEmailPrompt")
    if generate_email_prompt and all(
        f"{{{variable}}}" in generate_email_prompt
        for variable in GENERATE_EMAIL_PROMPT_VARIABLES
    ):
        preference.generate_email_prompt = generate_email_prompt

    generate_response_keywords_prompt = parameters.get("generateResponseKeywordsPrompt")
    if generate_response_keywords_prompt and all(
        f"{{{variable}}}" in generate_response_keywords_prompt
        for variable in GENERATE_RESPONSE_KEYWORDS_PROMPT_VARIABLES
    ):
        preference.generate_response_keywords_prompt = generate_response_keywords_prompt

    preference.save()

    return Response(
        {"message": "LLM settings updated successfully"}, status=status.HTTP_200_OK
    )


def reset_user_llm_settings(request: HttpRequest) -> Response:
    """
    Reset the LLM settings to the default values.
    """
    parameters: dict = json.loads(request.body)
    preference = get_object_or_404(Preference, user=request.user)

    if parameters.get("resetAll"):
        preference.improve_email_draft_prompt = None
        preference.improve_email_response_prompt = None
        preference.categorize_and_summarize_email_prompt = None
        preference.generate_email_response_prompt = None
        preference.generate_email_prompt = None
        preference.generate_response_keywords_prompt = None
        preference.llm_model = None
        preference.llm_provider = "google"
        preference.save()

        return Response(
            {"message": "LLM settings and prompts reset to default"},
            status=status.HTTP_200_OK,
        )
    else:
        # Reset selected prompts
        if parameters.get("improveEmailDraftPrompt"):
            preference.improve_email_draft_prompt = None
        if parameters.get("improveEmailResponsePrompt"):
            preference.improve_email_response_prompt = None
        if parameters.get("categorizeAndSummarizeEmailPrompt"):
            preference.categorize_and_summarize_email_prompt = None
        if parameters.get("generateEmailResponsePrompt"):
            preference.generate_email_response_prompt = None
        if parameters.get("generateEmailPrompt"):
            preference.generate_email_prompt = None
        if parameters.get("generateResponseKeywordsPrompt"):
            preference.generate_response_keywords_prompt = None

        preference.save()

        return Response(
            {"message": "Prompt reset to default"}, status=status.HTTP_200_OK
        )
