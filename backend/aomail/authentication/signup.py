"""
Authentication and Signup Module

Endpoints:
- ✅ signup: Register a new user and handle OAuth2.0 callback.
- ✅ check_username: Verify if a username is available.
- ✅ process_demo_data: Process the 10 most recent emails for a newly signed-up user.
"""

import json
import logging
import threading
import jwt
from concurrent.futures import ThreadPoolExecutor
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.utils import timezone
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from aomail.utils import security
from aomail.constants import (
    GOOGLE,
    GOOGLE,
    MICROSOFT,
    MICROSOFT,
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    PREMIUM_PLAN,
    SOCIAL_API_REFRESH_TOKEN_KEY,
)
from aomail.email_providers.google import profile as profile_google
from aomail.email_providers.microsoft import profile as profile_microsoft
from aomail.email_providers.google import authentication as auth_google
from aomail.email_providers.microsoft import authentication as auth_microsoft
from aomail.models import (
    SocialAPI,
    Preference,
    Statistics,
    Subscription,
    Agent,
)
from aomail.email_providers.microsoft import (
    email_operations as email_operations_microsoft,
)
from aomail.email_providers.google import (
    email_operations as email_operations_google,
)
from aomail.email_providers.imap import (
    email_operations as email_operations_imap,
)
from aomail.email_providers.utils import email_to_db
from aomail.authentication.authentication import subscribe_listeners


LOGGER = logging.getLogger(__name__)


