"""
Handles searching emails using email providers APIs, filtering, sorting, and retrieving email content.

Endpoints:
- ✅ get_api_emails_ids: Searches emails based on user-specified parameters.
- ✅ get_api_emails_data: Retrieves formatted email basic data to be displayed.
"""

import json
import logging
import threading
from django.http import HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from aomail.utils.security import subscription
from aomail.email_providers.microsoft import (
    email_operations as email_operations_microsoft,
)
from aomail.email_providers.google import (
    email_operations as email_operations_google,
)
from aomail.email_providers.imap import (
    email_operations as email_operations_imap,
)
from aomail.email_providers.google import authentication as auth_google
from aomail.email_providers.microsoft import authentication as auth_microsoft
from aomail.constants import (
    ALLOWED_PLANS,
    GOOGLE,
    GOOGLE,
    MICROSOFT,
    MICROSOFT,
)
from aomail.models import (
    SocialAPI,
)

LOGGER = logging.getLogger(__name__)


@api_view(["POST"])
@subscription(ALLOWED_PLANS)
def get_api_emails_data(request: HttpRequest) -> Response:
    """
    ⚠️ Images are saved as duplicates each time the user opens an old email. Reason: images are saved with get_mail_to_db

    Retrieve detailed email data for a given list of email IDs.

    Args:
        request (HttpRequest): The HTTP request object containing JSON data with email IDs.

    Returns:
        Response: A JSON object containing detailed email data, categorized by provider and email address
    """
    try:
        user = request.user
        payload: dict = json.loads(request.body)
        data: dict[str, dict[str, list[str]]] = payload.get("limitedApiIds", {})

        nb_ids = 0
        for dict_emails in data.values():
            for list_ids in dict_emails.values():
                nb_ids += len(list_ids)

        if not (0 <= nb_ids <= 100):
            return Response(
                {"error": "Number of IDs accepted: from 0 to 100"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = {}
        for provider, dict_emails in data.items():
            result[provider] = {}

            for email, list_ids in dict_emails.items():
                result[provider][email] = {}

                for id in list_ids:
                    try:
                        social_api = SocialAPI.objects.get(email=email, user=user)
                        if social_api.imap_config:
                            email_data = email_operations_imap.get_mail_to_db(
                                social_api, id
                            )
                        elif provider == GOOGLE:
                            email_data = email_operations_google.get_mail_to_db(
                                social_api, id
                            )
                        elif provider == MICROSOFT:
                            email_data = email_operations_microsoft.get_mail_to_db(
                                social_api, id
                            )

                        if email_data:
                            result[provider][email][id] = {
                                "providerId": id,
                                "subject": email_data["subject"],
                                "sender": {
                                    "name": email_data["from_info"][0],
                                    "email": email_data["from_info"][1],
                                },
                                "hasAttachments": email_data["has_attachments"],
                                "cc": (
                                    [
                                        {"name": cc[0], "email": cc[1]}
                                        for cc in email_data["cc_info"]
                                    ]
                                    if email_data.get("cc_info")
                                    else []
                                ),
                                "bcc": (
                                    [
                                        {"name": cc[0], "email": cc[1]}
                                        for cc in email_data["bcc_info"]
                                    ]
                                    if email_data.get("bcc_info")
                                    else []
                                ),
                                "attachments": email_data["attachments"],
                                "sentDate": email_data["sent_date"].strftime(
                                    "%Y-%m-%d"
                                ),
                                "sentTime": email_data["sent_date"].strftime("%H:%M"),
                            }
                        else:
                            LOGGER.error(f"No email data returned for ID: {id}")
                            continue
                    except SocialAPI.DoesNotExist:
                        LOGGER.error(f"Social API not found for email: {email}")
                        continue
                    except Exception as e:
                        LOGGER.error(f"Error processing email ID {id}: {str(e)}")
                        continue
        return Response(
            {"data": result},
            status=status.HTTP_200_OK,
        )
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON in request body"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        LOGGER.error(f"Error retrieving API emails data from ids: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@subscription(ALLOWED_PLANS)
def get_api_emails_ids(request: HttpRequest) -> Response:
    """
    Searches emails based on user-specified parameters.

    Args:
        request (HttpRequest): HTTP request object containing the search parameters in the request body.
            Expects JSON body with:
                emailProvider (list[str]): List of email providers to filter by.
                maxResults (int): Maximum number of results to return.
                query (str): The user query for the search.
                fileExtensions (list[str]): List of file extensions to filter attachments.
                advanced (bool): Flag to indicate if advanced search is enabled.
                fromAddresses (list[str]): List of sender email addresses to filter.
                toAddresses (list[str]): List of recipient email addresses to filter.
                subject (str): Subject of the emails to filter.
                body (str): Body content of the emails to filter.
                dateFrom (str): Start date to filter emails.
                searchIn (dict[str, bool], optional): A dictionary specifying the folders to search in:
                    spams: Search in spam/junk folder.
                    deleted_emails: Search in deleted items folder.
                    drafts: Search in drafts folder.
                    sent_emails: Search in sent items folder.

    Returns:
        Response: A JSON response with the search results categorized by email provider and email address,
                      or {"error": "Details of the specific error."} if there's an issue with the search process.
    """
    data: dict = json.loads(request.body)
    user = request.user
    email_provider: list[str] = data.get("emailProvider", [GOOGLE, MICROSOFT])
    max_results: int = data.get("maxResults")
    query: str = data.get("query")
    file_extensions: list = data.get("fileExtensions")
    filenames: list = data.get("filenames")
    advanced: bool = data.get("advanced")
    from_addresses: list = data.get("fromAddresses")
    to_addresses: list = data.get("toAddresses")
    subject: str = data.get("subject")
    body: str = data.get("body")
    date_from: str = data.get("dateFrom")
    search_in: dict = data.get("searchIn")

    def append_to_result(provider: str, email: str, data: list):
        if len(data) > 0:
            if provider not in result:
                result[provider] = {}
            result[provider][email] = data

    result = {}
    for provider in email_provider:
        social_apis = SocialAPI.objects.filter(user=user, type_api=provider)

        for social_api in social_apis:
            email = social_api.email
            social_api = SocialAPI.objects.get(email=email)
            type_api = social_api.type_api

            if type_api == GOOGLE and not social_api.imap_config:
                services = auth_google.authenticate_service(user, email, ["gmail"])
                search_result = threading.Thread(
                    target=append_to_result,
                    args=(
                        GOOGLE,
                        email,
                        email_operations_google.search_emails_manually(
                            services,
                            query,
                            max_results,
                            file_extensions,
                            filenames,
                            advanced,
                            search_in,
                            from_addresses,
                            to_addresses,
                            subject,
                            body,
                            date_from,
                        ),
                    ),
                )
            elif type_api == MICROSOFT and not social_api.imap_config:
                access_token = auth_microsoft.refresh_access_token(
                    auth_microsoft.get_social_api(user, email)
                )
                search_result = threading.Thread(
                    target=append_to_result,
                    args=(
                        MICROSOFT,
                        email,
                        email_operations_microsoft.search_emails_manually(
                            access_token,
                            query,
                            max_results,
                            file_extensions,
                            filenames,
                            advanced,
                            search_in,
                            from_addresses,
                            to_addresses,
                            subject,
                            body,
                            date_from,
                        ),
                    ),
                )
            elif social_api.imap_config:
                search_result = threading.Thread(
                    target=append_to_result,
                    args=(
                        social_api.type_api,
                        social_api.email,
                        email_operations_imap.search_emails_manually(
                            social_api,
                            query,
                            max_results,
                            file_extensions,
                            filenames,
                            advanced,
                            search_in,
                            from_addresses,
                            to_addresses,
                            subject,
                            body,
                            date_from,
                        ),
                    ),
                )

            search_result.start()
            search_result.join()

    return Response(result, status=status.HTTP_200_OK)
