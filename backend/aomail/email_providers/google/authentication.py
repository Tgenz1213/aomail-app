"""
Handles authentication processes and credential operations for Google API.

Endpoints:
- ✅ generate_auth_url: Get authorization URL for the signup page.
- ✅ auth_url_link_email: Get authorization URL for the settings page.
- ✅ auth_url_regrant: Get authorization URL for regranting consent.
"""

import json
import logging
from datetime import datetime
from django.http import HttpRequest, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.shortcuts import redirect
from google.auth import exceptions as auth_exceptions
from google.auth.transport.requests import Request
from google.oauth2 import credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from aomail.utils import security
from aomail.utils.security import subscription
from aomail.constants import (
    ALLOWED_PLANS,
    ENCRYPTION_KEYS,
    GOOGLE_CONFIG,
    GOOGLE_CREDS,
    REDIRECT_URI_LINK_EMAIL,
    REDIRECT_URI_SIGNUP,
    GOOGLE_SCOPES,
)
from aomail.models import SocialAPI, Subscription


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


def generate_auth_url(request: HttpRequest) -> HttpResponseRedirect:
    """
    Generate a connection URL to obtain the authorization code.

    Args:
        request (HttpRequest): HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the Google authorization URL.
    """
    try:
        ip = security.get_ip_with_port(request)
        LOGGER.info(f"Initiating Google OAuth flow from IP: {ip}")

        flow = Flow.from_client_secrets_file(
            GOOGLE_CREDS, scopes=GOOGLE_SCOPES, redirect_uri=REDIRECT_URI_SIGNUP
        )
        authorization_url, _ = flow.authorization_url(
            access_type="offline", include_granted_scopes="true", prompt="consent"
        )
        LOGGER.info(
            f"Successfully redirected to Google authorization URL from IP: {ip}"
        )
        return redirect(authorization_url)

    except Exception as e:
        LOGGER.error(f"Error generating Google OAuth URL: {str(e)}")


def exchange_code_for_tokens(
    authorization_code: str,
) -> tuple[str, str] | tuple[None, None]:
    """
    Exchange authorization code for access and refresh tokens.

    Args:
        authorization_code (str): Authorization code obtained from the OAuth2 flow.

    Returns:
        tuple: A tuple containing the access token and refresh token if successful,
               otherwise (None, None) if credentials are not obtained.
    """
    flow = Flow.from_client_secrets_file(
        GOOGLE_CREDS, scopes=GOOGLE_SCOPES, redirect_uri=REDIRECT_URI_SIGNUP
    )
    flow.fetch_token(code=authorization_code)

    credentials = flow.credentials

    if credentials:
        access_token = credentials.token
        refresh_token = credentials.refresh_token

        return access_token, refresh_token
    else:
        return None, None