@api_view(["GET"])
@permission_classes([AllowAny])
def check_username(request: HttpRequest) -> Response:
    """
    Verify if the username is available.

    Args:
        request (HttpRequest): HTTP request object containing the username in the headers.

    Returns:
        Response: {"available": False} if the username is taken,
                      {"available": True} if the username is available.
    """
    username = request.headers.get("username")

    if User.objects.filter(username=username).exists():
        return Response({"available": False}, status=status.HTTP_200_OK)
    else:
        return Response({"available": True}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request: HttpRequest) -> Response:
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

    Returns:
        Response: JSON response with user ID, access token, and email on success,
                      or error message on failure.
    """
    ip = security.get_ip_with_port(request)
    LOGGER.info(f"Signup request received from IP: {ip}")

    if User.objects.all().count() >= 250:
        return Response(
            {"error": "Limit of 250 users reached"}, status=status.HTTP_409_CONFLICT
        )

    parameters: dict = json.loads(request.body)
    type_api: str = parameters.get("typeApi", "")
    code: str = parameters.get("code", "")
    username: str = parameters.get("login", "")
    password: str = parameters.get("password", "")
    user_timezone: str = parameters.get("timezone", "")
    language: str = parameters.get("language", "")

    validation_result: dict = validate_signup_data(username, password, code)
    if "error" in validation_result:
        LOGGER.error(f"Validation failed for signup data: {validation_result['error']}")
        return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

    LOGGER.info("User signup data validated successfully")

    authorization_result: dict = validate_authorization_code(type_api, code)
    if "error" in authorization_result:
        LOGGER.error(f"Authorization failed: {authorization_result['error']}")
        return Response(
            {"error": authorization_result["error"]}, status=status.HTTP_400_BAD_REQUEST
        )

    LOGGER.info(f"Successfully validated authorization code for {type_api} API")

    access_token = authorization_result.get("access_token", "")
    refresh_token = authorization_result.get("refresh_token", "")
    email = authorization_result.get("email", "")

    if email:
        social_api = SocialAPI.objects.filter(email=email)
        if social_api.exists() and social_api.first().user:
            LOGGER.error("Email address already used by another account")
            return Response(
                {"error": "Email address already used by another account"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif " " in email:
            LOGGER.error("Email address must not contain spaces")
            return Response(
                {"error": "Email address must not contain spaces"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        LOGGER.error("No email received")
        return Response(
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
        return Response(
            {"error": "Internal server error"}, status=status.HTTP_400_BAD_REQUEST
        )

    result = save_user_data(
        user,
        type_api,
        email,
        access_token,
        refresh_token,
        language,
        user_timezone,
    )
    if "error" in result:
        LOGGER.error(f"Failed to save user data: {result['error']}")
        user.delete()
        LOGGER.info(f"User {username} deleted successfully")
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    LOGGER.info(f"User data saved successfully for {username}")

    try:
        if type_api == GOOGLE:
            threading.Thread(
                target=profile_google.set_all_contacts, args=(user, email)
            ).start()
        elif type_api == MICROSOFT:
            if profile_microsoft.verify_license(access_token):
                threading.Thread(
                    target=profile_microsoft.set_all_contacts, args=(user, email)
                ).start()
            else:
                LOGGER.error("No license associated with the account")
                user.delete()
                LOGGER.info(f"User {username} deleted successfully")
                return Response(
                    {"error": "No license associated with the account"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
    except Exception as e:
        LOGGER.error(f"Failed to set contacts: {str(e)}")
        user.delete()
        LOGGER.info(f"User {username} deleted successfully")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    Subscription.objects.create(
        user=user,
        plan=PREMIUM_PLAN,
    )
    LOGGER.info(f"User {username} subscribed to premium plan (free trial)")

    subscribed = subscribe_listeners(type_api, user, email)
    if subscribed:
        signup_token = jwt.encode(
            {
                "user_id": user.id,
                "type": "signup",
                "exp": timezone.now() + timezone.timedelta(minutes=30),
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        LOGGER.info(f"User {username} subscribed to listeners successfully")

        result = create_default_agents(user, language)

        if "error" in result:
            LOGGER.error(f"Default agent creation failed: {result['error']}")
            return Response(
                {"error": result["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                "accessToken": django_access_token,
                "signupToken": signup_token,
                "emailSocial": email,
            },
            status=status.HTTP_201_CREATED,
        )
    else:
        LOGGER.error(f"Failed to subscribe user {username} to listeners")
        user.delete()
        LOGGER.info(f"User {username} deleted successfully")
        return Response(
            {"error": "Could not subscribe to listener"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def create_default_agents(user: User, language: str) -> dict:
    """
    Creates default agents for the user based on the preferred language (English or French).

    Args:
        user (User): The user for whom agents will be created.
        language (str): The preferred language ('en' or 'fr').

    Returns:
        dict: A dictionary indicating the success or failure of the operation.
              - On success: {'message': 'Default agents created successfully'}
              - On failure: {'error': <error_message>}
    """
    try:
        default_agents_en = [
            {
                "agent_name": "Bob : to talk to friends",
                "agent_ai_model": "gpt-3.5-turbo",
                "ai_template": "Quick and informal as if talking to a friend.",
                "email_example": "",
                "length": "short",
                "formality": "informal",
                "language": language,
                "picture": "/app/media/agent_icon/default_aomail_agent_bob.png",
                "icon_name": "default_aomail_agent_bob.png",
            },
            {
                "agent_name": "AO : to talk to colleagues",
                "agent_ai_model": "gpt-3.5-turbo",
                "ai_template": "Fast and formal as if talking to colleagues.",
                "email_example": "",
                "length": "short",
                "formality": "formal",
                "language": language,
                "picture": "/app/media/agent_icon/aomail_agent_ao.png",
                "icon_name": "aomail_agent_ao.png",
            },
            {
                "agent_name": "Jhon : to talk to supervisors",
                "agent_ai_model": "gpt-3.5-turbo",
                "ai_template": "Medium-paced and highly formal as if talking to supervisors.",
                "email_example": "",
                "length": "medium",
                "formality": "very formal",
                "language": language,
                "picture": "/app/media/agent_icon/default_aomail_agent_jhon.png",
                "icon_name": "default_aomail_agent_jhon.png",
            },
        ]

        default_agents_fr = [
            {
                "agent_name": "Bob",
                "agent_ai_model": "gpt-3.5-turbo",
                "ai_template": "Rapide et informel comme si vous parliez à un ami.",
                "email_example": "",
                "length": "court",
                "formality": "informel",
                "language": language,
                "picture": "/app/media/agent_icon/default_aomail_agent_bob.png",
                "icon_name": "default_aomail_agent_bob.png",
            },
            {
                "agent_name": "AO",
                "agent_ai_model": "gpt-3.5-turbo",
                "ai_template": "Rapide et formel comme si vous parliez à des collègues.",
                "email_example": "",
                "length": "court",
                "formality": "formel",
                "language": language,
                "picture": "/app/media/agent_icon/aomail_agent_ao.png",
                "icon_name": "aomail_agent_ao.png",
            },
            {
                "agent_name": "Jhon",
                "agent_ai_model": "gpt-3.5-turbo",
                "ai_template": "Modéré et très formel comme si vous parliez à des décideurs.",
                "email_example": "",
                "length": "moyen",
                "formality": "formel",
                "language": language,
                "picture": "/app/media/agent_icon/default_aomail_agent_jhon.png",
                "icon_name": "default_aomail_agent_jhon.png",
            },
        ]

        if language.lower() == "fr" or language.lower() == "french":
            agents_to_create = default_agents_fr
            LOGGER.info(f"Creating default French agents for user {user.username}")
        else:
            agents_to_create = default_agents_en
            LOGGER.info(f"Creating default English agents for user {user.username}")

        for agent_data in agents_to_create:
            Agent.objects.create(
                agent_name=agent_data["agent_name"],
                agent_ai_model=agent_data["agent_ai_model"],
                ai_template=agent_data["ai_template"],
                email_example=agent_data["email_example"],
                user=user,
                length=agent_data["length"],
                formality=agent_data["formality"],
                language=agent_data["language"],
                last_used=False,
                picture=agent_data["picture"],
                icon_name=agent_data["icon_name"],
            )
        LOGGER.info(f"Default agents created for user {user.username}")
        return {"message": "Default agents created successfully"}
    except Exception as e:
        LOGGER.error(
            f"Failed to create default agents for user {user.username}: {str(e)}"
        )
        return {"error": "An error occurred during agent creation."}


@api_view(["POST"])
@permission_classes([AllowAny])
def process_demo_data(request: HttpRequest) -> Response:
    """
    Process the 10 most recent emails for a newly signed up user.
    This endpoint should only be accessible during the signup process.

    Args:
        request (HttpRequest): HTTP request containing:
            email (str): User's email address
            signup_token (str): Temporary token from signup process

    Returns:
        Response: Success or error message
    """
    try:
        parameters: dict = json.loads(request.body)
        email = parameters.get("emailSocial")
        type_api = parameters.get("typeApi")
        signup_token = parameters.get("signupToken")

        if not email or not signup_token:
            return Response(
                {"error": "Missing required parameters"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            decoded_token = jwt.decode(
                signup_token, settings.SECRET_KEY, algorithms=["HS256"]
            )

            if (
                decoded_token.get("type") != "signup"
                or decoded_token.get("exp") < timezone.now().timestamp()
            ):
                return Response(
                    {"error": "Invalid or expired signup token"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            user_id = decoded_token.get("user_id")
            user = User.objects.get(id=user_id)

        except (jwt.InvalidTokenError, User.DoesNotExist):
            return Response(
                {"error": "Invalid signup token"}, status=status.HTTP_401_UNAUTHORIZED
            )

        threading.Thread(
            target=process_demo_emails, args=(type_api, user, email)
        ).start()

        return Response(
            {"message": "Demo email processing started"},
            status=status.HTTP_202_ACCEPTED,
        )

    except Exception as e:
        LOGGER.error(f"Error processing demo emails: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def process_demo_emails(type_api: str, user: User, email: str):
    """
    Processes up to the newest 10 emails from the main inbox of the user.

    Args:
        type_api (str): The type of email service being used (e.g., "GOOGLE" or "MICROSOFT").
        user (User): User object representing the email account owner.
        email (str): Email address of the user for authentication and data retrieval.
    """
    LOGGER.info(
        f"User with ID {user.id} is initiating the demo email processing sequence for {type_api}."
    )

    social_api = SocialAPI.objects.get(user=user, email=email)

    if social_api.type_api == GOOGLE and not social_api.imap_config:
        email_ids = email_operations_google.get_demo_list(user, email)
    elif social_api.type_api == MICROSOFT and not social_api.imap_config:
        email_ids = email_operations_microsoft.get_demo_list(user, email)
    elif social_api.imap_config:
        email_ids = email_operations_imap.get_demo_list(user, email)
    else:
        LOGGER.error(f"Unsupported email provider type: {type_api}")
        return
    LOGGER.info(
        f"Retrieved {len(email_ids)} email IDs for user ID {user.id}. Processing each email now."
    )

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_email_id = {
            executor.submit(email_to_db, social_api, email_id): email_id
            for email_id in email_ids
        }

        for future in future_to_email_id:
            try:
                future.result()
            except Exception as e:
                LOGGER.error(
                    f"Error processing email ID {future_to_email_id[future]}: {e}"
                )

    LOGGER.info(f"Completed processing demo emails for user ID {user.id}.")


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
        if type_api == GOOGLE:
            access_token, refresh_token = auth_google.exchange_code_for_tokens(code)
            if not access_token or not refresh_token:
                return {
                    "error": "Failed to obtain access or refresh token from Google API"
                }

            result_get_email = profile_google.get_email(access_token, refresh_token)
            if "error" in result_get_email:
                return {"error": result_get_email["error"]}
            else:
                email = result_get_email["email"]

        elif type_api == MICROSOFT:
            access_token, refresh_token = auth_microsoft.exchange_code_for_tokens(code)
            if not access_token or not refresh_token:
                return {
                    "error": "Failed to obtain access or refresh token from Microsoft API"
                }

            result_get_email = profile_microsoft.get_email(access_token)
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
        LOGGER.error(f"An unexpected error occurred during validation: {str(e)}")
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
    elif not (PASSWORD_MIN_LENGTH <= len(password) <= PASSWORD_MAX_LENGTH):
        return {"error": "Password length must be between 8 and 128 characters"}

    return {"message": "User signup data validated successfully"}


def save_user_data(
    user: User,
    type_api: str,
    email: str,
    access_token: str,
    refresh_token: str,
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
            SOCIAL_API_REFRESH_TOKEN_KEY, refresh_token
        )
        SocialAPI.objects.create(
            user=user,
            type_api=type_api,
            email=email,
            access_token=access_token,
            refresh_token=refresh_token_encrypted,
        )
        Preference.objects.create(language=language, timezone=timezone, user=user)

        Statistics.objects.create(user=user)

        return {"message": "User data saved successfully"}

    except Exception as e:
        LOGGER.error(f"Unexpected error occured while saving user data: {str(e)}")
        return {"error": "Internal server error"}
