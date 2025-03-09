"""
Handles authentication processes and email account linking.

Endpoints:
- ✅ login: Authenticate user and return access token.
- ✅ is_authenticated: Check if the user has a valid access token.
- ✅ link_email: Link email with the authenticated user's account.
- ✅ unlink_email: Unlink email and delete associated data.
- ✅ delete_account: Remove the authenticated user account.
- ✅ refresh_token: Refresh JWT access token and return a new one.
- ✅ generate_reset_token: Send password reset email
- ✅ reset_password: Handle password reset requests
- ✅ is_admin: Check if the user is a superuser.
"""

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
from aomail.utils.security import subscription, admin_access_required
from aomail.constants import (
    ALLOW_ALL,
    BASE_URL,
    EMAIL_ADMIN,
    BASE_URL_API,
    EMAIL_NO_REPLY,
    ENTREPRISE_PLAN,
    GOOGLE,
    GOOGLE,
    MAX_RETRIES,
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
from aomail.email_providers.google import webhook as webhook_google
from aomail.email_providers.microsoft import webhook as webhook_microsoft
from aomail.models import (
    EmailServerConfig,
    GoogleListener,
    MicrosoftListener,
    SocialAPI,
    Subscription,
)
from aomail.payment_providers import stripe
from aomail.email_providers.imap.authentication import validate_imap_connection
from aomail.email_providers.smtp.authentication import validate_smtp_connection
from aomail.email_providers.imap import profile as imap_profile


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


def subscribe_listeners(type_api: str, user: User, email: str) -> bool:
    """
    Subscribes the user to listeners based on the type of API provided.

    Args:
        type_api (str): The type of API.
        user (User): User identifier.
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
    if email:
        social_apis = SocialAPI.objects.filter(user=user, email=email)
    else:
        social_apis = SocialAPI.objects.filter(user=user)

    # Unsubscribe from Google APIs
    if social_apis.exists():
        for social_api in social_apis:
            if not social_api.imap_config and social_api.type_api == GOOGLE:
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
            social_api = SocialAPI.objects.get(user=user, email=listener.email)
            for i in range(MAX_RETRIES):
                if (
                    not social_api.imap_config
                    and webhook_microsoft.delete_subscription(
                        user, listener.email, listener.subscription_id
                    )
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
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["DELETE"])
@subscription(ALLOW_ALL)
def delete_account(request: HttpRequest) -> Response:
    """
    Removes the authenticated user's account from the database.

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

        subscription = Subscription.objects.get(user=user)
        if not subscription.is_trial and subscription.is_active:
            cancelled_subscription = stripe.cancel_subscription(subscription)

            if not cancelled_subscription:
                return Response(
                    {
                        "error": "Failed to cancel Stripe subscription. Please try using the management link."
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        user_id = user.id
        user.delete()
        LOGGER.info(f"User with ID: {user_id} deleted successfully")

        return Response(
            {"message": "User successfully deleted"}, status=status.HTTP_200_OK
        )
    except Exception as e:
        LOGGER.error(f"Error when deleting account for user {user_id}: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@subscription(ALLOW_ALL)
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

    ip = security.get_ip_with_port(request)
    LOGGER.info(f"Unlink email request received from IP: {ip} and user ID: {user.id}.")

    if not email:
        LOGGER.warning(
            f"Unlinking failed: No email provided from IP: {ip} for user ID: {user.id}."
        )
        return Response(
            {"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        LOGGER.info(
            f"Attempting to unlink email '{email}' for user ID: {user.id} from IP: {ip}."
        )

        social_api = SocialAPI.objects.get(user=user, email=email)

        unsubscribe_listeners(user, email)
        social_api.delete()

        LOGGER.info(
            f"Email '{email}' successfully unlinked for user ID: {user.id} from IP: {ip}."
        )
        return Response(
            {"message": "Email unlinked successfully!"}, status=status.HTTP_202_ACCEPTED
        )
    except SocialAPI.DoesNotExist:
        LOGGER.error(
            f"Unlinking failed: SocialAPI entry not found for email '{email}' and user ID: {user.id} from IP: {ip}."
        )
        return Response(
            {"error": "SocialAPI entry not found"}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        LOGGER.error(
            f"Unlinking failed: An unexpected error occurred for user ID: {user.id} while unlinking email '{email}' from IP: {ip}: {str(e)}"
        )
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@subscription([PREMIUM_PLAN, ENTREPRISE_PLAN])
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

    # Oauth connection attempt
    if code:
        result = link_oauth_account(type_api, code, user, user_description)

    # IMAP/SMTP connection attempt
    else:
        result = link_email_config_account(
            user,
            type_api,
            user_description,
            parameters.get("emailAddress"),
            parameters.get("imapAppPassword"),
            parameters.get("imapHost"),
            parameters.get("imapPort"),
            parameters.get("imapEncryption"),
            parameters.get("smtpAppPassword"),
            parameters.get("smtpHost"),
            parameters.get("smtpPort"),
            parameters.get("smtpEncryption"),
        )

    if result["success"]:
        return Response({"message": result["message"]}, status=result["status_code"])
    else:
        return Response({"error": result["error"]}, status=result["status_code"])


def link_email_config_account(
    user: User,
    type_api: str,
    user_description: str,
    email_address: str,
    imap_app_password: str,
    imap_host: str,
    imap_port: int,
    imap_encryption: str,
    smtp_app_password: str,
    smtp_host: str,
    smtp_port: int,
    smtp_encryption: str,
) -> dict:
    imap_valid = validate_imap_connection(
        email_address, imap_app_password, imap_host, imap_port, imap_encryption
    )
    if not imap_valid:
        return {
            "success": False,
            "error": "Failed to validate IMAP connection",
            "status_code": status.HTTP_400_BAD_REQUEST,
        }

    smtp_valid = validate_smtp_connection(
        email_address, smtp_app_password, smtp_host, smtp_port, smtp_encryption
    )
    if not smtp_valid:
        return {
            "success": False,
            "error": "Failed to validate SMTP connection",
            "status_code": status.HTTP_400_BAD_REQUEST,
        }

    imap_app_password_encrypted = security.encrypt_text(
        SOCIAL_API_REFRESH_TOKEN_KEY, imap_app_password
    )
    smtp_app_password_encrypted = security.encrypt_text(
        SOCIAL_API_REFRESH_TOKEN_KEY, smtp_app_password
    )
    try:
        social_api = SocialAPI.objects.get(user=user, email=email_address)

        social_api.imap_config.host = imap_host
        social_api.imap_config.port = imap_port
        social_api.imap_config.app_password = imap_app_password_encrypted
        social_api.imap_config.encryption = imap_encryption

        social_api.smtp_config.host = smtp_host
        social_api.smtp_config.port = smtp_port
        social_api.smtp_config.app_password = smtp_app_password_encrypted
        social_api.smtp_config.encryption = smtp_encryption

        social_api.save()
        LOGGER.info(f"Social API for user ID: {user.id} tokens updated successfully")
    except SocialAPI.DoesNotExist:
        imap_config = EmailServerConfig.objects.create(
            host=imap_host,
            port=imap_port,
            app_password=imap_app_password_encrypted,
            encryption=imap_encryption,
        )
        smtp_config = EmailServerConfig.objects.create(
            host=smtp_host,
            port=smtp_port,
            app_password=smtp_app_password_encrypted,
            encryption=smtp_encryption,
        )
        social_api = SocialAPI.objects.create(
            user=user,
            email=email_address,
            type_api=type_api,
            user_description=user_description,
            access_token="",
            refresh_token="",
            imap_config=imap_config,
            smtp_config=smtp_config,
        )

    threading.Thread(
        target=imap_profile.set_all_contacts, args=(user, social_api)
    ).start()

    return {
        "success": True,
        "message": "Email linked to account successfully!",
        "status_code": status.HTTP_201_CREATED,
    }


def link_oauth_account(
    type_api: str, code: str, user: User, user_description: str
) -> dict:
    authorization_result = validate_code_link_email(type_api, code)
    if "error" in authorization_result:
        LOGGER.error(f"Authorization failed: {authorization_result['error']}")
        return {
            "success": False,
            "error": authorization_result["error"],
            "status_code": status.HTTP_400_BAD_REQUEST,
        }

    access_token = authorization_result["access_token"]
    refresh_token = authorization_result["refresh_token"]
    email = authorization_result["email"]
    refresh_token_encrypted = security.encrypt_text(
        SOCIAL_API_REFRESH_TOKEN_KEY, refresh_token
    )

    regrant = False
    try:
        regrant = True
        social_api = SocialAPI.objects.get(user=user, email=email)
        social_api.refresh_token = refresh_token_encrypted
        social_api.access_token = access_token
        social_api.save()
        LOGGER.info(f"Social API for user ID: {user.id} tokens updated successfully")
    except SocialAPI.DoesNotExist:
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
        return {
            "success": False,
            "error": "Email address already used by another account",
            "status_code": status.HTTP_400_BAD_REQUEST,
        }

    try:
        if type_api == GOOGLE:
            threading.Thread(
                target=profile_google.set_all_contacts, args=(user, email)
            ).start()
        elif type_api == MICROSOFT:
            threading.Thread(
                target=profile_microsoft.set_all_contacts, args=(user, email)
            ).start()
    except Exception as e:
        LOGGER.error(
            f"Failed to save all contacts for Social API email: {social_api.email}. Error: {str(e)}"
        )
        return {
            "success": False,
            "error": "Internal server error",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        }

    subscribed = subscribe_listeners(type_api, user, email)
    if subscribed:
        LOGGER.info(f"Email account linked successfully for user ID: {user.id}")
        return {
            "success": True,
            "message": "Email linked to account successfully!",
            "status_code": status.HTTP_201_CREATED,
        }
    else:
        LOGGER.error(
            f"Failed to subscribe to listener for Social API: {social_api.email}"
        )
        if not regrant:
            social_api.delete()
            LOGGER.info(f"Social API: {social_api.email} deleted successfully")

        return {
            "success": False,
            "error": "Could not subscribe to listenerr",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        }


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
        return {"error": "Internal server error"}


@api_view(["GET"])
@subscription(ALLOW_ALL)
def is_authenticated(request: HttpRequest) -> Response:
    """
    Check if the user is authenticated and return their subscription status.

    Args:
        request (HttpRequest): HTTP request object.

    Returns:
        Response:
            - {"isAuthenticated": True, "isActive": bool} indicating the user is authenticated and if their subscription is active.
            - If no subscription is found, returns an error response.
    """
    try:
        subscription = Subscription.objects.get(user=request.user)
        return Response(
            {"isAuthenticated": True, "isActive": subscription.is_active},
            status=status.HTTP_200_OK,
        )
    except Subscription.DoesNotExist:
        return Response(
            {"error": "No subscription found for the user."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


@api_view(["GET"])
@admin_access_required
def is_admin(request: HttpRequest) -> Response:
    """
    Check if the user is authenticated.

    Args:
        request (HttpRequest): HTTP request object.

    Returns:
        Response: {"is_admin": True} indicating the user is authenticated.
    """
    return Response({"isAdmin": True}, status=status.HTTP_200_OK)


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
        reset_link = f"{BASE_URL_API}reset_password/{uidb64}/{token}/"

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
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


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
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

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

        if not (PASSWORD_MIN_LENGTH <= len(password) <= PASSWORD_MAX_LENGTH):
            return Response(
                {"error": "Password length must be between 8 and 128 characters"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(password)
        user.save()
        LOGGER.info(f"Password reset successfully for user: {user.username}")
        return Response(
            {"message": "Password reset successfully"}, status=status.HTTP_200_OK
        )
