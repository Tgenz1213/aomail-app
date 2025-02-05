"""
Handles authentication processes and credential operations for Microsoft Graph API.

Endpoints:
- ✅ generate_auth_url: Get authorization URL for the signup page.
- ✅ auth_url_link_email: Get authorization URL for the settings page.
- ✅ auth_url_regrant: Get authorization URL for regranting consent.
"""

import json
import logging
import requests
from datetime import datetime
from collections import defaultdict
from urllib.parse import urlencode
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from msal import ConfidentialClientApplication
from aomail.utils.security import subscription
from aomail.utils import security
from aomail.constants import (
    ALLOWED_PLANS,
    GRAPH_URL,
    MICROSOFT_AUTHORITY,
    MICROSOFT_CLIENT_ID,
    MICROSOFT_CLIENT_SECRET,
    MICROSOFT_CLIENT_STATE,
    MICROSOFT_SCOPES,
    REDIRECT_URI_LINK_EMAIL,
    REDIRECT_URI_SIGNUP,
    SOCIAL_API_REFRESH_TOKEN_KEY,
)
from aomail.models import SocialAPI, Subscription


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


def generate_auth_url(request: HttpRequest) -> HttpResponseRedirect:
    """
    Generate a connection URL to obtain the authorization code for Microsoft.

    Args:
        request (HttpRequest): HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the Microsoft authorization URL.
    """
    try:
        ip = security.get_ip_with_port(request)
        LOGGER.info(f"Initiating Microsoft OAuth flow from IP: {ip}")

        params = {
            "client_id": MICROSOFT_CLIENT_ID,
            "response_type": "code",
            "redirect_uri": REDIRECT_URI_SIGNUP,
            "response_mode": "query",
            "scope": " ".join(MICROSOFT_SCOPES),
            "state": MICROSOFT_CLIENT_STATE,
            "prompt": "consent",
        }
        authorization_url = (
            f"{MICROSOFT_AUTHORITY}/oauth2/v2.0/authorize?{urlencode(params)}"
        )

        LOGGER.info(
            f"Successfully redirected to Microsoft authorization URL from IP: {ip}"
        )
        return redirect(authorization_url)

    except Exception as e:
        LOGGER.error(f"Error generating Microsoft OAuth URL: {str(e)}")


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
    app = ConfidentialClientApplication(
        client_id=MICROSOFT_CLIENT_ID,
        client_credential=MICROSOFT_CLIENT_SECRET,
        authority=MICROSOFT_AUTHORITY,
    )

    result = app.acquire_token_by_authorization_code(
        authorization_code, scopes=MICROSOFT_SCOPES, redirect_uri=REDIRECT_URI_SIGNUP
    )

    if result:
        return result.get("access_token"), result.get("refresh_token")
    else:
        return None, None


