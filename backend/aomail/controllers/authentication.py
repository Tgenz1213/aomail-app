"""
Handles authentication processes and email account linking.

Endpoints:
- ✅ signup: Register user and handle OAuth2.0 callback.
- ✅ login: Authenticate user and return access token.
- ✅ check_username: Verify if the username is available.
- ✅ is_authenticated: Check if the user has a valid access token.
- ✅ link_email: Link email with the authenticated user's account.
- ✅ unlink_email: Unlink email and delete associated data.
- ✅ delete_account: Remove the authenticated user account.
- ✅ refresh_token: Refresh JWT access token and return a new one.
- ✅ generate_reset_token: Send password reset email
- ✅ reset_password: Handle password reset requests
"""

import datetime
import json
import logging
import threading
import jwt
from urllib.parse import urlencode
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from aomail.utils import security
from aomail.utils.security import subscription
from aomail.constants import (
    BASE_URL,
    EMAIL_ADMIN,
    FREE_PLAN,
    BASE_URL_MA,
    DEFAULT_CATEGORY,
    EMAIL_NO_REPLY,
    ENCRYPTION_KEYS,
    GOOGLE,
    GOOGLE,
    MAX_RETRIES,
    MICROSOFT,
    MICROSOFT,
)
from aomail.email_providers.google import profile as profile_google
from aomail.email_providers.microsoft import profile as profile_microsoft
from aomail.email_providers.google import authentication as auth_google
from aomail.email_providers.microsoft import authentication as auth_microsoft
from aomail.email_providers.google import webhook as webhook_google
from aomail.email_providers.microsoft import webhook as webhook_microsoft
from aomail.models import (
    Category,
    GoogleListener,
    MicrosoftListener,
    SocialAPI,
    Preference,
    Statistics,
    Subscription,
)


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


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
            theme (str): User's preferred theme.
            color (str): User's preferred color.
            categories (list): List of categories associated with the user.
            userDescription (str): Description or bio of the user.

    Returns:
        Response: JSON response with user ID, access token, and email on success,
                      or error message on failure.
    """
    ip = security.get_ip_with_port(request)
    LOGGER.info(f"Signup request received from IP: {ip}")

    parameters: dict = json.loads(request.body)
    type_api: str = parameters.get("typeApi", "")
    code: str = parameters.get("code", "")
    username: str = parameters.get("login", "")
    password: str = parameters.get("password", "")
    timezone: str = parameters.get("timezone", "")
    language: str = parameters.get("language", "")
    theme: str = parameters.get("theme", "")
    categories: list = parameters.get("categories", [])
    user_description: str = parameters.get("userDescription", "")

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
        if SocialAPI.objects.filter(email=email).exists():
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
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    result = save_user_data(
        user,
        type_api,
        user_description,
        email,
        access_token,
        refresh_token,
        theme,
        categories,
        language,
        timezone,
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
                    target=profile_microsoft.set_all_contacts, args=(access_token, user)
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
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        return Response(
            {"accessToken": django_access_token},
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
    if type_api == GOOGLE:
        subscribed = webhook_google.subscribe_to_email_notifications(user, email)
        if subscribed:
            social_api = auth_google.get_social_api(user, email)
            GoogleListener.objects.create(
                last_modified=timezone.now(), social_api=social_api
            )
            return True

    elif type_api == MICROSOFT:
        subscribed_email = webhook_microsoft.subscribe_to_email_notifications(
            user, email
        )
        subscribed_contact = webhook_microsoft.subscribe_to_contact_notifications(
            user, email
        )
        if subscribed_email and subscribed_contact:
            return True

    return False


def unsubscribe_listeners(user: User, email: str = None):
    """
    Unsubscribes the authenticated user from social and Microsoft listeners.

    Args:
        user (User): The authenticated user object.
        email (str, optional): Specific email to unsubscribe from Microsoft listeners.
    """
    social_apis = SocialAPI.objects.filter(user=user)

    # Unsubscribe from Google APIs
    if social_apis.exists():
        for social_api in social_apis:
            if social_api.type_api == GOOGLE:
                for i in range(MAX_RETRIES):
                    if webhook_google.unsubscribe_from_email_notifications(
                        user, social_api.email
                    ):
                        break
                    else:
                        LOGGER.critical(
                            f"[Attempt {i+1}] Failed to unsubscribe from Google: {social_api.email}"
                        )
                        context = {
                            "title": "Critical Alert: Google Unsubscription Failure",
                            "attempt_number": i + 1,
                            "subscription_id": social_api.email,
                            "email_provider": GOOGLE,
                            "user": user,
                        }
                        email_html = render_to_string(
                            "unsubscribe_failure.html", context
                        )
                        send_mail(
                            subject="Critical Alert: Google Unsubscription Failure",
                            message="",
                            recipient_list=[EMAIL_ADMIN],
                            from_email=EMAIL_NO_REPLY,
                            html_message=email_html,
                            fail_silently=False,
                        )

    # Unsubscribe from Microsoft listeners
    if email:
        microsoft_listeners = MicrosoftListener.objects.filter(user=user, email=email)
    else:
        microsoft_listeners = MicrosoftListener.objects.filter(user=user)

    if microsoft_listeners.exists():
        for listener in microsoft_listeners:
            for i in range(MAX_RETRIES):
                if webhook_microsoft.delete_subscription(
                    user, listener.email, listener.subscription_id
                ):
                    break
                else:
                    LOGGER.critical(
                        f"[Attempt {i+1}] Failed to unsubscribe from Microsoft: {listener.subscription_id}"
                    )
                    context = {
                        "title": "Critical Alert: Microsoft Unsubscription Failure",
                        "attempt_number": i + 1,
                        "subscription_id": listener.subscription_id,
                        "email_provider": MICROSOFT,
                        "user": user,
                    }
                    email_html = render_to_string("unsubscribe_failure.html", context)
                    send_mail(
                        subject="Critical Alert: Microsoft Unsubscription Failure",
                        message="",
                        recipient_list=[EMAIL_ADMIN],
                        from_email=EMAIL_NO_REPLY,
                        html_message=email_html,
                        fail_silently=False,
                    )


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
        if type_api == GOOGLE:
            access_token, refresh_token = auth_google.link_email_tokens(code)
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
            access_token, refresh_token = auth_microsoft.link_email_tokens(code)
            if not access_token:
                return {"error": "Failed to obtain access token from Microsoft API"}

            result_get_email = profile_microsoft.get_email(access_token)
            if "error" in result_get_email:
                return {"error": result_get_email["error"]}
            else:
                email = result_get_email["email"]

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
        return {"error": str(e)}


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
            theme=theme, language=language, timezone=timezone, user=user
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

        Statistics.objects.create(user=user)

        return {"message": "User data saved successfully"}

    except Exception as e:
        return {"error": str(e)}


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request: HttpRequest) -> Response:
    """
    Authenticates a user using the provided username and password and returns an access token.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameters in the body:
            username (str): User's username for authentication.
            password (str): User's password for authentication.

    Returns:
        Response: JSON response with an access token on successful authentication,
                      or an error message on failure.
    """
    parameters: dict = json.loads(request.body)
    username = parameters.get("username")
    password = parameters.get("password")

    if not username:
        return Response(
            {"error": "Username is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not password:
        return Response(
            {"error": "Password is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(username=username, password=password)

    if user:
        refresh: RefreshToken = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({"accessToken": access_token}, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "Invalid username or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_token(request: HttpRequest) -> Response:
    """
    Refreshes the JWT access token for a user and returns a new access token.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameter in the body:
            access_token (str): JWT access token to be refreshed.

    Returns:
        Response: JSON response with a new access token on success,
                      or an error message on failure.
    """
    parameters: dict = json.loads(request.body)
    access_token: str = parameters.get("accessToken")

    if not access_token:
        return Response(
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

        return Response({"accessToken": new_access_token}, status=status.HTTP_200_OK)
    except Exception as e:
        LOGGER.error(
            f"Unexpected error occured when refreshing Django access token: {str(e)}"
        )
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@subscription([FREE_PLAN])
def delete_account(request: HttpRequest) -> Response:
    """
    Removes the authenticated user account from the database.

    Args:
        request (HttpRequest): HTTP request object containing the authenticated user.

    Returns:
        Response: {"message": "User successfully deleted"} if the user account is deleted successfully,
                      or {"error": "Details of the specific error."} if there's an issue with the deletion.
    """
    user = request.user

    try:
        ip = security.get_ip_with_port(request)
        LOGGER.info(f"Deletion request received from IP: {ip} for user ID: {user.id}")

        unsubscribe_listeners(user)
        user.delete()

        LOGGER.info(f"User with ID: {user.id} deleted successfully")
        return Response(
            {"message": "User successfully deleted"}, status=status.HTTP_200_OK
        )
    except Exception as e:
        LOGGER.error(f"Error when deleting account {user.id}: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@subscription([FREE_PLAN])
def unlink_email(request: HttpRequest) -> Response:
    """
    Unlinks the specified email and deletes all stored emails associated with the user's account.

    Args:
        request (HttpRequest): HTTP request object containing the email to unlink in the request body.
            Expects JSON body with:
                email (str): The email address to unlink from the user's account.

    Returns:
        Response: {"message": "Email unlinked successfully!"} if the unlinking is successful,
                      or {"error": "Details of the specific error."} if there's an issue with the unlinking.
    """
    parameters: dict = json.loads(request.body)
    user = request.user
    email = parameters.get("email")

    try:
        social_api = SocialAPI.objects.get(user=user, email=email)
        unsubscribe_listeners(user, email)
        social_api.delete()
        return Response(
            {"message": "Email unlinked successfully!"}, status=status.HTTP_202_ACCEPTED
        )
    except SocialAPI.DoesNotExist:
        return Response(
            {"error": "SocialAPI entry not found"}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@subscription([FREE_PLAN])
def link_email(request: HttpRequest) -> Response:
    """
    Links the specified email with the authenticated user's account.

    Args:
        request (HttpRequest): HTTP request object containing the email details to link in the request body.
            Expects JSON body with:
                type_api (str): The type of API.
                code (str): The authorization code for linking the email.
                user_description (str): A description provided by the user.

    Returns:
        Response: {"message": "Email linked to account successfully!"} if the linking is successful,
                      or {"error": "Details of the specific error."} if there's an issue with the linking process.
    """
    parameters: dict = json.loads(request.body)
    user = request.user
    type_api = parameters.get("typeApi")
    code = parameters.get("code")
    user_description = parameters.get("userDescription")

    ip = security.get_ip_with_port(request)
    LOGGER.info(f"Link email request received from IP: {ip} and user ID: {user.id}")

    authorization_result = validate_code_link_email(type_api, code)
    if "error" in authorization_result:
        LOGGER.error(f"Authorization failed: {authorization_result['error']}")
        return Response(
            {"error": authorization_result["error"]}, status=status.HTTP_400_BAD_REQUEST
        )

    access_token = authorization_result["access_token"]
    refresh_token = authorization_result["refresh_token"]
    email = authorization_result["email"]
    refresh_token_encrypted = security.encrypt_text(
        ENCRYPTION_KEYS["SocialAPI"]["refresh_token"], refresh_token
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
        LOGGER.info(f"Social API for user ID: {user.id} created successfully")
    except IntegrityError:
        return Response(
            {"error": "Email address already used by another account"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        if type_api == GOOGLE:
            threading.Thread(
                target=profile_google.set_all_contacts, args=(user, email)
            ).start()
        elif type_api == MICROSOFT:
            threading.Thread(
                target=profile_microsoft.set_all_contacts, args=(access_token, user)
            ).start()
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    subscribed = subscribe_listeners(type_api, user, email)
    if subscribed:
        LOGGER.info(f"Email account linked successfully for user ID: {user.id}")
        return Response(
            {"message": "Email linked to account successfully!"},
            status=status.HTTP_201_CREATED,
        )
    else:
        LOGGER.error(
            f"Failed to subscribe to listener for Social API: {social_api.email}. Error: {str(e)}"
        )
        social_api.delete()
        LOGGER.info(f"Social API: {social_api.email} deleted successfully")
        return Response(
            {"error": "Could not subscribe to listener"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@subscription([FREE_PLAN])
def is_authenticated(request: HttpRequest) -> Response:
    """
    Check if the user is authenticated.

    Args:
        request (HttpRequest): HTTP request object.

    Returns:
        Response: {"isAuthenticated": True} indicating the user is authenticated.
    """
    return Response({"isAuthenticated": True}, status=status.HTTP_200_OK)


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
def generate_reset_token(request: HttpRequest) -> Response:
    """
    Generate a password reset token and send an email with the reset link.

    Args:
        request (HttpRequest): HTTP request object containing the email in the request body.

    Returns:
        Response: A JSON response indicating the result of the operation.
    """
    try:
        parameters: dict = json.loads(request.body)
        email = parameters.get("email")
        LOGGER.info(f"Attempting to generate reset password token for email: {email}")

        social_api = SocialAPI.objects.get(email=email)
        token = PasswordResetTokenGenerator().make_token(social_api.user)
        uidb64 = urlsafe_base64_encode(str(social_api.user.pk).encode())
        reset_link = f"{BASE_URL_MA}reset_password/{uidb64}/{token}/"

        context = {"reset_link": reset_link, "email": EMAIL_ADMIN}
        email_html = render_to_string("password_reset_email.html", context)

        send_mail(
            subject="Password Reset for Aomail",
            message="",
            recipient_list=[email],
            from_email=EMAIL_NO_REPLY,
            html_message=email_html,
            fail_silently=False,
        )
        LOGGER.info(f"Password reset email sent successfully to {email}")
        return Response(
            {"message": "Email sent successfully!"}, status=status.HTTP_200_OK
        )
    except SocialAPI.DoesNotExist:
        return Response(
            {"error": "Email address is not linked with an account"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        LOGGER.error(f"Error generating reset token: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def reset_password(
    request: HttpRequest, uidb64: str, token: str
) -> Response | HttpResponseRedirect:
    """
    Handle password reset requests.

    Args:
        request (HttpRequest): HTTP request object.
        uidb64 (str): Base64 encoded user ID.
        token (str): Password reset token.

    Returns:
        Response: For GET requests.
        HttpResponseRedirect: For POST requests.
    """
    LOGGER.info(f"Password reset request received. Method: {request.method}")

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        LOGGER.error(f"Error decoding user ID or finding user: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if not PasswordResetTokenGenerator().check_token(user, token):
        return Response(
            {"error": "Invalid or expired password reset link"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if request.method == "GET":
        base_url = f"{BASE_URL}reset-password-form"
        params = urlencode({"uidb64": uidb64, "token": token})
        redirect_url = f"{base_url}?{params}"
        return HttpResponseRedirect(redirect_url)

    if request.method == "POST":
        parameters: dict = json.loads(request.body)
        password = parameters["password"]

        if not (8 <= len(password) <= 32):
            return Response(
                {"error": "Password length must be between 8 and 32 characters"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(password)
        user.save()
        LOGGER.info(f"Password reset successfully for user: {user.username}")
        return Response(
            {"message": "Password reset successfully"}, status=status.HTTP_200_OK
        )
