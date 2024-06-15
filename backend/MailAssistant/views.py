"""
Handles frontend requests and redirects them to the appropriate API.

TODO:
- (ANTI scraping/reverse engineering): Add a system that counts the number of 400 erros per user and send warning + ban
- Split all the code inside files and put it all inside 'controllers' folder
- Define all constants locally and globally (according to the scope)
- Log important messages/errors using IP, user id, clear error name when possible
- Clean the code by adding data types.
- Improve documentation to be concise.
- STOP using differents libs to do the same thing => only use 1
    EXAMPLE:
    status=200 | status=status.HTTP_200_OK => choose 1 (STRICTLY USE status.HTTP_CODE_DESC and stick to it
    JsonResponse | Response => choose 1 and stick to it
- Ensure Pylance can recognize variable types and methods.
    EXAMPLE:
    def view_function(request: HttpRequest):
        user = request.user
        # USE THIS instead of 'data'
        parameters: dict = json.loads(request.body)
- Refactor FE and backend requests: get_user_<data> by returning a dict and NOT a string (safe=False must be removed)
  CHECK everywhere a serializer is used as it is going to create issues
- Add check if serializer is valid everywhere a serializer is used and return errors + 400_BAD_REQUEST

REMAINING functions to opti and clean:
- def find_user_view_ai(request: HttpRequest) -> JsonResponse:
"""

import datetime
from functools import wraps
import json
import logging
import re
import threading
import os
import time
from django.db import IntegrityError
import jwt
import stripe
from django.http import FileResponse, Http404
from django.utils import timezone
from collections import defaultdict
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Subquery, Exists, OuterRef
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from collections import defaultdict
from MailAssistant.ai_providers import gpt_3_5_turbo, mistral, claude
from MailAssistant.email_providers import google_api, microsoft_api
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.core.mail import send_mail
from MailAssistant.constants import (
    ADMIN_EMAIL_LIST,
    BASE_URL_MA,
    DEFAULT_CATEGORY,
    EMAIL_NO_REPLY,
    ENCRYPTION_KEYS,
    GOOGLE_PROVIDER,
    LANGUAGES,
    MAX_RETRIES,
    MICROSOFT_PROVIDER,
    STRIPE_PAYMENT_FAILED_URL,
    STRIPE_PAYMENT_SUCCESS_URL,
    STRIPE_PRICES,
    STRIPE_SECRET_KEY,
    THEMES,
    MEDIA_ROOT,
)
from MailAssistant.controllers.tree_knowledge import Search
from MailAssistant.utils import security
from MailAssistant.utils.security import subscription
from .models import (
    Category,
    GoogleListener,
    MicrosoftListener,
    SocialAPI,
    Email,
    Rule,
    Preference,
    Sender,
    Contact,
    Subscription,
    CC_sender,
    BCC_sender,
)
from .serializers import (
    CategoryNameSerializer,
    EmailReadUpdateSerializer,
    EmailReplyLaterUpdateSerializer,
    RuleBlockUpdateSerializer,
    PreferencesSerializer,
    RuleSerializer,
    SenderSerializer,
    NewEmailAISerializer,
    EmailAIRecommendationsSerializer,
    EmailCorrectionSerializer,
    EmailCopyWritingSerializer,
    EmailProposalAnswerSerializer,
    EmailGenerateAnswer,
    NewCategorySerializer,
    ContactSerializer,
)


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)
FREE_PLAN = "free_plan"
READ_EMAILS_MARKER = "read"


