"""
Handles frontend requests and redirects them to the appropriate API.

TODO:
- (ANTI scraping/reverse engineering): Add a system that counts the number of 400 erros per user and send warning + ban
- Split all the code inside files and put it all inside 'controllers' folder
- Define all constants locally and globally (according to the scope)
- Log important messages/errors with user id, clear error name when possible
- Clean the code by adding data types.
- Improve documentation to be concise.
- STOP using differents libs to do the same thing => only use 1
    Use ONLY: status=status.HTTP_200_OK
    Use ONLY: Response to send back data
- Ensure Pylance can recognize variable types and methods.
    EXAMPLE:
    def view_function(request: HttpRequest):
        user = request.user
        # USE THIS instead of 'data'
        parameters: dict = json.loads(request.body)
- Add check if serializer is valid everywhere a serializer is used and return errors + 400_BAD_REQUEST

REMAINING functions to opti and clean:
- def find_user_view_ai(request: HttpRequest) -> Response:
"""

import datetime
import json
import logging
import os
import threading
import jwt
import stripe
from collections import defaultdict
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Subquery, Exists, OuterRef
from django.http import HttpRequest, FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from MailAssistant.utils import security
from MailAssistant.utils.security import subscription
from MailAssistant.ai_providers import claude
from MailAssistant.constants import (
    FREE_PLAN,
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
from MailAssistant.utils.tree_knowledge import Search
from MailAssistant.email_providers import google_api, microsoft_api
from MailAssistant.models import (
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
)
from MailAssistant.utils.serializers import (
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
READ_EMAILS_MARKER = "read"


######################## ENDPOINTS HANDLING GMAIL & OUTLOOK ########################
# ----------------------- GET REQUESTS -----------------------#
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


def forward_request(request: HttpRequest, api_method: str) -> Response:
    """
    Forwards the request to the appropriate API method based on type_api.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameters in the body:
            email (str, optional): User's email address.
        api_method (str): The API method to be called.

    Returns:
        Response: The response from the API method or an error response if
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
        return Response(
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
        return Response(
            {"error": "Unsupported API or method"}, status=status.HTTP_400_BAD_REQUEST
        )


######################## LANGUAGES ########################
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
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
# @permission_classes([IsAuthenticated])
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
# @permission_classes([IsAuthenticated])
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


######################## TIMEZONES ########################
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
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
# @permission_classes([IsAuthenticated])
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


######################## ENDPOINTS TO DELETE ALL USELESS, INFORMATIVE, IMPORTANT EMAILS ########################
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def delete_emails(request: HttpRequest) -> Response:
    """
    Delete emails based on the priority or specific email IDs provided in the request body.

    Args:
        request (HttpRequest): The HTTP request object containing user and body parameters:
            priority (str): Priority level of emails to delete.
            clean (bool): Flag indicating whether to perform a clean deletion.
            emailIds (list[int]): List of specific email IDs to delete.

    Returns:
        Response: JSON response indicating success or failure of email deletion.
    """
    parameters: dict = json.loads(request.body)
    user = request.user
    priority: str = parameters.get("priority")
    clean: bool = parameters.get("clean")

    if not priority:
        return Response(
            {"error": "No priority provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    if priority == READ_EMAILS_MARKER:
        emails = Email.objects.filter(user=user, read=True)
        for email in emails:
            email.delete()

        return Response(
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

    return Response(
        {"message": "Emails deleted successfully"}, status=status.HTTP_200_OK
    )




############################# CONTACT ##############################
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_user_contacts(request: HttpRequest) -> Response:
    """
    Retrieve contacts associated with the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: JSON response containing user's contacts or an error message if no contacts are found.
    """
    try:
        user_contacts = Contact.objects.filter(user=request.user)
    except Contact.DoesNotExist:
        return Response(
            {"error": "No contacts found"}, status=status.HTTP_404_NOT_FOUND
        )

    contacts_serializer = ContactSerializer(user_contacts, many=True)
    return Response(contacts_serializer.data, status=status.HTTP_200_OK)


# ----------------------- REPLY LATER -----------------------#
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_answer_later_emails(request: HttpRequest) -> Response:
    """
    Retrieve emails flagged for answering later by the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object containing the user information.

    Returns:
        Response: JSON response containing the list of emails flagged for answering later,
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

        return Response(formatted_data, status=status.HTTP_200_OK)

    except Exception as e:
        LOGGER.error(f"Error fetching answer-later emails: {str(e)}")
        return Response(
            {"error": "Failed to retrieve answer-later emails."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


######################## DATABASE OPERATIONS ########################
# ----------------------- CREDENTIALS UPDATE-----------------------#
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
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
# @permission_classes([IsAuthenticated])
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


# ----------------------- RULES -----------------------#
# TODO: https://github.com/Teh45/MailAssistant/issues/33
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def set_rule_block_for_sender(request: HttpRequest, email_id):
    user = request.user
    email = get_object_or_404(Email, user=user, id=email_id)

    rule, created = Rule.objects.get_or_create(
        sender=email.sender, user=user, defaults={"block": True}, priority=""
    )
    if not created:
        rule.block = True
        rule.save()

    serializer = RuleBlockUpdateSerializer(rule)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_user_rules(request: HttpRequest) -> Response:
    """
    Retrieves rules associated with the authenticated user.

    Args:
        request (HttpRequest): HTTP request object containing the authenticated user.

    Returns:
        Response: A JSON response containing a list of rules owned by the user.
    """
    user_rules = Rule.objects.filter(user=request.user)
    rules_data = []

    for rule in user_rules:
        rule_serializer = RuleSerializer(rule)
        rule_data = rule_serializer.data

        category_name = rule.category.name if rule.category else None
        sender_name = rule.sender.name if rule.sender else None
        sender_email = rule.sender.email if rule.sender else None

        rule_data["category_name"] = category_name
        rule_data["sender_name"] = sender_name
        rule_data["sender_email"] = sender_email

        rules_data.append(rule_data)

    return Response(rules_data, status=status.HTTP_200_OK)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_user_rule_by_id(request: HttpRequest, id_rule: int) -> Response:
    """
    Retrieves details of a specific rule owned by the authenticated user.

    Args:
        request (HttpRequest): HTTP request object containing the authenticated user.
        id_rule (int): ID of the rule to retrieve.

    Returns:
        Response: A JSON response containing details of the rule.
                      If the rule is not found, returns {"error": "Rule not found"} with status 400.
    """
    try:
        user_rule = Rule.objects.get(id=id_rule, user=request.user)
    except Rule.DoesNotExist:
        return Response({"error": "Rule not found"}, status=status.HTTP_400_BAD_REQUEST)

    rule_serializer = RuleSerializer(user_rule)
    rule_data = rule_serializer.data

    category_name = user_rule.category.name if user_rule.category else None
    sender_name = user_rule.sender.name if user_rule.sender else None
    sender_email = user_rule.sender.email if user_rule.sender else None

    rule_data["category_name"] = category_name
    rule_data["sender_name"] = sender_name
    rule_data["sender_email"] = sender_email

    return Response(rule_data)


@api_view(["DELETE"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def delete_user_rule_by_id(request: HttpRequest, id_rule: int) -> Response:
    """
    Deletes a specific rule owned by the authenticated user.

    Args:
        request (HttpRequest): HTTP request object containing the authenticated user.
        id_rule (int): ID of the rule to delete.

    Returns:
        Response: {"message": "Rule deleted successfully"} if the rule is deleted.
                      {"error": "Rule not found"} with status 400 if the rule doesn't exist for the user.
    """
    try:
        user_rule = Rule.objects.get(id=id_rule, user=request.user)
    except Rule.DoesNotExist:
        return Response({"error": "Rule not found"}, status=status.HTTP_400_BAD_REQUEST)

    user_rule.delete()

    return Response({"message": "Rule deleted successfully"})


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def create_user_rule(request: HttpRequest) -> Response:
    """
    Creates a new rule for the authenticated user based on the request data.

    Args:
        request (HttpRequest): HTTP request object containing rule data in the request body.

    Returns:
        Response: JSON response with the created rule data if successful.
                      {"error": "Details of the specific error."} if there's an issue with the creation.
    """
    data: dict = json.loads(request.body)
    user = request.user

    sender_id = data.get("sender")
    if not sender_id:
        return Response(
            {"error": "Sender ID must be provided"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    existing_rule = Rule.objects.filter(sender_id=sender_id, user=user)
    if existing_rule.exists():
        return Response(
            {"error": "A rule already exists for that sender"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = RuleSerializer(data=data, context={"user": user})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["PUT"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def update_user_rule(request: HttpRequest) -> Response:
    """
    Updates an existing rule for the authenticated user based on the request data.

    Args:
        request (HttpRequest): HTTP request object containing rule data in the request body.

    Returns:
        Response: JSON response with the updated rule data if successful.
                      {"error": "Details of the specific error."} if there's an issue with the update.
    """
    data: dict = json.loads(request.body)
    rule_id = data.get("id")

    try:
        rule = Rule.objects.get(id=rule_id, user=request.user)
    except Rule.DoesNotExist:
        return Response(
            {"error": "Rule not found."}, status=status.HTTP_400_BAD_REQUEST
        )

    serializer = RuleSerializer(
        rule, data=data, partial=True, context={"user": request.user}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


# ----------------------- USER -----------------------#
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def check_sender_for_user(request: HttpRequest) -> Response:
    """
    Check if a sender with the specified email exists.

    Args:
        request (HttpRequest): HTTP request object containing the email to check in the request body.
            Expects JSON body with:
                email (str): The email address of the sender to check.

    Returns:
        Response: Either {"exists": True, "sender_id": sender.id} if the sender exists,
                      or {"exists": False} if the sender does not exist.
    """
    parameters: dict = json.loads(request.body)
    email = parameters.get("email")

    try:
        sender = Sender.objects.get(email=email)
        return Response(
            {"exists": True, "sender_id": sender.id}, status=status.HTTP_200_OK
        )
    except ObjectDoesNotExist:
        return Response({"exists": False}, status=status.HTTP_200_OK)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_user_details(request: HttpRequest) -> Response:
    """Returns the username of authenticated user."""
    return Response({"username": request.user.username})


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_emails_linked(request: HttpRequest) -> Response:
    """
    Returns the list of emails linked to the authenticated user's account.

    Args:
        request (HttpRequest): HTTP request object from the authenticated user.

    Returns:
        Response: A list of linked emails with their type of API if the request is successful,
                      or {"error": "Details of the specific error."} if there's an issue with the retrieval.
    """
    try:
        social_apis = SocialAPI.objects.filter(user=request.user)
        emails_linked = []
        for social_api in social_apis:
            emails_linked.append(
                {"email": social_api.email, "type_api": social_api.type_api}
            )
        return Response(emails_linked, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def search_emails(request: HttpRequest) -> Response:
    """
    Searches emails based on user-specified parameters.

    Args:
        request (HttpRequest): HTTP request object containing the search parameters in the request body.
            Expects JSON body with:
                emails (list of str): List of email addresses to search.
                max_results (int): Maximum number of results to return.
                query (str): The user query for the search.
                file_extensions (list of str): List of file extensions to filter attachments.
                advanced (bool): Flag to indicate if advanced search is enabled.
                from_addresses (list of str): List of sender email addresses to filter.
                to_addresses (list of str): List of recipient email addresses to filter.
                subject (str): Subject of the emails to filter.
                body (str): Body content of the emails to filter.
                date_from (str): Start date to filter emails.
                search_in (dict): Additional search parameters.

    Returns:
        Response: A JSON response with the search results categorized by email provider and email address,
                      or {"error": "Details of the specific error."} if there's an issue with the search process.
    """
    data: dict = json.loads(request.body)
    user = request.user
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
                target=append_to_result,
                args=(
                    GOOGLE_PROVIDER,
                    email,
                    google_api.search_emails(
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
                    microsoft_api.search_emails(
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
                ),
            )

        search_result.start()
        search_result.join()

    return Response(result, status=status.HTTP_200_OK)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def update_user_description(request: HttpRequest) -> Response:
    """
    Updates the user description of the given email.

    Args:
        request (HttpRequest): HTTP request object containing the email and new user description.
            Expects JSON body with:
                email (str): The email associated with the user.
                user_description (str, optional): The new user description to update. Defaults to an empty string.

    Returns:
        Response: A JSON response indicating success or failure of the update operation.
    """
    data: dict = json.loads(request.body)
    user = request.user
    email = data.get("email")
    user_description = data.get("user_description", "")

    if email:
        try:
            social_api = SocialAPI.objects.get(user=user, email=email)
            social_api.user_description = user_description
            social_api.save()
            return Response(
                {"message": "User description updated"}, status=status.HTTP_200_OK
            )
        except SocialAPI.DoesNotExist:
            return Response(
                {"error": "Email not found"}, status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {"error": "No email provided"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_user_description(request: HttpRequest) -> Response:
    """
    Retrieves user description of the given email.

    Args:
        request (HttpRequest): HTTP request object containing the email.
            Expects JSON body with:
                email (str): The email associated with the user.

    Returns:
        Response: A JSON response containing the user description if found,
                      or an error message if no email is provided or if the email is not found.
    """
    data: dict = json.loads(request.body)
    user = request.user
    email = data.get("email")

    if email:
        try:
            social_api = SocialAPI.objects.get(user=user, email=email)
            return Response(
                {"data": social_api.user_description}, status=status.HTTP_200_OK
            )
        except SocialAPI.DoesNotExist:
            return Response(
                {"error": "Email not found"}, status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {"error": "No email provided"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def create_sender(request: HttpRequest) -> Response:
    """
    Create a new sender associated with the authenticated user.

    Args:
        request (HttpRequest): HTTP request object containing the sender data.
            Expects JSON body with:
                email (str): The email of the sender.
                name (str): The name of the sender.

    Returns:
        Response: Either {"id": <sender_id>} if the sender is successfully created,
                      or serializer errors with status HTTP 400 Bad Request if validation fails.
    """
    data: dict = json.loads(request.body)
    serializer = SenderSerializer(data=data)

    if serializer.is_valid():
        sender = Sender.objects.create(email=data["email"], name=data["name"])
        return Response({"id": sender.id}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def delete_email(request: HttpRequest, email_id: int) -> Response:
    """
    Deletes an email associated with the authenticated user.

    Args:
        request (HttpRequest): HTTP request object.
        email_id (int): The ID of the email to delete.

    Returns:
        Response: {"message": "Email deleted successfully"} if the email is deleted successfully,
                      or {"error": <error_message>} with status HTTP 500 Internal Server Error if there's an issue.
    """
    try:
        user = request.user
        email = Email.objects.get(user=user, id=email_id)
        social_api = email.social_api
        type_api = social_api.type_api
        provider_id = email.provider_id
        email.delete()

        if type_api == "google":
            result = google_api.delete_email(user, social_api.email, provider_id)
        elif type_api == "microsoft":
            result = microsoft_api.delete_email(provider_id, social_api)

        if result.get("message", "") == "Email moved to trash successfully!":
            return Response(
                {"message": "Email deleted successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": result.get("error")},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    except Email.DoesNotExist:
        return Response(
            {"error": "Email not found"}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        LOGGER.error(f"Error when deleting email: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def archive_email(request: HttpRequest, email_id: int) -> Response:
    """
    Archives an email associated with the authenticated user.

    Args:
        request (HttpRequest): HTTP request object.
        email_id (int): The ID of the email to archive.

    Returns:
        Response: {"message": "Email archived successfully"} if the email is archived successfully,
                      or {"error": <error_message>} with appropriate status code otherwise.
    """
    try:
        user = request.user
        email = Email.objects.get(user=user, id=email_id)
        email.delete()
        return Response(
            {"message": "Email archived successfully"}, status=status.HTTP_200_OK
        )
    except Email.DoesNotExist:
        return Response(
            {"error": "Email not found"}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        LOGGER.error(f"Error when archiving email: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ----------------------- EMAIL -----------------------#
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_first_email(request: HttpRequest) -> Response:
    """
    Returns the first email associated with the user in the database.

    Args:
        request (HttpRequest): HTTP request object.

    Returns:
        Response: {"email": "<email_address>"} if an email is found.
    """
    user = request.user
    social_api = SocialAPI.objects.filter(user=user).first()

    return Response({"email": social_api.email}, status=status.HTTP_200_OK)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_mail_by_id(request: HttpRequest) -> Response:
    """
    Retrieves details of an email by its ID associated with the authenticated user.

    Args:
        request (HttpRequest): HTTP request object containing the email_id parameter in GET.

    Returns:
        Response:
            {"message": "Authentication successful", "email": {...}} if the email is retrieved successfully.
            {"error": "No email ID provided"} if no email_id parameter is provided in the request.
    """
    user = request.user
    mail_id = request.GET.get("email_id")

    email = get_object_or_404(Email, user=user, provider_id=mail_id)
    social_api = email.social_api
    email_user = social_api.email
    type_api = social_api.type_api

    if mail_id:
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

        return Response(
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
        return Response(
            {"error": "No email ID provided"}, status=status.HTTP_400_BAD_REQUEST
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
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def set_email_unread(request: HttpRequest, email_id: int) -> Response:
    """
    Marks a specific email as unread for the authenticated user.

    Args:
        request (HttpRequest): HTTP request object.
        email_id (int): The ID of the email to mark as unread.

    Returns:
        Response: JSON response with the serialized data of the updated email,
                      status=status.HTTP_200_OK if successful.
    """
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
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def set_email_reply_later(request: HttpRequest, email_id: int) -> Response:
    """
    Marks a specific email for later reply for the authenticated user.

    Args:
        request (HttpRequest): HTTP request object.
        email_id (int): The ID of the email to mark for later reply.

    Returns:
        Response: JSON response with the serialized data of the updated email,
                      status=status.HTTP_200_OK if successful.
    """
    user = request.user
    email = get_object_or_404(Email, user=user, id=email_id)
    email.answer_later = True
    email.save()

    serializer = EmailReplyLaterUpdateSerializer(email)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def set_email_not_reply_later(request: HttpRequest, email_id: int) -> Response:
    """
    Unmarks a specific email for later reply for the authenticated user.

    Args:
        request (HttpRequest): HTTP request object.
        email_id (int): The ID of the email to unmark for later reply.

    Returns:
        Response: JSON response with the serialized data of the updated email,
                      status=status.HTTP_200_OK if successful.
    """
    user = request.user
    email = get_object_or_404(Email, user=user, id=email_id)
    email.answer_later = False
    email.save()

    serializer = EmailReplyLaterUpdateSerializer(email)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@subscription([FREE_PLAN])
def get_user_emails(request: HttpRequest) -> Response:
    """
    Retrieves and formats user emails grouped by category and priority.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: A JSON response containing formatted user emails grouped by category and priority.
                      Each email entry includes details such as ID, provider ID, sender information,
                      subject, content, attachments, date, time, read status, rules applied, and other metadata.
                      Returns status=status.HTTP_200_OK on success.
    """
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

    return Response(formatted_data, status=status.HTTP_200_OK)


####################################################################
######################## UNDER CONSTRUCTION ########################
####################################################################
# ----------------------- EMAIL ATTACHMENT -----------------------#
@api_view(["GET"])
@subscription([FREE_PLAN])
def retrieve_attachment_data(
    request: HttpRequest, email_id: str, attachment_name: str
) -> Response:
    """
    Retrieves email attachment data for a specific email and attachment ID.

    Args:
        request (HttpRequest): The HTTP request object.
        email_id (str): The ID of the email containing the attachment.
        attachment_id (str): The ID of the attachment to retrieve.

    Returns:
        Response: JSON response containing the attachment data.
                      Returns status=status.HTTP_200_OK on success.
    """
    user = request.user
    email = get_object_or_404(Email, user=user, id=email_id)
    social_api = email.social_api

    if social_api.type_api == "google":
        attachment_data = google_api.get_attachment_data(
            user, social_api.email, email.provider_id, attachment_name
        )
        if attachment_data:
            response = HttpResponse(
                attachment_data["data"], content_type="application/octet-stream"
            )
            response["Content-Disposition"] = (
                f'attachment; filename="{attachment_name}"'
            )
            return response
        else:
            return Response({"error": "Attachment not found"}, status=404)
    elif social_api.type_api == "microsoft":
        # TODO: Implement handling for Microsoft API attachments
        return Response(
            {"error": "Microsoft API attachment handling not implemented yet"},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )


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
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.WebhookSignature as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response(
                {"error": "Unhandled event type"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"message": "Received"}, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "Invalid request method"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


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


###########################################################
######################## TO DELETE ########################
###########################################################
# ----------------------- BACKGROUND COLOR-----------------------#
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
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
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        LOGGER.error(f"Serializer errors in set_user_bg_color: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
