"""
Handles regrant consent logic and data synchronization for Google API.

Endpoints:
- ✅ check_connectivity: Checks if Aomail is connected to the user's Google account.
- ✅ synchronize: Synchronizes Aomail database with Google servers.
"""

import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from aomail.utils.security import subscription
from aomail.constants import (
    ALLOWED_PLANS,
)
from aomail.models import Email, SocialAPI, Subscription
from aomail.email_providers.google.authentication import (
    authenticate_service,
    fetch_email_ids_since,
)
from aomail.email_providers.utils import email_to_db


LOGGER = logging.getLogger(__name__)


@api_view(["POST"])
@subscription(ALLOWED_PLANS)
def check_connectivity(request: HttpRequest) -> Response:
    """
    Checks the connectivity status of a user's linked email account.

    Args:
        request (HttpRequest): The HTTP request object containing the user's email.

    Returns:
        Response: Contains the token validity status and the number of missed emails.
    """
    parameters: dict = json.loads(request.body)
    email = parameters["email"]
    user = request.user

    services = authenticate_service(user, email, ["gmail"])
    if not services:
        return Response(
            {"isTokenValid": False},
            status=status.HTTP_200_OK,
        )

    subscription = Subscription.objects.get(user=user)
    start_date = subscription.created_at
    email_ids = fetch_email_ids_since(services["gmail"], start_date)

    nb_missed_emails = 0

    for email_id in email_ids:
        if not Email.objects.filter(user=user, provider_id=email_id).exists():
            nb_missed_emails += 1

    return Response(
        {"isTokenValid": True, "nbMissedEmails": nb_missed_emails},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@subscription(ALLOWED_PLANS)
def synchronize(request: HttpRequest) -> Response:
    """
    Synchronizes Aomail DB with Google servers by fetching and processing email IDs.

    Args:
        request (HttpRequest): The HTTP request object containing the user's email and
                               the number of missed emails.

    Returns:
        Response: Contains the number of emails processed from the user's inbox.
    """
    parameters: dict = json.loads(request.body)
    email = parameters["email"]
    nb_missed_emails = parameters["nbMissedEmails"]
    user = request.user

    services = authenticate_service(user, email, ["gmail"])

    subscription = Subscription.objects.get(user=user)
    start_date = subscription.created_at
    email_ids = fetch_email_ids_since(services["gmail"], start_date)

    social_api = SocialAPI.objects.get(user=user, email=email)

    LOGGER.info(
        f"Starting to process {len(email_ids)} emails for user ID: {user.id} and social API ID: {social_api.id}"
    )

    nb_processed_emails = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_email_id = {}

        for email_id in email_ids:
            if Email.objects.filter(provider_id=email_id).exists():
                continue

            future = executor.submit(email_to_db, social_api, email_id)
            future_to_email_id[future] = email_id

        for future in as_completed(future_to_email_id):
            email_id = future_to_email_id[future]
            try:
                if future.result():  # Increment count if email_to_db returns True
                    nb_processed_emails += 1
            except Exception as e:
                LOGGER.error(f"Error processing email ID {email_id}: {str(e)}")

    LOGGER.info(
        f"All emails have been processed. Processed: {nb_processed_emails}, Missed: {nb_missed_emails}"
    )

    return Response(
        {"nbProcessedEmails": nb_processed_emails},
        status=status.HTTP_200_OK,
    )