######################## REGISTRATION ########################
@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request: HttpRequest) -> JsonResponse:
    """
    Register user in database and handle the callback of the API with OAuth2.0.

    Args:
        request (HttpRequest): The HTTP request object containing the following user data in the body:
            type_api (str): Type of API (e.g., 'google' or 'microsoft').
            code (str): OAuth2.0 authorization code.
            login (str): User's login or username.
            password (str): User's password.
            timezone (str): User's preferred timezone.
            language (str): User's preferred language.
            theme (str): User's preferred theme.
            color (str): User's preferred color.
            categories (list): List of categories associated with the user.
            userDescription (str): Description or bio of the user.

    Returns:
        JsonResponse: JSON response with user ID, access token, and email on success,
                      or error message on failure.
    """
    ip = security.get_ip_with_port(request)
    LOGGER.info(f"Signup request received from IP: {ip}")

    parameters: dict = json.loads(request.body)
    type_api: str = parameters.get("type_api", "")
    code: str = parameters.get("code", "")
    username: str = parameters.get("login", "")
    password: str = parameters.get("password", "")
    timezone: str = parameters.get("timezone", "")
    language: str = parameters.get("language", "")
    theme: str = parameters.get("theme", "")
    color: str = parameters.get("color", "")
    categories: list = parameters.get("categories", [])
    user_description: str = parameters.get("userDescription", "")

    validation_result: dict = validate_signup_data(username, password, code)
    if "error" in validation_result:
        LOGGER.error(f"Validation failed for signup data: {validation_result['error']}")
        return JsonResponse(validation_result, status=status.HTTP_400_BAD_REQUEST)

    LOGGER.info("User signup data validated successfully")

    authorization_result: dict = validate_authorization_code(type_api, code)
    if "error" in authorization_result:
        LOGGER.error(f"Authorization failed: {authorization_result['error']}")
        return JsonResponse(
            {"error": authorization_result["error"]}, status=status.HTTP_400_BAD_REQUEST
        )

    LOGGER.info(f"Successfully validated authorization code for {type_api} API")

    access_token = authorization_result.get("access_token", "")
    refresh_token = authorization_result.get("refresh_token", "")
    email = authorization_result.get("email", "")

    if email:
        if SocialAPI.objects.filter(email=email).exists():
            LOGGER.error("Email address already used by another account")
            return JsonResponse(
                {"error": "Email address already used by another account"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif " " in email:
            LOGGER.error("Email address must not contain spaces")
            return JsonResponse(
                {"error": "Email address must not contain spaces"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        LOGGER.error("No email received")
        return JsonResponse(
            {"error": "No email received"}, status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(username, "", password)
    LOGGER.info(f"User {username} created successfully")

    try:
        django_refresh_token: RefreshToken = RefreshToken.for_user(user)
        django_access_token = str(django_refresh_token.access_token)
    except Exception as e:
        LOGGER.error(f"Failed to generate access token: {str(e)}")
        user.delete()
        LOGGER.info(f"User {username} deleted successfully")
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    result = save_user_data(
        user,
        type_api,
        user_description,
        email,
        access_token,
        refresh_token,
        theme,
        color,
        categories,
        language,
        timezone,
    )
    if "error" in result:
        LOGGER.error(f"Failed to save user data: {result['error']}")
        user.delete()
        LOGGER.info(f"User {username} deleted successfully")
        return JsonResponse(result, status=status.HTTP_400_BAD_REQUEST)

    LOGGER.info(f"User data saved successfully for {username}")

    try:
        if type_api == "google":
            threading.Thread(
                target=google_api.set_all_contacts, args=(user, email)
            ).start()
        elif type_api == "microsoft":
            if microsoft_api.verify_license(access_token):
                threading.Thread(
                    target=microsoft_api.set_all_contacts, args=(access_token, user)
                ).start()
            else:
                LOGGER.error("No license associated with the account")
                user.delete()
                LOGGER.info(f"User {username} deleted successfully")
                return JsonResponse(
                    {"error": "No license associated with the account"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    except Exception as e:
        LOGGER.error(f"Failed to set contacts: {str(e)}")
        user.delete()
        LOGGER.info(f"User {username} deleted successfully")
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    end_date: datetime.datetime = datetime.datetime.now() + datetime.timedelta(days=30)
    end_date_utc = end_date.replace(tzinfo=datetime.timezone.utc)
    Subscription.objects.create(
        user=user,
        plan=FREE_PLAN,
        stripe_subscription_id=None,
        end_date=end_date_utc,
        billing_interval=None,
        amount=0.0,
    )
    LOGGER.info(f"User {username} subscribed to free plan")

    subscribed = subscribe_listeners(type_api, user, email)
    if subscribed:
        LOGGER.info(f"User {username} subscribed to listeners successfully")
        return JsonResponse(
            {"access_token": django_access_token},
            status=status.HTTP_201_CREATED,
        )
    else:
        LOGGER.error(f"Failed to subscribe user {username} to listeners")
        user.delete()
        LOGGER.info(f"User {username} deleted successfully")
        return JsonResponse(
            {"error": "Could not subscribe to listener"},
            status=status.HTTP_400_BAD_REQUEST,
        )


def subscribe_listeners(type_api: str, user: str, email: str) -> bool:
    """
    Subscribes the user to listeners based on the type of API provided.

    Args:
        type_api (str): The type of API.
        user (str): User identifier.
        email (str): User's email address.

    Returns:
        bool: True if subscription was successful, False otherwise.
    """
    if type_api == "google":
        subscribed = google_api.subscribe_to_email_notifications(user, email)
        if subscribed:
            social_api = google_api.get_social_api(user, email)
            GoogleListener.objects.create(
                last_modified=timezone.now(), social_api=social_api
            )
            return True

    elif type_api == "microsoft":
        subscribed_email = microsoft_api.subscribe_to_email_notifications(user, email)
        subscribed_contact = microsoft_api.subscribe_to_contact_notifications(
            user, email
        )
        if subscribed_email and subscribed_contact:
            return True

    return False


def validate_authorization_code(type_api: str, code: str) -> dict:
    """
    Validates the authorization code for a given API type and returns the access token,
    refresh token, and associated email.

    Args:
        type_api (str): The type of API.
        code (str): The authorization code.

    Returns:
        dict: A dictionary containing access_token, refresh_token, and email,
              or an error message if validation fails.
    """
    try:
        if type_api == "google":
            access_token, refresh_token = google_api.exchange_code_for_tokens(code)
            if not access_token or not refresh_token:
                return {
                    "error": "Failed to obtain access or refresh token from Google API"
                }

            result_get_email = google_api.get_email(access_token, refresh_token)
            if "error" in result_get_email:
                return {"error": result_get_email["error"]}
            else:
                email = result_get_email["email"]

        elif type_api == "microsoft":
            access_token, refresh_token = microsoft_api.exchange_code_for_tokens(code)
            if not access_token or not refresh_token:
                return {
                    "error": "Failed to obtain access or refresh token from Microsoft API"
                }

            result_get_email = microsoft_api.get_email(access_token)
            if "error" in result_get_email:
                return {"error": result_get_email["error"]}
            else:
                email = result_get_email["email"]

        else:
            return {"error": f"Unsupported API type: {type_api}"}

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "email": email,
        }

    except Exception as e:
        return {"error": "An unexpected error occurred during validation"}


def validate_code_link_email(type_api: str, code: str) -> dict:
    """
    Validates the authorization code for a given API type and returns the access token,
    refresh token, and associated email.

    Args:
        type_api (str): The type of API.
        code (str): The authorization code.

    Returns:
        dict: A dictionary containing access_token, refresh_token, and email,
              or an error message if validation fails.
    """
    try:
        if type_api == "google":
            access_token, refresh_token = google_api.link_email_tokens(code)
            if not access_token or not refresh_token:
                return {
                    "error": "Failed to obtain access or refresh token from Google API"
                }

            email = google_api.get_email(access_token, refresh_token)
            if not email:
                return {"error": "Failed to obtain email from Google API"}

        elif type_api == "microsoft":
            access_token, refresh_token = microsoft_api.link_email_tokens(code)
            if not access_token:
                return {"error": "Failed to obtain access token from Microsoft API"}

            email = microsoft_api.get_email(access_token)
            if not email:
                return {"error": "Failed to obtain email from Microsoft API"}

        else:
            return {"error": f"Unsupported API type: {type_api}"}

        LOGGER.info(f"Successfully validated code for {type_api} API")
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "email": email,
        }

    except Exception as e:
        LOGGER.error(f"Unexpected error during validation for {type_api} API: {str(e)}")
        return {"error": "An unexpected error occurred during validation"}


def validate_signup_data(username: str, password: str, code: str) -> dict:
    """
    Validates user signup data to ensure all requirements are met.

    Args:
        username (str): Username provided by the user.
        password (str): Password provided by the user.
        code (str): Authorization code provided by the user.

    Returns:
        dict: {'error': <error_message>} if validation fails,
              {'message': 'User signup data validated successfully'} with appropriate success message if validation passes.
    """
    if not code:
        return {"error": "No authorization code provided"}
    elif User.objects.filter(username=username).exists():
        return {"error": "Username already exists"}
    elif " " in username:
        return {"error": "Username must not contain spaces"}
    elif not (8 <= len(password) <= 32):
        return {"error": "Password length must be between 8 and 32 characters"}

    return {"message": "User signup data validated successfully"}


def save_user_data(
    user: User,
    type_api: str,
    user_description: str,
    email: str,
    access_token: str,
    refresh_token: str,
    theme: str,
    color: str,
    categories: dict,
    language: str,
    timezone: str,
) -> dict:
    """
    Store user credentials and settings in the database.

    Args:
        user (User): Django User model instance representing the user.
        type_api (str): Type of API associated with the user.
        user_description (str): Description of the user.
        email (str): User's email address.
        access_token (str): Access token for API authentication.
        refresh_token (str): Refresh token for API authentication.
        theme (str): Preferred theme for the user interface.
        color (str): Background color preference.
        categories (dict): Dictionary containing categories data.
                           Expected format: {'name': str, 'description': str}
        language (str): Preferred language setting.
        timezone (str): Preferred timezone.

    Returns:
        dict: {'message': 'User data saved successfully'} on success,
              {'error': <error_message>} on failure.
    """
    try:
        refresh_token_encrypted = security.encrypt_text(
            ENCRYPTION_KEYS["SocialAPI"]["refresh_token"], refresh_token
        )
        SocialAPI.objects.create(
            user=user,
            user_description=user_description,
            type_api=type_api,
            email=email,
            access_token=access_token,
            refresh_token=refresh_token_encrypted,
        )
        Preference.objects.create(
            theme=theme, bg_color=color, language=language, timezone=timezone, user=user
        )

        if categories:
            try:
                categories_json: list[dict] = json.loads(categories)
                for category_data in categories_json:
                    category_name = category_data.get("name")
                    category_description = category_data.get("description")

                    Category.objects.create(
                        name=category_name, description=category_description, user=user
                    )
            except json.JSONDecodeError:
                return {"error": "Invalid categories data"}

        Category.objects.create(
            name=DEFAULT_CATEGORY,
            description="",
            user=user,
        )

        return {"message": "User data saved successfully"}

    except Exception as e:
        return {"error": str(e)}


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def is_authenticated(request):
    """Used in index.js by the router to check if the user can access enpoints"""
    return JsonResponse({"isAuthenticated": True}, status=status.HTTP_200_OK)


######################## ENDPOINTS HANDLING GMAIL & OUTLOOK ########################
# ----------------------- GET REQUESTS -----------------------#
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def unread_mails(request: Request):
    return forward_request(request._request, "unread_mails")


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_profile_image(request: Request):
    return forward_request(request._request, "get_profile_image")


# ----------------------- POST REQUESTS -----------------------#
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def send_email(request: Request):
    return forward_request(request._request, "send_email")


def forward_request(request: HttpRequest, api_method: str) -> JsonResponse:
    """
    Forwards the request to the appropriate API method based on type_api.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameters in the body:
            email (str, optional): User's email address.
        api_method (str): The API method to be called.

    Returns:
        JsonResponse: The response from the API method or an error response if
                      the API type or method is unsupported, or if the SocialAPI
                      entry is not found for the user and email.
    """
    user = request.user
    email = request.POST.get("email")
    if email is None:
        email = request.headers.get("email")

    try:
        social_api = SocialAPI.objects.get(user=user, email=email)
        type_api = social_api.type_api
    except SocialAPI.DoesNotExist:
        LOGGER.error(
            f"SocialAPI entry not found for the user with ID: {user.id} and email: {email}"
        )
        return JsonResponse(
            {"error": "SocialAPI entry not found for the user and email"},
            status=status.HTTP_404_NOT_FOUND,
        )

    api_module = None
    if type_api == "google":
        api_module = google_api
    elif type_api == "microsoft":
        api_module = microsoft_api

    if api_module and hasattr(api_module, api_method):
        api_function = getattr(api_module, api_method)
        return api_function(request)
    else:
        return JsonResponse(
            {"error": "Unsupported API or method"}, status=status.HTTP_400_BAD_REQUEST
        )


######################## AUTHENTICATION API ########################
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request: HttpRequest) -> JsonResponse:
    """
    Authenticates a user using the provided username and password and returns an access token.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameters in the body:
            username (str): User's username for authentication.
            password (str): User's password for authentication.

    Returns:
        JsonResponse: JSON response with an access token on successful authentication,
                      or an error message on failure.
    """
    parameters: dict = json.loads(request.body)
    username = parameters.get("username")
    password = parameters.get("password")

    if not username or not password:
        return JsonResponse(
            {"error": "Username and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(username=username, password=password)

    if user:
        refresh: RefreshToken = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return JsonResponse({"access_token": access_token}, status=status.HTTP_200_OK)
    else:
        return JsonResponse(
            {"error": "Invalid username or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_token(request: HttpRequest) -> JsonResponse:
    """
    Refreshes the JWT access token for a user and returns a new access token.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameter in the body:
            access_token (str): JWT access token to be refreshed.

    Returns:
        JsonResponse: JSON response with a new access token on success,
                      or an error message on failure.
    """
    parameters: dict = json.loads(request.body)
    access_token: str = parameters.get("access_token")

    if not access_token:
        return JsonResponse(
            {"error": "Access token is missing"}, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        # Decode the token without checking for expiration
        decoded_data: dict = jwt.decode(
            access_token,
            api_settings.SIGNING_KEY,
            algorithms=[api_settings.ALGORITHM],
            options={"verify_exp": False},
        )
        user = User.objects.get(id=decoded_data["user_id"])
        refresh_token: RefreshToken = RefreshToken.for_user(user)
        new_access_token = str(refresh_token.access_token)

        return JsonResponse(
            {"access_token": new_access_token}, status=status.HTTP_200_OK
        )
    except Exception as e:
        LOGGER.error(
            f"Unexpected error occured when refreshing Django access token: {str(e)}"
        )
        return JsonResponse(
            {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


######################## LANGUAGES ########################
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_user_language(request: HttpRequest) -> JsonResponse:
    """
    Retrieve the language setting for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response with the user's language setting on success,
                      or an error message on failure.
    """
    user = request.user

    try:
        language = Preference.objects.get(user=user).language
        return JsonResponse({"language": language}, status=status.HTTP_200_OK)
    except Exception as e:
        LOGGER.error(
            f"Unexpected error occurred when retrieving user language: {str(e)}"
        )
        return JsonResponse(
            {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def set_user_language(request: HttpRequest) -> JsonResponse:
    """
    Set the language for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameter in the body:
            language (str): The language code to set for the user.

    Returns:
        JsonResponse: JSON response indicating success or failure of setting the user's language.
    """
    parameters: dict = json.loads(request.body)
    user = request.user
    language: str = parameters.get("language")

    if not language:
        return JsonResponse(
            {"error": "No language provided"}, status=status.HTTP_400_BAD_REQUEST
        )
    if language not in LANGUAGES:
        return JsonResponse(
            {"error": "Language not allowed"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        preferences = Preference.objects.get(user=user)
        preferences.language = language
        preferences.save()
        return JsonResponse(
            {"message": "Language updated successfully"}, status=status.HTTP_200_OK
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error occurred when changing user language: {str(e)}")
        return JsonResponse(
            {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


######################## PICTURES ########################
def serve_image(request, image_name):
    image_path = os.path.join(MEDIA_ROOT, "pictures", image_name)
    if os.path.exists(image_path):
        _, ext = os.path.splitext(image_path)
        content_type = (
            "image/jpeg"
            if ext.lower() == ".jpg"
            else "image/png" if ext.lower() == ".png" else None
        )
        if content_type:
            return FileResponse(open(image_path, "rb"), content_type=content_type)
        else:
            raise Http404("Unsupported image format")
    else:
        raise Http404("Image not found")


######################## THEMES ########################
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_user_theme(request: HttpRequest) -> JsonResponse:
    """
    Retrieve the theme setting for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response with the user's theme setting on success,
                      or an error message on failure.
    """
    user = request.user
    try:
        theme = Preference.objects.get(user=user).theme
        return JsonResponse({"theme": theme}, status=status.HTTP_200_OK)
    except Exception as e:
        LOGGER.error(f"Failed to retrieve user theme: {str(e)}")
        return JsonResponse(
            {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def set_user_theme(request: HttpRequest) -> JsonResponse:
    """
    Set the theme for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameter in the body:
            theme (str): The theme to set for the user.

    Returns:
        JsonResponse: JSON response indicating success or failure of setting the user's theme.
    """
    parameters: dict = json.loads(request.body)
    user = request.user
    theme = parameters.get("theme")

    if not theme:
        return JsonResponse(
            {"error": "No theme provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    if theme not in THEMES:
        return JsonResponse(
            {"error": "Theme not allowed"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        preference = Preference.objects.get(user=user)
        preference.theme = theme
        preference.save()
        return JsonResponse(
            {"message": "Theme updated successfully"}, status=status.HTTP_200_OK
        )
    except Exception as e:
        LOGGER.error(f"Failed to update user theme: {str(e)}")
        return JsonResponse(
            {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


######################## TIMEZONES ########################
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_user_timezone(request: HttpRequest) -> JsonResponse:
    """
    Retrieve the timezone setting for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response with the user's timezone setting on success,
                      or an error message on failure.
    """
    user = request.user
    try:
        timezone = Preference.objects.get(user=user).timezone
        return JsonResponse({"timezone": timezone}, status=status.HTTP_200_OK)
    except Exception as e:
        LOGGER.error(f"Failed to retrieve user timezone: {str(e)}")
        return JsonResponse(
            {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def set_user_timezone(request: HttpRequest) -> JsonResponse:
    """
    Set the timezone for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameter in the body:
            timezone (str): The timezone to set for the user.

    Returns:
        JsonResponse: JSON response indicating success or failure of setting the user's timezone.
    """
    parameters: dict = json.loads(request.body)
    user = request.user
    timezone = parameters.get("timezone")

    if not timezone:
        return JsonResponse(
            {"error": "No timezone provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        preference = Preference.objects.get(user=user)
        preference.timezone = timezone
        preference.save()
        return JsonResponse(
            {"message": "Timezone updated successfully"}, status=status.HTTP_200_OK
        )
    except Exception as e:
        LOGGER.error(f"Failed to update timezone: {str(e)}")
        return JsonResponse(
            {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


######################## ENDPOINTS TO DELETE ALL USELESS, INFORMATIVE, IMPORTANT EMAILS ########################
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def delete_emails(request: HttpRequest) -> JsonResponse:
    """
    Delete emails based on the priority or specific email IDs provided in the request body.

    Args:
        request (HttpRequest): The HTTP request object containing user and body parameters:
            priority (str): Priority level of emails to delete.
            clean (bool): Flag indicating whether to perform a clean deletion.
            emailIds (list[int]): List of specific email IDs to delete.

    Returns:
        JsonResponse: JSON response indicating success or failure of email deletion.
    """
    parameters: dict = json.loads(request.body)
    user = request.user
    priority: str = parameters.get("priority")
    clean: bool = parameters.get("clean")

    if not priority:
        return JsonResponse(
            {"error": "No priority provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    if priority == READ_EMAILS_MARKER:
        emails = Email.objects.filter(user=user, read=True)
        for email in emails:
            email.delete()

        return JsonResponse(
            {"message": "Read emails deleted successfully"}, status=status.HTTP_200_OK
        )

    if clean:
        emails = Email.objects.filter(user=user, priority=priority)
        for email in emails:
            email.delete()

    else:
        email_ids: list[int] = parameters.get("emailIds", [])
        for email_id in email_ids:
            try:
                email = Email.objects.get(user=user, id=email_id)
                email.delete()
            except Email.DoesNotExist:
                pass

    return JsonResponse(
        {"message": "Emails deleted successfully"}, status=status.HTTP_200_OK
    )


######################## CATEGORIES ########################
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_user_categories(request: HttpRequest) -> JsonResponse:
    """
    Retrieve categories associated with the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response containing user's categories or an error message.
    """
    user = request.user
    try:
        categories = Category.objects.filter(user=user)
        serializer = CategoryNameSerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        LOGGER.error(f"Failed to retrieve user categories: {str(e)}")
        return JsonResponse(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["PUT"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def update_category(request: HttpRequest) -> JsonResponse:
    """
    Update an existing category for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameters in the body:
            categoryName (str): The current name of the category to update.
            description (str): The updated description for the category.

    Returns:
        JsonResponse: JSON response containing the updated category data or error messages.
    """
    parameters: dict = json.loads(request.body)
    current_name = parameters.get("categoryName")
    description = parameters.get("description")

    if not current_name:
        return JsonResponse(
            {"error": "No category name provided"}, status=status.HTTP_400_BAD_REQUEST
        )
    if not description:
        return JsonResponse(
            {"error": "No category description provided"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if current_name == DEFAULT_CATEGORY:
        return JsonResponse(
            {"error": f"Cannot modify default category: {DEFAULT_CATEGORY}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if len(current_name) > 50:
        return JsonResponse(
            {"error": "Category name length exceeds 50 characters"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if len(description) > 300:
        return JsonResponse(
            {"error": "Description length exceeds 300 characters"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        category = Category.objects.get(name=current_name, user=request.user)
    except Category.DoesNotExist:
        return JsonResponse(
            {"error": "Category not found"}, status=status.HTTP_400_BAD_REQUEST
        )

    serializer = CategoryNameSerializer(category, data=parameters)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    else:
        LOGGER.error(
            f"Failed to update category '{current_name}' for user ID: {request.user.id}. Errors: {serializer.errors}"
        )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def delete_category(request: HttpRequest) -> JsonResponse:
    """
    Delete a category associated with the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameter in the body:
            categoryName (str): The name of the category to be deleted.

    Returns:
        JsonResponse: JSON response indicating success or failure of deleting the category.
                      Returns an error if the category name is not provided, if attempting to delete the default category,
                      or if the category is not found.
    """
    parameters: dict = json.loads(request.body)
    current_name = parameters.get("categoryName")

    if not current_name:
        return JsonResponse(
            {"error": "No category name provided"}, status=status.HTTP_400_BAD_REQUEST
        )
    if current_name == DEFAULT_CATEGORY:
        return JsonResponse(
            {"error": f"Cannot delete: {DEFAULT_CATEGORY}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        category = Category.objects.get(name=current_name, user=request.user)
    except Category.DoesNotExist:
        return JsonResponse(
            {"error": "Category not found"}, status=status.HTTP_400_BAD_REQUEST
        )

    category.delete()

    return JsonResponse(
        {"message": "Category deleted successfully"}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_rules_linked(request: HttpRequest) -> JsonResponse:
    """
    Retrieves the number of rules linked to a specified category for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameter in the body:
            categoryName (str): The name of the category to retrieve linked rules for.

    Returns:
        JsonResponse: JSON response indicating the number of rules linked to the category.
                      Returns an error if the category name is not provided or if the category is not found.
    """
    parameters: dict = json.loads(request.body)
    current_name = parameters.get("categoryName")
    user = request.user

    if not current_name:
        return JsonResponse(
            {"error": "No category name provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        category = Category.objects.get(name=current_name, user=user)
    except Category.DoesNotExist:
        return JsonResponse(
            {"error": "Category not found"}, status=status.HTTP_400_BAD_REQUEST
        )
    rules = Rule.objects.filter(category=category, user=user)

    return JsonResponse({"nb_rules": len(rules)}, status=status.HTTP_200_OK)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def create_category(request: HttpRequest) -> JsonResponse:
    """
    Create a new category for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the following JSON data:
            name (str): The name of the category to create.
            description (str): The description of the category (up to 300 characters).

    Returns:
        JsonResponse: JSON response with the created category data on success,
                      or error messages on failure (e.g., invalid input, existing category).
    """
    data: dict = json.loads(request.body)
    data["user"] = request.user.id
    name = data.get("name")
    description = data.get("description")

    if not name:
        return JsonResponse(
            {"error": "No category name provided"}, status=status.HTTP_400_BAD_REQUEST
        )
    if not description:
        return JsonResponse(
            {"error": "No category description provided"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if name == DEFAULT_CATEGORY:
        return JsonResponse(
            {"error": f"Cannot create category with name: {DEFAULT_CATEGORY}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if len(name) > 50:
        return JsonResponse(
            {"error": "Category name length must be 50 characters or fewer"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if len(description) > 300:
        return JsonResponse(
            {"error": "Description length must be 300 characters or fewer"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    existing_category = Category.objects.filter(user=request.user, name=name).exists()

    if existing_category:
        return JsonResponse(
            {"error": "Category with this name already exists"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = NewCategorySerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_category_id(request: HttpRequest) -> JsonResponse:
    """
    Retrieve the ID of a category based on its name for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the following JSON data:
            categoryName (str): The name of the category whose ID is to be retrieved.

    Returns:
        JsonResponse: JSON response with the ID of the category on success,
                      or an error message if the category name is not provided or not found.
    """
    parameters: dict = json.loads(request.body)
    user = request.user
    category_name = parameters.get("categoryName")

    if category_name:
        try:
            category = Category.objects.get(name=category_name, user=user)
            return JsonResponse({"id": category.id}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return JsonResponse(
                {"error": "Category does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return JsonResponse(
            {"error": "No category name provided"}, status=status.HTTP_400_BAD_REQUEST
        )


############################# CONTACT ##############################
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_user_contacts(request: HttpRequest) -> JsonResponse:
    """
    Retrieve contacts associated with the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response containing user's contacts or an error message if no contacts are found.
    """
    try:
        user_contacts = Contact.objects.filter(user=request.user)
    except Contact.DoesNotExist:
        return JsonResponse(
            {"error": "No contacts found"}, status=status.HTTP_404_NOT_FOUND
        )

    contacts_serializer = ContactSerializer(user_contacts, many=True)
    return JsonResponse(contacts_serializer.data, safe=False, status=status.HTTP_200_OK)


######################## PROMPT ENGINEERING ########################
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def find_user_view_ai(request: HttpRequest) -> JsonResponse:
    """Searches for emails in the user's mailbox based on the provided search query in both the subject and body."""
    search_query = request.GET.get("query")

    if search_query:
        main_list, cc_list, bcc_list = claude.extract_contacts_recipients(search_query)

        if not main_list:
            return JsonResponse(
                {"error": "Invalid input or query not about email recipients"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_contacts = Contact.objects.filter(user=request.user)
        except Contact.DoesNotExist:
            return JsonResponse(
                {"error": "No contacts found"}, status=status.HTTP_404_NOT_FOUND
            )

        contacts_serializer = ContactSerializer(user_contacts, many=True)

        # TODO: check for performance (should be fast)
        def transform_list_of_dicts(list_of_dicts):
            new_dict = {}

            for item in list_of_dicts:
                new_dict[item["username"]] = item["email"]

            return new_dict

        contacts_dict = transform_list_of_dicts(contacts_serializer.data)

        def find_emails(input_str, contacts_dict):
            # Split input_str into substrings if it contains spaces
            input_substrings = input_str.split() if " " in input_str else [input_str]

            # Convert input substrings to lowercase for case-insensitive matching
            input_substrings_lower = [sub_str.lower() for sub_str in input_substrings]

            # List comprehension to find matching emails
            matching_emails = [
                email
                for name, email in contacts_dict.items()
                if all(sub_str in name.lower() for sub_str in input_substrings_lower)
            ]

            # Return the list of matching emails
            return matching_emails

        def find_emails_for_recipients(recipient_list, contacts_dict) -> dict:
            """Find matching emails for a list of recipients."""
            recipients_with_emails = []

            # Iterate through recipient_list to find matches
            for recipient_name in recipient_list:
                matching_emails = find_emails(recipient_name, contacts_dict)

                # Append the result as a dictionary
                if len(matching_emails) > 0:
                    recipients_with_emails.append(
                        {"username": recipient_name, "email": matching_emails}
                    )

            return recipients_with_emails

        # Find matching emails for each list of recipients
        main_recipients_with_emails = find_emails_for_recipients(
            main_list, contacts_dict
        )
        cc_recipients_with_emails = find_emails_for_recipients(cc_list, contacts_dict)
        bcc_recipients_with_emails = find_emails_for_recipients(bcc_list, contacts_dict)

        return JsonResponse(
            {
                "main_recipients": main_recipients_with_emails,
                "cc_recipients": cc_recipients_with_emails,
                "bcc_recipients": bcc_recipients_with_emails,
            },
            status=status.HTTP_200_OK,
        )
    else:
        return JsonResponse(
            {"error": "Failed to authenticate or no search query provided"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# ----------------------- REDACTION -----------------------#
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def new_email_ai(request: HttpRequest) -> JsonResponse:
    """
    Return an AI-generated email subject and content based on input data.

    Args:
        request (HttpRequest): The HTTP request object containing input data in the body.

    Returns:
        JsonResponse: JSON response with generated email subject and content on success,
                      or error messages on failure.
    """
    data: dict = json.loads(request.body)
    serializer = NewEmailAISerializer(data=data)

    if serializer.is_valid():
        input_data = serializer.validated_data["input_data"]
        length = serializer.validated_data["length"]
        formality = serializer.validated_data["formality"]

        subject_text, mail_text = claude.generate_email(input_data, length, formality)

        return JsonResponse({"subject": subject_text, "mail": mail_text})
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def improve_email_writing(request: HttpRequest) -> JsonResponse:
    """
    Enhance the subject and body of an email in French, focusing on both quantity and quality improvements,
    while retaining key details from the original version.

    Args:
        request (HttpRequest): The HTTP request object containing data to correct the email.
            Expects a JSON body with fields:
                email_body (str): The current body of the email.
                email_subject (str): The current subject of the email.

    Returns:
        JsonResponse: JSON response containing the improved email subject and body,
            or errors if the input data is invalid.
    """
    data: dict = json.loads(request.body)
    serializer = EmailCorrectionSerializer(data=data)

    if serializer.is_valid():
        email_body = serializer.validated_data["email_body"]
        email_subject = serializer.validated_data["email_subject"]

        email_body, subject_text = claude.improve_email_writing(
            email_body, email_subject
        )
        return JsonResponse({"subject": subject_text, "email_body": email_body})
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def correct_email_language(request: HttpRequest) -> JsonResponse:
    """
    Corrects spelling and grammar mistakes in the email subject and body based on user's request.

    Args:
        request (HttpRequest): HTTP request object containing data to correct the email.
            Expects JSON body with:
                email_subject (str): The subject of the email to be corrected.
                email_body (str): The body of the email to be corrected.

    Returns:
        JsonResponse: JSON response containing corrected email subject, body, and the number of corrections made.
                      If there are validation errors in the serializer, returns a JSON response with the errors
                      and status HTTP 400 Bad Request.
    """
    data: dict = json.loads(request.body)
    serializer = EmailCorrectionSerializer(data=data)

    if serializer.is_valid():
        email_subject = serializer.validated_data["email_subject"]
        email_body = serializer.validated_data["email_body"]

        corrected_subject, corrected_body, num_corrections = (
            claude.correct_mail_language_mistakes(email_body, email_subject)
        )
        return JsonResponse(
            {
                "corrected_subject": corrected_subject,
                "corrected_body": corrected_body,
                "num_corrections": num_corrections,
            }
        )
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def check_email_copywriting(request: HttpRequest) -> JsonResponse:
    """
    Checks and provides feedback on the email copywriting based on the user's request.

    Args:
        request (HttpRequest): HTTP request object containing data to check the email copywriting.
            Expects JSON body with:
                email_subject (str): The subject of the email to be checked.
                email_body (str): The body of the email to be checked.

    Returns:
        JsonResponse: JSON response containing feedback on the email copywriting.
                      If there are validation errors in the serializer, returns a JSON response with the errors
                      and status HTTP 400 Bad Request.
    """
    data: dict = json.loads(request.body)
    serializer = EmailCopyWritingSerializer(data=data)

    if serializer.is_valid():
        email_subject = serializer.validated_data["email_subject"]
        email_body = serializer.validated_data["email_body"]

        feedback_copywriting = claude.improve_email_copywriting(
            email_body, email_subject
        )
        return JsonResponse({"feedback_copywriting": feedback_copywriting})
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------- ANSWER -----------------------#
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def generate_email_response_keywords(request: HttpRequest) -> JsonResponse:
    """
    Generates response keywords based on the provided email subject and content.

    Args:
        request (HttpRequest): HTTP request object containing data to generate response keywords.
            Expects JSON body with:
                email_subject (str): The subject of the email for which response keywords are to be generated.
                email_content (str): The content/body of the email for which response keywords are to be generated.

    Returns:
        JsonResponse: JSON response containing response keywords generated from the email subject and content.
                      If there are validation errors in the serializer, returns a JSON response with the errors
                      and status HTTP 400 Bad Request.
    """
    data: dict = json.loads(request.body)
    serializer = EmailProposalAnswerSerializer(data=data)

    if serializer.is_valid():
        email_subject = serializer.validated_data["email_subject"]
        email_content = serializer.validated_data["email_content"]

        response_keywords = claude.generate_response_keywords(
            email_subject, email_content
        )
        return JsonResponse({"response_keywords": response_keywords})
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def generate_email_answer(request: HttpRequest) -> JsonResponse:
    """
    Generates an automated response to an email based on its subject, content, and user instructions.

    Args:
        request (HttpRequest): HTTP request object containing data to generate an email response.
            Expects JSON body with:
                email_subject (str): The subject of the email for which the response is generated.
                email_content (str): The content/body of the email for which the response is generated.
                response_type (str): User instruction indicating how the response should be generated.

    Returns:
        JsonResponse: JSON response containing the generated email response.
                      If there are validation errors in the serializer, returns a JSON response with the errors
                      and status HTTP 400 Bad Request.
    """
    data: dict = json.loads(request.body)
    serializer = EmailGenerateAnswer(data=data)

    if serializer.is_valid():
        email_subject = serializer.validated_data["email_subject"]
        email_content = serializer.validated_data["email_content"]
        user_instruction = serializer.validated_data["response_type"]

        email_answer = claude.generate_email_response(
            email_subject, email_content, user_instruction
        )

        return JsonResponse({"email_answer": email_answer})
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------- REPLY LATER -----------------------#
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_answer_later_emails(request: HttpRequest) -> JsonResponse:
    """
    Retrieve emails flagged for answering later by the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the user information.

    Returns:
        JsonResponse: JSON response containing the list of emails flagged for answering later,
                      grouped by priority, or an error message if retrieval fails.
    """
    try:
        user = request.user
        emails = Email.objects.filter(user=user, answer_later=True).prefetch_related(
            "bulletpoint_set", "sender", "category"
        )

        emails = emails.annotate(
            has_rule=Exists(Rule.objects.filter(sender=OuterRef("sender"), user=user))
        )
        rule_id_subquery = Rule.objects.filter(
            sender=OuterRef("sender"), user=user
        ).values("id")[:1]
        emails = emails.annotate(rule_id=Subquery(rule_id_subquery))

        formatted_data = defaultdict(list)

        for email in emails:
            email_data = {
                "id": email.id,
                "id_provider": email.provider_id,
                "email": email.sender.email,
                "name": email.sender.name,
                "description": email.email_short_summary,
                "details": [
                    {"id": bp.id, "text": bp.content}
                    for bp in email.bulletpoint_set.all()
                ],
                "rule": email.has_rule,
                "rule_id": email.rule_id,
            }
            formatted_data[email.priority].append(email_data)

        return JsonResponse(formatted_data, status=status.HTTP_200_OK)

    except Exception as e:
        LOGGER.error(f"Error fetching answer-later emails: {str(e)}")
        return JsonResponse(
            {"error": "Failed to retrieve answer-later emails."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


######################## DATABASE OPERATIONS ########################
# ----------------------- CREDENTIALS UPDATE-----------------------#
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def update_username(request: HttpRequest) -> JsonResponse:
    """
    Update the username for the authenticated user.

    Args:
        request (HttpRequest): HTTP request object containing the new username in the request body.
            Expects JSON body with:
                username (str): The new username to update for the authenticated user.

    Returns:
        JsonResponse: Either {"success": "Username updated successfully."} if the update is successful,
                    or {"error": "Details of the specific error."} if there's an issue with the update.
    """
    parameters: dict = json.loads(request.body)
    user = request.user
    new_username = parameters.get("username")

    if not new_username:
        return JsonResponse(
            {"error": "No new username provided."}, status=status.HTTP_400_BAD_REQUEST
        )
    elif User.objects.filter(username=new_username).exists():
        return JsonResponse(
            {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
        )
    elif " " in new_username:
        return JsonResponse(
            {"error": "Username must not contain spaces"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.username = new_username
    user.save()

    return JsonResponse({"success": "Username updated successfully."})


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def update_password(request: HttpRequest) -> JsonResponse:
    """
    Update the password for the authenticated user.

    Args:
        request (HttpRequest): HTTP request object containing the new password in the request body.
            Expects JSON body with:
                password (str): The new password to update for the authenticated user.

    Returns:
        JsonResponse: Either {"success": "Password updated successfully."} if the update is successful,
                    or {"error": "Details of the specific error."} if there's an issue with the update.
    """
    parameters: dict = json.loads(request.body)
    user = request.user
    new_password = parameters.get("password")

    if not new_password:
        return JsonResponse(
            {"error": "No new password provided."}, status=status.HTTP_400_BAD_REQUEST
        )
    elif not (8 <= len(new_password) <= 32):
        return JsonResponse(
            {"error": "Password length must be between 8 and 32 characters"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.set_password(new_password)
    user.save()

    return JsonResponse({"success": "Password updated successfully."})


# ----------------------- ACCOUNT-----------------------#
@api_view(["DELETE"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def delete_account(request):
    """Removes the user from the database"""
    user = request.user

    try:
        unsubscribe_listeners(user)
        user.delete()
        return JsonResponse(
            {"message": "User successfully deleted"}, status=status.HTTP_200_OK
        )

    except Exception as e:
        LOGGER.error(f"Error when deleting account {user.id}: {str(e)}")
        return JsonResponse({"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)


def unsubscribe_listeners(user, email=None):
    social_apis = SocialAPI.objects.filter(user=user)
    if social_apis.exists():
        for social_api in social_apis:
            if social_api.type_api == "google":
                for i in range(MAX_RETRIES):
                    if google_api.unsubscribe_from_email_notifications(
                        user, social_api.email
                    ):
                        break
                    else:
                        LOGGER.critical(
                            f"[Attempt n°{i+1}] Failed to unsubscribe from Google: {social_api.email}"
                        )
                    context = {
                        "title": "Critical Alert: Google Unsubscription Failure",
                        "attempt_number": i + 1,
                        "subscription_id": social_api.email,
                        "email_provider": GOOGLE_PROVIDER,
                        "user": user,
                    }
                    email_html = render_to_string("unsubscribe_failure.html", context)
                    send_mail(
                        subject="Critical Alert: Google Unsubscription Failure",
                        message="",
                        recipient_list=ADMIN_EMAIL_LIST,
                        from_email=EMAIL_NO_REPLY,
                        html_message=email_html,
                        fail_silently=False,
                    )

    if email:
        microsoft_listeners = MicrosoftListener.objects.filter(user=user, email=email)
    else:
        microsoft_listeners = MicrosoftListener.objects.filter(user=user)

    if microsoft_listeners.exists():
        for listener in microsoft_listeners:
            for i in range(MAX_RETRIES):
                if microsoft_api.delete_subscription(
                    user, listener.email, listener.subscription_id
                ):
                    break
                else:
                    LOGGER.critical(
                        f"[Attempt n°{i+1}] Failed to unsubscribe from Microsoft: {listener.subscription_id}"
                    )
                    context = {
                        "title": "Critical Alert: Microsoft Unsubscription Failure",
                        "attempt_number": i + 1,
                        "subscription_id": listener.subscription_id,
                        "email_provider": MICROSOFT_PROVIDER,
                        "user": user,
                    }
                    email_html = render_to_string("unsubscribe_failure.html", context)
                    send_mail(
                        subject="Critical Alert: Microsoft Unsubscription Failure",
                        message="",
                        recipient_list=ADMIN_EMAIL_LIST,
                        from_email=EMAIL_NO_REPLY,
                        html_message=email_html,
                        fail_silently=False,
                    )


# ----------------------- RULES -----------------------#
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def set_rule_block_for_sender(request, email_id):
    user = request.user

    # Check if the email belongs to the authenticated user
    email = get_object_or_404(Email, user=user, id=email_id)

    # Check if there's a rule for this sender and user, create with block=True if it doesn't exist
    rule, created = Rule.objects.get_or_create(
        sender=email.sender, user=user, defaults={"block": True}, priority=""
    )

    # If the rule already existed, update the block field
    if not created:
        rule.block = True
        rule.save()

    serializer = RuleBlockUpdateSerializer(rule)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_user_rules(request):
    user_rules = Rule.objects.filter(user=request.user)
    rules_data = []

    for rule in user_rules:
        rule_serializer = RuleSerializer(rule)
        rule_data = rule_serializer.data

        # Manually add category name and sender details
        category_name = rule.category.name if rule.category else None
        sender_name = rule.sender.name if rule.sender else None
        sender_email = rule.sender.email if rule.sender else None

        rule_data["category_name"] = category_name
        rule_data["sender_name"] = sender_name
        rule_data["sender_email"] = sender_email

        rules_data.append(rule_data)

    return JsonResponse(rules_data, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_user_rule_by_id(request, id_rule):
    try:
        # Retrieve the rule with the given id that belongs to the user
        user_rule = Rule.objects.get(id=id_rule, user=request.user)

    except Rule.DoesNotExist:
        return JsonResponse(
            {"error": "Rule not found"}, status=status.HTTP_404_NOT_FOUND
        )

    rule_serializer = RuleSerializer(user_rule)
    rule_data = rule_serializer.data

    # Manually add category name and sender details if they exist
    category_name = user_rule.category.name if user_rule.category else None
    sender_name = user_rule.sender.name if user_rule.sender else None
    sender_email = user_rule.sender.email if user_rule.sender else None

    rule_data["category_name"] = category_name
    rule_data["sender_name"] = sender_name
    rule_data["sender_email"] = sender_email

    return JsonResponse(rule_data)


@api_view(["DELETE"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def delete_user_rule_by_id(request, id_rule):
    try:
        # Retrieve the rule with the given id that belongs to the user
        user_rule = Rule.objects.get(id=id_rule, user=request.user)

    except Rule.DoesNotExist:
        return JsonResponse(
            {"error": "Rule not found"}, status=status.HTTP_404_NOT_FOUND
        )

    user_rule.delete()

    return JsonResponse({"message": "Rule deleted successfully"})


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def create_user_rule(request):
    data = request.data
    user = request.user

    rule = Rule.objects.filter(sender_id=data["sender"], user=user)
    if rule.exists():
        return JsonResponse(
            {"error": "A rule already exists for that sender"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = RuleSerializer(data=request.data, context={"user": user})
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    else:
        LOGGER.error(f"Serializer errors in create_user_rule: {serializer.errors}")
        return JsonResponse(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["PUT"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def update_user_rule(request):
    try:
        rule = Rule.objects.get(id=request.data.get("id"), user=request.user)
    except Rule.DoesNotExist:
        return JsonResponse(
            {"error": "Rule not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = RuleSerializer(
        rule, data=request.data, partial=True, context={"user": request.user}
    )
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    else:
        LOGGER.error(f"Serializer errors in update_user_rule: {serializer.errors}")
        return JsonResponse(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


# ----------------------- USER -----------------------#
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def check_sender_for_user(request):
    email = request.data.get("email")

    try:
        sender = Sender.objects.get(email=email)
        return JsonResponse(
            {"exists": True, "sender_id": sender.id}, status=status.HTTP_200_OK
        )

    except ObjectDoesNotExist:
        return JsonResponse({"exists": False}, status=status.HTTP_200_OK)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_user_details(request):
    """Returns the username"""
    return JsonResponse({"username": request.user.username})


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_emails_linked(request):
    """Returns the list of linked emails with the user account."""

    user = request.user

    try:
        social_apis = SocialAPI.objects.filter(user=user)
        emails_inked = []
        for social_api in social_apis:
            emails_inked.append(
                {"email": social_api.email, "type_api": social_api.type_api}
            )

        return JsonResponse(emails_inked, safe=False, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def unlink_email(request):
    """Unlinks the email and deletes all stored emails associated with the user account."""
    user = request.user
    email = request.data.get("email")

    try:
        social_api = SocialAPI.objects.get(user=user, email=email)
        unsubscribe_listeners(user, email)
        social_api.delete()
        return JsonResponse(
            {"message": "Email unlinked successfully!"}, status=status.HTTP_202_ACCEPTED
        )
    except SocialAPI.DoesNotExist:
        return JsonResponse(
            {"error": "SocialAPI entry not found"}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def link_email(request):
    """Links the email with the user account."""

    user = request.user
    type_api = request.data.get("type_api")
    code = request.data.get("code")
    user_description = request.data.get("user_description")

    # Checks if the authorization code is valid
    authorization_result = validate_code_link_email(type_api, code)

    if "error" in authorization_result:
        # TODO: add clean LOGGER with given error message
        return JsonResponse(
            {"error": authorization_result["error"]}, status=status.HTTP_400_BAD_REQUEST
        )

    # Extract tokens and email from the authorization result
    access_token = authorization_result["access_token"]
    refresh_token = authorization_result["refresh_token"]
    email = authorization_result["email"]
    refresh_token_encrypted = security.encrypt_text(
        ENCRYPTION_KEYS["SocialAPI"]["refresh_token"], refresh_token
    )

    # Check email requirements
    if email:
        if " " in email:
            return JsonResponse(
                {"error": "Email address must not contain spaces"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            social_api = SocialAPI.objects.create(
                user=user,
                email=email,
                type_api=type_api,
                user_description=user_description,
                access_token=access_token,
                refresh_token=refresh_token_encrypted,
            )
        except IntegrityError:
            return JsonResponse(
                {"error": "Email address already used by another account"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return JsonResponse(
            {"error": "No email received"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Asynchronous function to store all contacts
    try:
        if type_api == "google":
            threading.Thread(
                target=google_api.set_all_contacts, args=(user, email)
            ).start()
        elif type_api == "microsoft":
            threading.Thread(
                target=microsoft_api.set_all_contacts, args=(access_token, user)
            ).start()
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Subscribe to listeners
    subscribed = subscribe_listeners(type_api, user, email)
    if subscribed:
        return JsonResponse(
            {"message": "Email linked to account successfully!"},
            status=status.HTTP_201_CREATED,
        )
    else:
        social_api.delete()

    return JsonResponse(
        {"error": "Could not subscribe to listener"}, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def search_emails_ai(request):
    """Searches emails using AI interpretation of user query."""
    user = request.user
    data = request.data
    emails = data["emails"]
    query = data["query"]
    search_params: dict = claude.search_emails(query)
    result = {}

    def append_to_result(
        provider: str,
        email: str,
        data: list,
    ):
        if len(data) > 0:
            if provider not in result:
                result[provider] = {}
            result[provider][email] = data

    # TODO: check if max_results correspond to subscription !!!

    max_results: int = search_params["max_results"]
    from_addresses: list = search_params["from"]
    to: list = search_params["to"]
    subject: str = search_params["subject"]
    body: str = search_params["body"]
    filenames: list = search_params["filenames"]
    date_from: str = search_params["date_from"]
    keywords: list = search_params["keywords"]
    search_in: dict = search_params["search_in"]

    for email in emails:
        social_api = SocialAPI.objects.get(email=email)
        type_api = social_api.type_api

        if type_api == "google":
            services = google_api.authenticate_service(user, email)
            search_result = threading.Thread(
                target=append_to_result,
                args=(
                    GOOGLE_PROVIDER,
                    email,
                    google_api.search_emails_ai(
                        services,
                        max_results=max_results,
                        filenames=filenames,
                        from_addresses=from_addresses,
                        to_addresses=to,
                        subject=subject,
                        body=body,
                        keywords=keywords,
                        date_from=date_from,
                        search_in=search_in,
                    ),
                ),
            )

        elif type_api == "microsoft":
            access_token = microsoft_api.refresh_access_token(
                microsoft_api.get_social_api(user, email)
            )
            search_result = threading.Thread(
                target=append_to_result,
                args=(
                    MICROSOFT_PROVIDER,
                    email,
                    microsoft_api.search_emails_ai(
                        access_token,
                        max_results=max_results,
                        filenames=filenames,
                        from_addresses=from_addresses,
                        to_addresses=to,
                        subject=subject,
                        body=body,
                        keywords=keywords,
                        date_from=date_from,
                        search_in=search_in,
                    ),
                ),
            )

        search_result.start()
        search_result.join()

    return JsonResponse(result, status=status.HTTP_200_OK)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def search_emails(request):
    user = request.user
    data: dict = request.data
    emails: list = data["emails"]
    max_results: int = data["max_results"]
    query: str = data["query"]
    file_extensions: list = data["file_extensions"]
    advanced: bool = data["advanced"]
    from_addresses: list = data["from_addresses"]
    to_addresses: list = data["to_addresses"]
    subject: str = data["subject"]
    body: str = data["body"]
    date_from: str = data["date_from"]
    search_in: dict = data["search_in"]

    # TODO: check if max_results correspond to subscription !!!

    def append_to_result(provider: str, email: str, data: list):
        if len(data) > 0:
            if provider not in result:
                result[provider] = {}
            result[provider][email] = data

    result = {}
    for email in emails:
        social_api = SocialAPI.objects.get(email=email)
        type_api = social_api.type_api

        if type_api == "google":
            services = google_api.authenticate_service(user, email)
            search_result = threading.Thread(
                target=append_to_result(
                    GOOGLE_PROVIDER,
                    email,
                    google_api.search_emails_manually(
                        services,
                        query,
                        max_results,
                        file_extensions,
                        advanced,
                        search_in,
                        from_addresses,
                        to_addresses,
                        subject,
                        body,
                        date_from,
                    ),
                )
            )
        elif type_api == "microsoft":
            access_token = microsoft_api.refresh_access_token(
                microsoft_api.get_social_api(user, email)
            )
            search_result = threading.Thread(
                target=append_to_result(
                    MICROSOFT_PROVIDER,
                    email,
                    microsoft_api.search_emails_manually(
                        access_token,
                        query,
                        max_results,
                        file_extensions,
                        advanced,
                        search_in,
                        from_addresses,
                        to_addresses,
                        subject,
                        body,
                        date_from,
                    ),
                )
            )
        search_result.start()
        search_result.join()

    return JsonResponse(result, status=status.HTTP_200_OK)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def search_tree_knowledge(request: HttpRequest):
    """
    Searches emails using AI interpretation of user query.
    """
    try:
        user = request.user
        user_id = user.id
        parameters: dict = json.loads(request.body)
        question = parameters.get("question")

        if not question:
            return JsonResponse(
                {"error": "Question is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        search = Search(user_id, question)
        if not search.can_answer():
            return JsonResponse(
                {"message": "Not have enough data"},
                status=status.HTTP_200_OK,
            )

        # TODO: debug if Ao fails with little data - if so: improve prompt engineering
        selected_categories = search.get_selected_categories()
        keypoints = search.get_keypoints(selected_categories)

        if not selected_categories or not keypoints:
            return JsonResponse(
                {"message": "Not have enough data"},
                status=status.HTTP_200_OK,
            )

        language = Preference.objects.get(user=user).language
        answer = search.get_answer(keypoints, language)
        emails = []

        for category in keypoints:
            for organization in keypoints[category]:
                for topic in keypoints[category][organization]:
                    emails.extend(
                        search.knowledge_tree[category]["organizations"][organization][
                            "topics"
                        ][topic]["emails"]
                    )

        answer["emails"] = emails

        return JsonResponse({"answer": answer}, status=status.HTTP_200_OK)

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON format"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse(
            {"error": "An error occurred while processing your request"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def update_user_description(request):
    """Updates the user desctiption of the given email."""
    data = request.data
    user = request.user
    email = data.get("email")
    user_description = data["user_description"]

    if email:
        social_api = SocialAPI.objects.get(user=user, email=email)
        social_api.user_description = user_description
        social_api.save()
        return JsonResponse(
            {"message": "User description updated"}, status=status.HTTP_200_OK
        )
    else:
        return JsonResponse(
            {"error": "No email provided"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_user_description(request):
    """Retrieves user description of the given email."""
    data = request.data
    user = request.user
    email = data.get("email")

    if email:
        social_api = SocialAPI.objects.get(user=user, email=email)
        return JsonResponse(
            {"data": social_api.user_description}, status=status.HTTP_200_OK
        )
    else:
        return JsonResponse(
            {"error": "No email provided"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def create_sender(request):
    """Create a new sender associated with the authenticated user"""
    serializer = SenderSerializer(data=request.data)
    data = request.data

    if serializer.is_valid():
        sender = Sender.objects.create(email=data["email"], name=data["name"])
        return JsonResponse({"id": sender.id}, status=status.HTTP_201_CREATED)
    else:
        LOGGER.error(f"Serializer errors in create_sender: {serializer.errors}")
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def delete_email(request, email_id):
    try:
        user = request.user
        email = get_object_or_404(Email, user=user, id=email_id)
        social_api = email.social_api
        type_api = social_api.type_api
        provider_id = email.provider_id
        email.delete()

        if type_api == "google":
            result = google_api.delete_email(user, social_api.email, provider_id)
        elif type_api == "microsoft":
            result = microsoft_api.delete_email(provider_id, social_api)

        if result.get("message", "") == "Email moved to trash successfully!":
            return JsonResponse(
                {"message": "Email deleted successfully"}, status=status.HTTP_200_OK
            )
        else:
            return JsonResponse(
                {"error": result.get("error")}, status=status.HTTP_400_BAD_REQUEST
            )

    except Exception as e:
        LOGGER.error(f"Error when deleting email: {str(e)}")
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ----------------------- CREDENTIALS AVAILABILITY -----------------------#
@api_view(["GET"])
@permission_classes([AllowAny])
def check_username(request):
    """Verify if the username is available"""
    username = request.headers.get("username")

    if User.objects.filter(username=username).exists():
        return JsonResponse({"available": False}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"available": True}, status=status.HTTP_200_OK)


# ----------------------- EMAIL -----------------------#
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_first_email(request: HttpRequest):
    """Returns the first email associated with the user in database."""
    user = request.user
    social_apis = SocialAPI.objects.filter(user=user)
    email = social_apis.first().email

    return Response({"email": email}, status=200)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_mail_by_id(request):
    user = request.user
    mail_id = request.GET.get("email_id")

    email = get_object_or_404(Email, user=user, provider_id=mail_id)
    social_api = email.social_api
    email_user = social_api.email
    type_api = social_api.type_api

    if mail_id is not None:
        if type_api == "google":
            services = google_api.authenticate_service(user, email_user)
            subject, from_name, decoded_data, cc, bcc, email_id, date, _ = (
                google_api.get_mail(services, None, mail_id)
            )
        elif type_api == "microsoft":
            access_token = microsoft_api.refresh_access_token(
                microsoft_api.get_social_api(user, email_user)
            )
            subject, from_name, decoded_data, cc, bcc, email_id, date, _ = (
                microsoft_api.get_mail(access_token, None, mail_id)
            )

        if cc:
            cc = tuple(item for item in cc if item is not None)
        if bcc:
            bcc = tuple(item for item in bcc if item is not None)

        return JsonResponse(
            {
                "message": "Authentication successful",
                "email": {
                    "subject": subject,
                    "from_name": from_name,
                    "decoded_data": decoded_data,
                    "cc": cc,
                    "bcc": bcc,
                    "email_id": email_id,
                    "date": date,
                    "email_receiver": email_user,
                },
            },
            status=status.HTTP_200_OK,
        )
    else:
        return JsonResponse(
            {"error": "Failed to authenticate"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def set_email_read(request, email_id):
    """Mark a specific email as read for the authenticated user"""
    user = request.user

    email = get_object_or_404(Email, user=user, id=email_id)
    email.read = True
    email.read_date = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)
    email.save()

    social_api = email.social_api
    if social_api.type_api == "google":
        google_api.set_email_read(user, social_api.email, email.provider_id)
    elif social_api.type_api == "microsoft":
        microsoft_api.set_email_read(social_api, email.provider_id)

    serializer = EmailReadUpdateSerializer(email)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def set_email_undread(request, email_id):
    """Mark a specific email as read for the authenticated user"""
    user = request.user

    email = get_object_or_404(Email, user=user, id=email_id)
    email.read = False
    email.read_date = None
    email.save()

    social_api = email.social_api
    if social_api.type_api == "google":
        google_api.set_email_unread(user, social_api.email, email.provider_id)
    elif social_api.type_api == "microsoft":
        microsoft_api.set_email_unread(social_api, email.provider_id)

    serializer = EmailReadUpdateSerializer(email)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def set_email_reply_later(request, email_id):
    """Mark a specific email for later reply for the authenticated user"""
    user = request.user
    email = get_object_or_404(Email, user=user, id=email_id)
    email.answer_later = True
    email.save()

    serializer = EmailReplyLaterUpdateSerializer(email)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def set_email_not_reply_later(request, email_id):
    """Unmark a specific email for later reply."""
    user = request.user
    email = get_object_or_404(Email, user=user, id=email_id)
    email.answer_later = False
    email.save()

    serializer = EmailReplyLaterUpdateSerializer(email)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_user_emails(request):
    """Retrieves and formats user emails grouped by category and priority"""
    user = request.user
    emails = Email.objects.filter(user=user).prefetch_related(
        "category", "bulletpoint_set", "cc_senders", "bcc_senders", "attachments"
    )
    emails = emails.annotate(
        has_rule=Exists(Rule.objects.filter(sender=OuterRef("sender"), user=user))
    )
    rule_id_subquery = Rule.objects.filter(sender=OuterRef("sender"), user=user).values(
        "id"
    )[:1]
    emails = emails.annotate(rule_id=Subquery(rule_id_subquery))

    formatted_data = defaultdict(lambda: defaultdict(list))

    one_third = len(emails) // 3
    emails1 = emails[:one_third]
    emails2 = emails[one_third : 2 * one_third]
    emails3 = emails[2 * one_third :]

    def process_emails(email_list: list[Email]):
        for email in email_list:
            if email.read_date:
                current_datetime_utc = datetime.datetime.now().replace(
                    tzinfo=datetime.timezone.utc
                )
                delta_time = current_datetime_utc - email.read_date

                # Delete read email older than 1 week
                if delta_time > datetime.timedelta(weeks=1):
                    email.delete()
                    continue

            email_date = email.date.date() if email.date else None
            email_time = email.date.strftime("%H:%M") if email.date else None

            email_data = {
                "id": email.id,
                "id_provider": email.provider_id,
                "email": email.sender.email,
                "subject": email.subject,
                "name": email.sender.name,
                "description": email.email_short_summary,
                "html_content": email.html_content,
                "details": [
                    {"id": bp.id, "text": bp.content}
                    for bp in email.bulletpoint_set.all()
                ],
                "cc": [
                    {"email": cc.email, "name": cc.name}
                    for cc in email.cc_senders.all()
                ],
                "bcc": [
                    {"email": bcc.email, "name": bcc.name}
                    for bcc in email.bcc_senders.all()
                ],
                "read": email.read,
                "rule": email.has_rule,
                "rule_id": email.rule_id,
                "answer_later": email.answer_later,
                "web_link": email.web_link,
                "has_attachments": email.has_attachments,
                "attachments": [
                    {
                        "attachmentName": attachment.name,
                        "attachmentId": attachment.id_api,
                    }
                    for attachment in email.attachments.all()
                ],
                "date": email_date,
                "time": email_time,
            }

            formatted_data[email.category.name][email.priority].append(email_data)

    # Multi-threading for faster computation with large amount of emails
    thread1 = threading.Thread(target=process_emails, args=(emails1,))
    thread2 = threading.Thread(target=process_emails, args=(emails2,))
    thread3 = threading.Thread(target=process_emails, args=(emails3,))

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

    # Ensuring all priorities are present for each category
    all_priorities = {"Important", "Information", "Useless"}
    for category in formatted_data:
        for priority in all_priorities:
            formatted_data[category].setdefault(priority, [])

    return JsonResponse(formatted_data, status=status.HTTP_200_OK)


# ----------------------- EMAIL ATTACHMENT -----------------------#
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def retrieve_attachment_data(request, email_id, attachment_id):
    """API endpoint to retrieve email attachment data"""
    user = request.user
    email = get_object_or_404(Email, user=user, id=email_id)
    social_api = email.social_api

    if social_api.type_api == "google":
        print("SOCIAL API :", social_api.email, "PROVIDER ID :", email.provider_id)
        attachment_data = google_api.get_attachment_data(
            user, social_api.email, email.provider_id, attachment_id
        )
    elif social_api.type_api == "microsoft":
        # TO DO
        print("TO DO : ERROR")

    return JsonResponse(attachment_data, status=status.HTTP_200_OK)


####################################################################
######################## UNDER CONSTRUCTION ########################
####################################################################
def create_subscription(user, stripe_plan_id, email="nothingForNow"):
    stripe_customer = stripe.Customer.create(email=email)
    stripe_customer_id = stripe_customer.id

    stripe_subscription = stripe.Subscription.create(
        customer=stripe_customer_id,
        items=[
            {
                "plan": stripe_plan_id,
            },
        ],
        trial_period_days=30,
    )

    # Creation of default subscription plan
    Subscription.objects.create(
        user=user,
        plan="start_plan",
        stripe_subscription_id=stripe_subscription.id,
        end_date=datetime.datetime.now() + datetime.timedelta(days=30),
        billing_interval=None,
        amount=STRIPE_PRICES[stripe_plan_id],
    )


# ----------------------- PASSWORD RESET CONFIGURATION -----------------------#
@api_view(["POST"])
@permission_classes([AllowAny])
def generate_reset_token(request):
    """Sends an email with the reset password link."""

    email = request.data.get("email")
    social_api = SocialAPI.objects.filter(email=email)
    if social_api.exists() == False:
        return JsonResponse(
            {"error": "Email address is not linked with an account"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    token = PasswordResetTokenGenerator().make_token(social_api.first().user)
    reset_link = f"{BASE_URL_MA}reset_password/?token={token}"
    context = {"reset_link": reset_link, "email": EMAIL_NO_REPLY}
    email_html = render_to_string("password_reset_email.html", context)

    try:
        send_mail(
            subject="Password Reset for MailAssistant",
            message="",
            recipient_list=[email],
            from_email=EMAIL_NO_REPLY,
            html_message=email_html,
            fail_silently=False,
        )
        return JsonResponse(
            {"message": "Email sent successfully!"}, status=status.HTTP_200_OK
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([AllowAny])
def reset_password(request):
    """Checks if the token is valid and reset the password of user"""
    ...


######################## STRIPE ########################
@csrf_exempt
def receive_payment_notifications(request):
    """Handles Stripe notifications"""

    if request.method == "POST":
        payload = request.body
        sig_header = request.headers["Stripe-Signature"]

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_SECRET_KEY
            )
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.WebhookSignature as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if event["type"] == "invoice.payment_succeeded":
            # TODO: Handle successful + informations for customer
            # use create_subscription
            ...  # data base operations
            # Subscription.objects.get(...)
            redirect(STRIPE_PAYMENT_SUCCESS_URL)
        elif event["type"] == "invoice.payment_failed":
            # TODO: Handle failed payment + add error message
            redirect(STRIPE_PAYMENT_FAILED_URL)
        else:
            return JsonResponse(
                {"error": "Unhandled event type"}, status=status.HTTP_400_BAD_REQUEST
            )

        return JsonResponse({"message": "Received"}, status=status.HTTP_200_OK)
    else:
        return JsonResponse(
            {"error": "Invalid request method"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


# ----------------------- BACKGROUND COLOR-----------------------#
# TODO: DELETE
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_user_bg_color(request):
    try:
        preferences = Preference.objects.get(user=request.user)
        serializer = PreferencesSerializer(preferences)
        return JsonResponse(serializer.data)

    except Preference.DoesNotExist:
        return JsonResponse(
            {"error": "Preferences not found for the user."},
            status=status.HTTP_404_NOT_FOUND,
        )


# TODO: DELETE
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def set_user_bg_color(request):
    try:
        preferences = Preference.objects.get(user=request.user)
    except Preference.DoesNotExist:
        preferences = Preference(user=request.user)

    serializer = PreferencesSerializer(preferences, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    else:
        LOGGER.error(f"Serializer errors in set_user_bg_color: {serializer.errors}")
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
