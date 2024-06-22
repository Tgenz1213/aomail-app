"""
Handles user settings operations, returns results to frontend, and saves to database.

Endpoints available:
- get_user_details: Returns the username of the authenticated user.
- get_user_language: Retrieve the language setting for the authenticated user.
- get_user_theme: Retrieve the theme setting for the authenticated user.
- get_user_timezone: Retrieve the timezone setting for the authenticated user.
- set_user_language: Set the language for the authenticated user.
- set_user_theme: Set the theme for the authenticated user.
- set_user_timezone: Set the timezone for the authenticated user.
- update_password: Update the password for the authenticated user.
- update_username: Update the username for the authenticated user.
"""

import json
import logging
from django.contrib.auth.models import User
from django.http import HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MailAssistant.utils.security import subscription
from MailAssistant.constants import (
    FREE_PLAN,
    LANGUAGES,
    THEMES,
)
from MailAssistant.models import (
    Preference,
)
from MailAssistant.utils.serializers import (
    PreferencesSerializer,
)


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


@api_view(["POST"])
@subscription([FREE_PLAN])
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
            {"error": "No new username provided."}, status=status.HTTP_400_BAD_REQUEST
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

    return Response({"success": "Username updated successfully."})


@api_view(["POST"])
@subscription([FREE_PLAN])
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
@subscription([FREE_PLAN])
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
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@subscription([FREE_PLAN])
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
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@subscription([FREE_PLAN])
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
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@subscription([FREE_PLAN])
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
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@subscription([FREE_PLAN])
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
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@subscription([FREE_PLAN])
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
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@subscription([FREE_PLAN])
def get_user_details(request: HttpRequest) -> Response:
    """Returns the username of authenticated user."""
    return Response({"username": request.user.username})


###########################################################
######################## TO DELETE ########################
###########################################################
@api_view(["GET"])
@subscription([FREE_PLAN])
def get_user_bg_color(request):
    try:
        preferences = Preference.objects.get(user=request.user)
        serializer = PreferencesSerializer(preferences)
        return Response(serializer.data)

    except Preference.DoesNotExist:
        return Response(
            {"error": "Preferences not found for the user."},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["POST"])
@subscription([FREE_PLAN])
def set_user_bg_color(request):
    try:
        preferences = Preference.objects.get(user=request.user)
    except Preference.DoesNotExist:
        preferences = Preference(user=request.user)

    serializer = PreferencesSerializer(preferences, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        LOGGER.error(f"Serializer errors in set_user_bg_color: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