@api_view(["GET"])
@subscription(ALLOWED_PLANS)
def auth_url_link_email(request: HttpRequest) -> HttpResponseRedirect:
    """
    Generates a connection URL to obtain the authorization code for linking an email account with Microsoft.

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
        LOGGER.info(f"Initiating Microsoft OAuth flow from IP: {ip}")

        params = {
            "client_id": MICROSOFT_CLIENT_ID,
            "response_type": "code",
            "redirect_uri": REDIRECT_URI_LINK_EMAIL,
            "response_mode": "query",
            "scope": " ".join(MICROSOFT_SCOPES),
            "state": MICROSOFT_CLIENT_STATE,
            "prompt": "consent",
        }
        authorization_url = (
            f"{MICROSOFT_AUTHORITY}/oauth2/v2.0/authorize?{urlencode(params)}"
        )
        LOGGER.info(
            f"Successfully redirected to Microsoft authorization URL from IP: {ip}"
        )
        return Response(
            {"authorizationUrl": authorization_url},
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        LOGGER.error(f"Error generating Microsoft OAuth URL: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def fetch_email_ids_since(access_token: str, start_date: datetime) -> list[str]:
    """
    Fetches email IDs from the user's inbox since the specified start date.

    Args:
        access_token (str): The access token for authenticating requests to the API.
        start_date (datetime): The date from which to fetch email IDs.

    Returns:
        list[str]: A list of email IDs retrieved from the inbox, or an empty list
                    if an error occurs.
    """
    headers = get_headers(access_token)
    start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%S") + "Z"

    try:
        response = requests.get(
            f"{GRAPH_URL}me/messages?$filter=receivedDateTime ge {start_date_str}",
            headers=headers,
        )

        if response.status_code == 200:
            messages = response.json().get("value", [])
            email_ids = [message["id"] for message in messages]
            return email_ids
        else:
            LOGGER.error(f"Error fetching email IDs: {response.text}")
            return []

    except Exception as e:
        LOGGER.error(f"Exception while fetching email IDs: {str(e)}")
        return []


@api_view(["POST"])
@subscription(ALLOWED_PLANS)
def auth_url_regrant(request: HttpRequest) -> HttpResponseRedirect:
    """
    Generates a Microsoft re-consent authorization URL for linking an email account.

    Args:
        request (HttpRequest): The HTTP request object containing the user's email.

    Returns:
        HttpResponseRedirect: Redirects the user to the generated authorization URL for re-consent.
    """
    try:
        parameters: dict = json.loads(request.body)
        email = parameters.get("email", "")

        ip = security.get_ip_with_port(request)
        LOGGER.info(
            f"Initiating Microsoft OAuth regrant flow from IP: {ip} for email: {email}"
        )

        if not email:
            return Response(
                {"error": "No email provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        params = {
            "client_id": MICROSOFT_CLIENT_ID,
            "response_type": "code",
            "redirect_uri": REDIRECT_URI_LINK_EMAIL,
            "response_mode": "query",
            "scope": " ".join(MICROSOFT_SCOPES),
            "state": MICROSOFT_CLIENT_STATE,
            "prompt": "consent",
            "login_hint": email,
        }
        authorization_url = (
            f"{MICROSOFT_AUTHORITY}/oauth2/v2.0/authorize?{urlencode(params)}"
        )

        LOGGER.info(
            f"Successfully redirected to Microsoft regrant authorization URL from IP: {ip} for email: {email}"
        )
        return Response(
            {"authorizationUrl": authorization_url},
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        LOGGER.error(f"Error generating Microsoft OAuth regrant URL: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def link_email_tokens(authorization_code: str) -> tuple[str, str] | tuple[None, None]:
    """
    Exchange authorization code for access and refresh tokens with Microsoft.

    Args:
        authorization_code (str): Authorization code obtained from the OAuth2 flow.

    Returns:
        tuple: A tuple containing the access token and refresh token if successful,
               otherwise (None, None) if credentials are not obtained.
    """
    app = ConfidentialClientApplication(
        client_id=MICROSOFT_CLIENT_ID,
        client_credential=MICROSOFT_CLIENT_SECRET,
        authority=MICROSOFT_AUTHORITY,
    )

    result = app.acquire_token_by_authorization_code(
        authorization_code,
        scopes=MICROSOFT_SCOPES,
        redirect_uri=REDIRECT_URI_LINK_EMAIL,
    )
    if result:
        return result.get("access_token"), result.get("refresh_token")
    else:
        return None, None


def get_headers(access_token: str) -> dict:
    """
    Returns the default headers for making authenticated API requests.

    Args:
        access_token (str): The access token obtained from OAuth2 authentication.

    Returns:
        dict: A dictionary containing the HTTP headers with 'Content-Type' set to 'application/json'
              and 'Authorization' set to the provided access token using the Bearer scheme.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    return headers


def get_social_api(user: User, email: str) -> SocialAPI | None:
    """
    Retrieves the SocialAPI instance associated with the specified user and email.

    Args:
        user: The user object for whom the SocialAPI instance is retrieved.
        email (str): The email address associated with the SocialAPI instance.

    Returns:
        SocialAPI or None: The SocialAPI instance if found, otherwise None.
    """
    try:
        social_api = SocialAPI.objects.get(user=user, email=email)
        return social_api
    except SocialAPI.DoesNotExist:
        LOGGER.error(
            f"No credentials found for user with ID {user.id} and email {email}"
        )
        return None


def is_token_valid(access_token: str) -> bool:
    """
    Checks if the access token is still valid by making a sample request to a sample URL.

    Args:
        access_token (str): The access token to be validated.

    Returns:
        bool: True if the access token is valid (status code 200), False otherwise.
    """
    sample_url = f"{GRAPH_URL}me"
    headers = get_headers(access_token)
    response = requests.get(sample_url, headers=headers)
    return response.status_code == 200


def refresh_access_token(social_api: SocialAPI) -> str | None:
    """
    Returns a valid access token for the provided SocialAPI instance.

    Args:
        social_api (SocialAPI): The SocialAPI instance containing the access and refresh tokens.

    Returns:
        str | None: A valid access token if successfully refreshed, otherwise None.
    """
    access_token = social_api.access_token

    if is_token_valid(access_token):
        return access_token

    refresh_url = f"{MICROSOFT_AUTHORITY}/oauth2/v2.0/token"
    refresh_token_encrypted = social_api.refresh_token
    refresh_token = security.decrypt_text(
        SOCIAL_API_REFRESH_TOKEN_KEY, refresh_token_encrypted
    )
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": MICROSOFT_CLIENT_ID,
        "client_secret": MICROSOFT_CLIENT_SECRET,
        "scope": " ".join(MICROSOFT_SCOPES),
    }

    response = requests.post(refresh_url, data=data)
    response_data: defaultdict = response.json()

    if "access_token" in response_data:
        access_token = response_data["access_token"]
        social_api.access_token = access_token
        social_api.save()
        return access_token
    else:
        error = response_data.get("error_description", response.reason)
        LOGGER.error(
            f"Failed to refresh access token for email {social_api.email}: {error}"
        )
        return None