@api_view(["GET"])
@subscription(ALLOWED_PLANS)
def auth_url_link_email(request: HttpRequest) -> HttpResponseRedirect:
    """
    Generates a connection URL to obtain the authorization code for linking an email account.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects the user to the generated authorization URL.
    """
    try:
        subscription = Subscription.objects.get(user=request.user)
        if subscription.is_trial:
            return Response(
                {"error": "User can only link 1 email with a free trial"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ip = security.get_ip_with_port(request)
        LOGGER.info(f"Initiating Google OAuth flow from IP: {ip}")

        flow = Flow.from_client_secrets_file(
            GOOGLE_CREDS, scopes=GOOGLE_SCOPES, redirect_uri=REDIRECT_URI_LINK_EMAIL
        )
        authorization_url, _ = flow.authorization_url(
            access_type="offline", include_granted_scopes="true", prompt="consent"
        )
        LOGGER.info(
            f"Successfully redirected to Google authorization URL from IP: {ip}"
        )
        return Response(
            {"authorizationUrl": authorization_url},
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        LOGGER.error(f"Error generating Google OAuth URL: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def fetch_email_ids_since(service, start_date: datetime) -> list[str]:
    """
    Fetches email IDs from the user's Gmail inbox since the specified start date.

    Args:
        service: The authenticated Gmail API service instance.
        start_date (datetime): The date from which to fetch email IDs.

    Returns:
        list[str]: A list of email IDs retrieved from the inbox, or an empty list
                    if an error occurs.
    """
    try:
        results = (
            service.users()
            .messages()
            .list(userId="me", q=f"after:{int(start_date.timestamp())}")
            .execute()
        )
        messages = results.get("messages", [])
        email_ids = [message["id"] for message in messages]

        return email_ids

    except Exception as e:
        LOGGER.error(f"Error fetching email IDs: {str(e)}")
        return []


@api_view(["POST"])
@subscription(ALLOWED_PLANS)
def auth_url_regrant(request: HttpRequest) -> HttpResponseRedirect:
    """
    Generates a connection URL for regranting consent to link an existing email account.

    Args:
        request (HttpRequest): The HTTP request object, expected to contain the user's email
                               in JSON format within the request body.

    Returns:
        HttpResponseRedirect: Redirects the user to the generated Google re-consent
                              authorization URL if email is provided, or an error response otherwise.
    """
    try:
        parameters: dict = json.loads(request.body)
        email = parameters.get("email", "")

        ip = security.get_ip_with_port(request)
        LOGGER.info(
            f"Initiating Google OAuth regrant flow from IP: {ip} for email: {email}"
        )

        if not email:
            return Response(
                {"error": "No email provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        flow = Flow.from_client_secrets_file(
            GOOGLE_CREDS,
            scopes=GOOGLE_SCOPES,
            redirect_uri=REDIRECT_URI_LINK_EMAIL,
        )

        authorization_url, _ = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent",
            login_hint=email,
        )

        LOGGER.info(
            f"Redirected to Google regrant authorization URL for re-consent with login_hint for {email}"
        )

        return Response(
            {"authorizationUrl": authorization_url},
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        LOGGER.error(f"Error generating Google OAuth regrant URL: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def link_email_tokens(authorization_code: str) -> tuple[str, str] | tuple[None, None]:
    """
    Exchange authorization code for access and refresh tokens.

    Args:
        authorization_code (str): Authorization code obtained from the OAuth2 flow.

    Returns:
        tuple: A tuple containing the access token and refresh token if successful,
               otherwise (None, None) if credentials are not obtained.
    """
    flow = Flow.from_client_secrets_file(
        GOOGLE_CREDS, scopes=GOOGLE_SCOPES, redirect_uri=REDIRECT_URI_LINK_EMAIL
    )
    flow.fetch_token(code=authorization_code)

    credentials = flow.credentials

    if credentials:
        access_token = credentials.token
        refresh_token = credentials.refresh_token

        return access_token, refresh_token
    else:
        return None, None


def get_credentials(user: User, email: str) -> credentials.Credentials | None:
    """
    Retrieve and return Google API credentials for the specified user and email.

    Args:
        user (User): The user object.
        email (str): The email address associated with the user's Google account.

    Returns:
        credentials.Credentials or None: The Google API credentials, or None if not found.
    """
    try:
        social_api = SocialAPI.objects.get(user=user, email=email)
        refresh_token_encrypted = social_api.refresh_token
        refresh_token = security.decrypt_text(
            ENCRYPTION_KEYS["SocialAPI"]["refresh_token"], refresh_token_encrypted
        )
        creds_data = {
            "token": social_api.access_token,
            "refresh_token": refresh_token,
            "token_uri": GOOGLE_CONFIG["token_uri"],
            "client_id": GOOGLE_CONFIG["client_id"],
            "client_secret": GOOGLE_CONFIG["client_secret"],
            "scopes": GOOGLE_SCOPES,
        }
        creds = credentials.Credentials.from_authorized_user_info(creds_data)
    except SocialAPI.DoesNotExist:
        LOGGER.error(f"No credentials for user with ID {user.id} and email: {email}")
        creds = None

    return creds


def get_social_api(user: User, email: str) -> SocialAPI | None:
    """
    Retrieve and return the SocialAPI instance for the specified user and email.

    Args:
        user (User): The user object.
        email (str): The email address associated with the user's social API.

    Returns:
        SocialAPI or None: The SocialAPI instance, or None if not found.
    """
    try:
        social_api = SocialAPI.objects.get(user=user, email=email)
        return social_api
    except SocialAPI.DoesNotExist:
        LOGGER.error(
            f"No credentials found for user with ID {user.id} and email {email}"
        )
        return None


def refresh_credentials(
    creds: credentials.Credentials,
) -> credentials.Credentials | None:
    """
    Refresh the given Google API credentials.

    Args:
        creds (credentials.Credentials): The Google API credentials to refresh.

    Returns:
        credentials.Credentials or None: The refreshed credentials, or None if refresh fails.
    """
    try:
        creds.refresh(Request())
    except auth_exceptions.RefreshError as e:
        LOGGER.error(f"Failed to refresh credentials: {str(e)}")
        creds = None
    return creds


def save_credentials(creds: credentials.Credentials, user: User, email: str):
    """
    Update the database with the new access token for the specified user and email.

    Args:
        creds (credentials.Credentials): The updated Google API credentials.
        user (User): The user object.
        email (str): The email address associated with the user's social API.
    """
    try:
        social_api = SocialAPI.objects.get(user=user, email=email)
        social_api.access_token = creds.token
        social_api.save()
    except Exception as e:
        LOGGER.error(f"Failed to save credentials: {str(e)}")


def build_services(
    creds: credentials.Credentials, required_services: list[str] = ["gmail", "people"]
) -> dict:
    """
    Builds and returns a dictionary of specified Google API service endpoints.

    Args:
        creds (credentials.Credentials): The Google API credentials to use for building the services.
        required_services (list[str]): List of service names to initialize.

    Returns:
        dict: A dictionary containing only the requested Google API service endpoints,
              where keys are service names and values are the initialized service objects.
    """
    available_services = {
        "gmail": lambda: build("gmail", "v1", cache_discovery=False, credentials=creds),
        "people": lambda: build(
            "people", "v1", cache_discovery=False, credentials=creds
        ),
    }

    services = {
        name: available_services[name]()
        for name in required_services
        if name in available_services
    }

    return services


def authenticate_service(
    user: User,
    email: str,
    required_services: list[str] = None,
) -> dict | None:
    """
    Authenticate and build Google API services for the specified user and email.

    Args:
        user (User): The user object containing information about the user.
        email (str): The email address associated with the user's Google account.
        required_services (list[str], optional): A list of strings specifying which Google API

    Returns:
        dict or None: A dictionary of Google API service endpoints for the requested services,
                      or None if authentication fails or if no valid services are specified.
    """
    creds = get_credentials(user, email)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds = refresh_credentials(creds)
        if creds:
            save_credentials(creds, user, email)
        else:
            LOGGER.error(
                f"Failed to authenticate for user with ID {user.id} and email: {email}"
            )
            return None

    services = build_services(creds, required_services or ["gmail", "people"])
    return services
