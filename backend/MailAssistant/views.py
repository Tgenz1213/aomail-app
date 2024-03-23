"""
Handles frontend requests and redirects them to the appropriate API.
"""

import json
import logging
import re
import threading
import jwt
from collections import defaultdict
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Subquery, Exists, OuterRef
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from MailAssistant.ai_providers import gpt_3_5_turbo, mistral, claude
from MailAssistant.email_providers import google_api, microsoft_api
from .models import (
    Category,
    SocialAPI,
    Email,
    Rule,
    Preference,
    Sender,
    Contact,
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


######################## REGISTRATION ########################
@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    """Register user in mailassistandb and handles the callback of the API with Oauth2.0

    APIs taken into account:
        - Gmail API (Google)
        - Graph API (Microsoft)
    """
    # Extract user data from the request
    type_api = request.data.get("type_api")
    code = request.data.get("code")
    username = request.data.get("login")
    password = request.data.get("password")
    theme = request.data.get("theme")
    color = request.data.get("color")
    categories = request.data.get("categories")

    # Validate user data
    validation_result = validate_signup_data(username, password, code)
    if "error" in validation_result:
        return Response(validation_result, status=400)

    # Checks if the authorization code is valid
    authorization_result = validate_authorization_code(type_api, code)

    if "error" in authorization_result:
        return Response({"error": authorization_result["error"]}, status=400)

    # Extract tokens and email from the authorization result
    access_token = authorization_result["access_token"]
    refresh_token = authorization_result["refresh_token"]
    email = authorization_result["email"]

    # Check email requirements
    if email:
        if SocialAPI.objects.filter(email=email).exists():
            return Response({"error": "Email address already used"}, status=400)
        elif " " in email:
            return Response(
                {"error": "Email address must not contain spaces"}, status=400
            )
    else:
        # Google Oauth2.0 returns a refresh token only at first consent
        return Response({"error": "Email address already used"}, status=400)

    # Create and save user
    user = User.objects.create_user(username, "", password)
    user_id = user.id
    refresh = RefreshToken.for_user(user)
    jwt_access_token = str(refresh.access_token)
    user.save()

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
        return Response({"error": str(e)}, status=400)

    # Save user data
    result = save_user_data(
        user, type_api, email, access_token, refresh_token, theme, color, categories
    )
    if "error" in result:
        return Response(result, status=400)

    # Create the Google listener
    if type_api == "google":
        google_api.subscribe_to_email_notifications(user, email, 'chrome-cipher-268712', 'mail_push')

    return Response(
        {"user_id": user_id, "access_token": jwt_access_token, "email": email},
        status=201,
    )


def validate_authorization_code(type_api, code):
    """Validates the authorization code for a given API type"""
    try:
        if type_api == "google":
            access_token, refresh_token = google_api.exchange_code_for_tokens(code)
            email = google_api.get_email(access_token, refresh_token)
        elif type_api == "microsoft":
            access_token, refresh_token = microsoft_api.exchange_code_for_tokens(code)
            email = microsoft_api.get_email(access_token)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "email": email,
        }
    except Exception as e:
        LOGGER.error(f"Error in validate_authorization_code: {str(e)}")
        return {"error": str(e)}


def validate_signup_data(username, password, code):
    """Validates user signup data to ensure all requirements are met"""
    if not code:
        return {"error": "No authorization code provided"}

    # Check if user requirements
    if User.objects.filter(username=username).exists():
        return {"error": "Username already exists"}
    elif " " in username:
        return {"error": "Username must not contain spaces"}

    # Check passwords requirements
    if not (8 <= len(password) <= 32):
        return {"error": "Password length must be between 8 and 32 characters"}
    if " " in password:
        return {"error": "Password must not contain spaces"}
    elif not re.match(r"^[a-zA-Z0-9!@#$%^&*()-=_+]+$", password):
        return {"error": "Password contains invalid characters"}

    return {"status": 200}


def save_user_data(
    user, type_api, email, access_token, refresh_token, theme, color, categories
):
    """Store user creds and settings in DB"""
    try:
        social_api = SocialAPI(
            user=user,
            type_api=type_api,
            email=email,
            access_token=access_token,
            refresh_token=refresh_token,
        )
        social_api.save()

        # Save user preferences
        preference = Preference(theme=theme, bg_color=color, user=user)
        preference.save()

        # Save user categories
        if categories:
            try:
                categories_j = json.loads(categories)
                for category_data in categories_j:
                    category_name = category_data.get("name")
                    category_description = category_data.get("description")

                    category = Category(
                        name=category_name, description=category_description, user=user
                    )
                    category.save()
            except json.JSONDecodeError:
                return {"error": "Invalid categories data"}

        # Creation of the Other/default category => TO UPDATE WITH THE LANGUAGE
        default_category = Category(name="Autres", description="Choose this category only as a last resort, if you can't place the mail in any other category", user=user)
        default_category.save()

        return {"message": "User data saved successfully"}

    except Exception as e:
        LOGGER.error(f"Error in save_user_data: {str(e)}")
        return {"error": str(e)}


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def is_authenticated(request):
    """Used in index.js by the router to check if the user can access enpoints"""
    return JsonResponse({"isAuthenticated": True}, status=200)


######################## ENDPOINTS HANDLING GMAIL & OUTLOOK ########################
# ----------------------- GET REQUESTS -----------------------#
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def unread_mails(request):
    """Returns the number of unread emails"""
    return forward_request(request._request, "unread_mails")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile_image(request):
    """Returns the profile image of the user"""
    return forward_request(request._request, "get_profile_image")


# ----------------------- POST REQUESTS -----------------------#
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_email(request):
    return forward_request(request._request, "send_email")


def forward_request(request, api_method):
    """Forwards the request to the appropriate API method based on type_api"""
    user = request.user
    email = request.headers.get("email")

    try:
        social_api = get_object_or_404(SocialAPI, user=user, email=email)
        type_api = social_api.type_api
    except SocialAPI.DoesNotExist:
        LOGGER.error(
            f"SocialAPI entry not found for the user with ID: {user.id} and email: {email}"
        )
        return JsonResponse(
            {"error": "SocialAPI entry not found for the user and email"}, status=404
        )

    api_module = None
    if type_api == "google":
        api_module = google_api
    elif type_api == "microsoft":
        api_module = microsoft_api

    if api_module and hasattr(api_module, api_method):
        # Call the specified API method dynamically
        api_function = getattr(api_module, api_method)
        # Forward the request and return the response
        return api_function(request)
    else:
        return JsonResponse({"error": "Unsupported API type or method"}, status=400)


######################## AUTHENTICATION API ########################
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """Authentication Django Rest API"""
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        social_api_instance = get_object_or_404(SocialAPI, user=user)

        # TODO: update the code to handle when the user has several emails
        email = social_api_instance.email

        return Response({"access_token": access_token, "email": email}, status=200)

    return Response(status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_token(request):
    """Refreshes the JWT access token"""
    raw_token = request.data.get("access_token")
    if not raw_token:
        return Response({"error": "Access token is missing"}, status=400)

    try:
        # Decode the token without checking for expiration
        decoded_data = jwt.decode(
            raw_token,
            api_settings.SIGNING_KEY,
            algorithms=[api_settings.ALGORITHM],
            options={"verify_exp": False},
        )
        user = User.objects.get(id=decoded_data["user_id"])

        # Issue a new access token
        new_access_token = str(RefreshToken.for_user(user).access_token)

        return Response({"access_token": new_access_token})

    except Exception as e:
        LOGGER.error(f"Error in refresh_token: {str(e)}")
        return Response({"error": str(e)}, status=400)


######################## CATEGORIES ########################
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_categories(request):
    username = request.user.username

    try:
        current_user = User.objects.get(username=username)
        categories = Category.objects.filter(user=current_user)
        serializer = CategoryNameSerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=400)

    except Exception as e:
        LOGGER.error(f"Error in get_user_categories: {str(e)}")
        return Response({"error": str(e)}, status=500)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_category(request, currentName):
    try:
        category = Category.objects.get(name=currentName, user=request.user)
    except Category.DoesNotExist:
        return Response(
            {"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = CategoryNameSerializer(category, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        LOGGER.error(f"Serializer errors in update_category: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_category(request, currentName):
    try:
        # Retrieve the category to be deleted
        category = Category.objects.get(name=currentName, user=request.user)
    except Category.DoesNotExist:
        return Response(
            {"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND
        )

    category.delete()

    return Response(
        {"detail": "Category deleted successfully"}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def set_category(request):
    data = request.data.copy()
    data["user"] = request.user.id

    # Check if the category already exists for the user
    existing_category = Category.objects.filter(
        user=request.user, name=data["name"]
    ).exists()

    if existing_category:
        return Response(
            {"error": "Category already exists for the user"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = NewCategorySerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        LOGGER.error(f"Serializer errors set_category: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_category_id(request, category_name):
    user = request.user
    category = get_object_or_404(Category, name=category_name, user=user)
    return Response({"id": category.id})


############################# CONTACT ##############################
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_contacts(request):
    try:
        user_contacts = Contact.objects.filter(user=request.user)
    except Contact.DoesNotExist:
        return Response(
            {"error": "No contacts found"}, status=status.HTTP_404_NOT_FOUND
        )

    contacts_serializer = ContactSerializer(user_contacts, many=True)

    return Response(contacts_serializer.data)


def is_no_reply_email(sender_email):
    """Returns True if the email is a no-reply address."""
    no_reply_patterns = ["no-reply", "donotreply", "noreply", "do-not-reply"]

    return any(pattern in sender_email.lower() for pattern in no_reply_patterns)


def save_email_sender(user, sender_name, sender_email):
    """Saves the sender if the mail is relevant"""
    if not is_no_reply_email(sender_email):
        existing_contact = Contact.objects.filter(user=user, email=sender_email).first()

        if not existing_contact:
            try:
                Contact.objects.create(
                    email=sender_email, username=sender_name, user=user
                )
            except IntegrityError:
                # TODO: Handle duplicates gracefully (e.g., update existing records)
                pass


######################## PROMPT ENGINEERING ########################
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def find_user_view_ai(request):
    """Searches for emails in the user's mailbox based on the provided search query in both the subject and body."""
    search_query = request.GET.get("query")

    if search_query:
        main_list, cc_list, bcc_list = mistral.extract_contacts_recipients(search_query)

        if not main_list:
            return Response(
                {"error": "Invalid input or query not about email recipients"},
                status=400,
            )

        try:
            user_contacts = Contact.objects.filter(user=request.user)
        except Contact.DoesNotExist:
            return Response(
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

            LOGGER.info(f"Matching emails for '{', '.join(recipient_list)}':")
            for recipient in recipients_with_emails:
                LOGGER.info(f"{recipient['username']}: {recipient['email']}")

            return recipients_with_emails

        # Find matching emails for each list of recipients
        main_recipients_with_emails = find_emails_for_recipients(
            main_list, contacts_dict
        )
        cc_recipients_with_emails = find_emails_for_recipients(cc_list, contacts_dict)
        bcc_recipients_with_emails = find_emails_for_recipients(bcc_list, contacts_dict)

        return Response(
            {
                "main_recipients": main_recipients_with_emails,
                "cc_recipients": cc_recipients_with_emails,
                "bcc_recipients": bcc_recipients_with_emails,
            },
            status=200,
        )
    else:
        LOGGER.error("Failed to authenticate or no search query provided")
        return Response(
            {"error": "Failed to authenticate or no search query provided"}, status=400
        )


# ----------------------- REDACTION -----------------------#
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def new_email_ai(request):
    serializer = NewEmailAISerializer(data=request.data)

    if serializer.is_valid():
        input_data = serializer.validated_data["input_data"]
        length = serializer.validated_data["length"]
        formality = serializer.validated_data["formality"]

        subject_text, mail_text = mistral.generate_email(input_data, length, formality)

        return Response({"subject": subject_text, "mail": mail_text})
    else:
        LOGGER.error(f"Serializer errors in new_email_ai: {serializer.errors}")
        return Response(serializer.errors, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def new_email_recommendations(request):
    serializer = EmailAIRecommendationsSerializer(data=request.data)

    if serializer.is_valid():
        mail_content = serializer.validated_data["mail_content"]
        user_recommendation = serializer.validated_data["user_recommendation"]
        email_subject = serializer.validated_data["email_subject"]

        LOGGER.info(f"mail_content: {mail_content}")
        LOGGER.info(f"user_recommendation: {user_recommendation}")
        LOGGER.info(f"email_subject: {email_subject}")

        subject_text, email_body = mistral.new_mail_recommendation(
            mail_content, email_subject, user_recommendation
        )

        return Response({"subject": subject_text, "email_body": email_body})
    else:
        LOGGER.error(
            f"Serializer errors in new_email_recommendations: {serializer.errors}"
        )
        return Response(serializer.errors, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def improve_email_writing(request):
    """Enhance the subject and body of an email in both quantity and quality in French, while preserving key details from the original version."""

    serializer = EmailCorrectionSerializer(data=request.data)
    if serializer.is_valid():
        email_body = serializer.validated_data["email_body"]
        email_subject = serializer.validated_data["email_subject"]

        email_body, subject_text = mistral.improve_email_writing(
            email_body, email_subject
        )

        return Response({"subject": subject_text, "email_body": email_body})
    else:
        LOGGER.error(f"Serializer errors in improve_email_writing: {serializer.errors}")
        return Response(serializer.errors, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def correct_email_language(request):
    """Corrects spelling and grammar mistakes in the email subject and body based on user's request."""

    serializer = EmailCorrectionSerializer(data=request.data)
    if serializer.is_valid():
        email_subject = serializer.validated_data["email_subject"]
        email_body = serializer.validated_data["email_body"]

        corrected_subject, corrected_body, num_corrections = (
            mistral.correct_mail_language_mistakes(email_body, email_subject)
        )

        return Response(
            {
                "corrected_subject": corrected_subject,
                "corrected_body": corrected_body,
                "num_corrections": num_corrections,
            }
        )
    else:
        LOGGER.error(
            f"Serializer errors in correct_email_language: {serializer.errors}"
        )
        return Response(serializer.errors, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def check_email_copywriting(request):
    serializer = EmailCopyWritingSerializer(data=request.data)

    if serializer.is_valid():
        email_subject = serializer.validated_data["email_subject"]
        email_body = serializer.validated_data["email_body"]

        feedback_copywriting = claude.improve_email_copywriting(
            email_body, email_subject
        )

        return Response({"feedback_copywriting": feedback_copywriting})
    else:
        LOGGER.error(
            f"Serializer errors in check_email_copywriting: {serializer.errors}"
        )
        return Response(serializer.errors, status=400)


# ----------------------- ANSWER -----------------------#
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_email_response_keywords(request):
    serializer = EmailProposalAnswerSerializer(data=request.data)

    if serializer.is_valid():
        email_subject = serializer.validated_data["email_subject"]
        email_content = serializer.validated_data["email_content"]

        # TODO: Add language parameter
        response_keywords = mistral.generate_response_keywords(
            email_subject, email_content, "French"
        )
        return Response({"response_keywords": response_keywords})
    else:
        LOGGER.error(
            f"Serializer errors in generate_email_response_keywords: {serializer.errors}"
        )
        return Response(serializer.errors, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_email_answer(request):
    serializer = EmailGenerateAnswer(data=request.data)

    if serializer.is_valid():
        email_subject = serializer.validated_data["email_subject"]
        email_content = serializer.validated_data["email_content"]
        response_type = serializer.validated_data["response_type"]
        email_answer = mistral.generate_email_response(
            email_subject, email_content, response_type, "French"
        )

        return Response({"email_answer": email_answer})
    else:
        LOGGER.error(f"Serializer errors in generate_email_answer: {serializer.errors}")
        return Response(serializer.errors, status=400)


# ----------------------- REPLY LATER -----------------------#
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_answer_later_emails(request):
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
        LOGGER.error(f"Error fetching emails: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


######################## DATABASE OPERATIONS ########################
# ----------------------- BACKGROUND COLOR-----------------------#
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_bg_color(request):
    try:
        preferences = Preference.objects.get(user=request.user)
        serializer = PreferencesSerializer(preferences)
        return Response(serializer.data)

    except Preference.DoesNotExist:
        return Response({"error": "Preferences not found for the user."}, status=404)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def set_user_bg_color(request):
    try:
        preferences = Preference.objects.get(user=request.user)
    except Preference.DoesNotExist:
        preferences = Preference(user=request.user)

    serializer = PreferencesSerializer(preferences, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    else:
        LOGGER.error(f"Serializer errors in set_user_bg_color: {serializer.errors}")
        return Response(serializer.errors, status=400)


# ----------------------- CREDENTIALS UPDATE-----------------------#
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_username(request):
    user = request.user
    new_username = request.data.get("username")

    if not new_username:
        return Response({"error": "No new username provided."}, status=400)

    # Check if user requirements
    if User.objects.filter(username=new_username).exists():
        return Response({"error": "Username already exists"}, status=400)
    elif " " in new_username:
        return Response({"error": "Username must not contain spaces"}, status=400)

    user.username = new_username
    user.save()

    return Response({"success": "Username updated successfully."})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_password(request):
    user = request.user
    new_password = request.data.get("password")

    if not new_password:
        return Response({"error": "No new password provided."}, status=400)

    # Checks passwords requirements
    if not (8 <= len(new_password) <= 32):
        return Response(
            {"error": "Password length must be between 8 and 32 characters"}, status=400
        )
    if " " in new_password:
        return Response({"error": "Password must not contain spaces"}, status=400)
    elif not re.match(r"^[a-zA-Z0-9!@#$%^&*()-=_+]+$", new_password):
        return Response({"error": "Password contains invalid characters"}, status=400)

    user.set_password(new_password)
    user.save()

    return Response({"success": "Password updated successfully."})


# ----------------------- ACCOUNT-----------------------#
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_account(request):
    """Removes the user from the database"""
    user = request.user

    try:
        user.delete()
        return Response({"message": "User successfully deleted"}, status=200)

    except Exception as e:
        LOGGER.error(f"Error when deleting account {user.id}: {str(e)}")
        return Response({"error": str(e)}, status=500)


# ----------------------- RULES -----------------------#
@api_view(["POST"])
@permission_classes([IsAuthenticated])
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
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
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

        return Response(rules_data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_rule_by_id(request, id_rule):
    try:
        # Retrieve the rule with the given id that belongs to the user
        user_rule = Rule.objects.get(id=id_rule, user=request.user)

    except Rule.DoesNotExist:
        return Response({"error": "Rule not found"}, status=status.HTTP_404_NOT_FOUND)

    rule_serializer = RuleSerializer(user_rule)
    rule_data = rule_serializer.data

    # Manually add category name and sender details if they exist
    category_name = user_rule.category.name if user_rule.category else None
    sender_name = user_rule.sender.name if user_rule.sender else None
    sender_email = user_rule.sender.email if user_rule.sender else None

    rule_data["category_name"] = category_name
    rule_data["sender_name"] = sender_name
    rule_data["sender_email"] = sender_email

    return Response(rule_data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user_rule_by_id(request, id_rule):
    try:
        # Retrieve the rule with the given id that belongs to the user
        user_rule = Rule.objects.get(id=id_rule, user=request.user)

    except Rule.DoesNotExist:
        return Response({"error": "Rule not found"}, status=404)

    user_rule.delete()

    return Response({"message": "Rule deleted successfully"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_user_rule(request):
    serializer = RuleSerializer(data=request.data, context={"user": request.user})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    else:
        LOGGER.error(f"Serializer errors in create_user_rule: {serializer.errors}")
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user_rule(request):
    try:
        rule = Rule.objects.get(id=request.data.get("id"), user=request.user)
    except Rule.DoesNotExist:
        return Response({"error": "Rule not found."}, status=404)

    serializer = RuleSerializer(
        rule, data=request.data, partial=True, context={"user": request.user}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    else:
        LOGGER.error(f"Serializer errors in update_user_rule: {serializer.errors}")
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


# ----------------------- USER -----------------------#
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def check_sender_for_user(request):
    user_email = request.data.get("email")

    try:
        # Check if a sender with the given email exists for the authenticated user
        sender = Sender.objects.get(email=user_email, user=request.user)
        return Response(
            {"exists": True, "sender_id": sender.id}, status=status.HTTP_200_OK
        )

    except ObjectDoesNotExist:
        return Response({"exists": False}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_details(request):
    """Returns the username"""
    return Response({"username": request.user.username})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_sender(request):
    """Create a new sender associated with the authenticated user"""
    serializer = SenderSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        LOGGER.error(f"Serializer errors in create_sender: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_email(request, email_id):
    try:
        user = request.user

        # Check if the email belongs to the authenticated user
        email = get_object_or_404(Email, user=user, id=email_id)
        email.delete()

        return Response(
            {"message": "Email deleted successfully"}, status=status.HTTP_200_OK
        )

        # result = forward_request(request, "delete_email")
        #
        # if result.get("message", "") == "Email moved to trash successfully!":
        #     return Response(
        #         {"message": "Email deleted successfully"}, status=status.HTTP_200_OK
        #     )
        # else:
        #     return Response(
        #         {"error": result.get("error")}, status=status.HTTP_400_BAD_REQUEST
        #     )

    except Exception as e:
        LOGGER.error(f"Error when deleting email: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ----------------------- CREDENTIALS AVAILABILITY -----------------------#
@api_view(["GET"])
@permission_classes([AllowAny])
def check_username(request):
    """Verify if the username is available"""
    username = request.headers.get("username")

    if User.objects.filter(username=username).exists():
        return Response({"available": False}, status=200)
    else:
        return Response({"available": True}, status=200)


# ----------------------- EMAIL -----------------------#
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_first_email(request):
    """Returns the first email associated with the user in mailassistantdb"""
    user = request.user
    social_api_instance = get_object_or_404(SocialAPI, user=user)

    # TODO: update the code to handle when the user has several emails
    email = social_api_instance.email

    if email:
        return Response({"email": email}, status=200)
    else:
        return Response({"error": "No emails associated with the user"}, status=404)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def set_email_read(request, email_id):
    """Mark a specific email as read for the authenticated user"""
    user = request.user

    # Check if the email belongs to the authenticated user
    email = get_object_or_404(Email, user=user, id=email_id)

    # Update the read field
    email.read = True
    email.save()

    serializer = EmailReadUpdateSerializer(email)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def set_email_reply_later(request, email_id):
    """Mark a specific email for later reply for the authenticated user"""
    user = request.user

    email = get_object_or_404(Email, user=user, id=email_id)
    email.answer_later = True
    email.save()

    serializer = EmailReplyLaterUpdateSerializer(email)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_emails(request):
    """Retrieves and formats user emails grouped by category and priority"""
    user = request.user
    emails = Email.objects.filter(user=user).prefetch_related(
        "category", "bulletpoint_set"
    )

    emails = emails.annotate(
        has_rule=Exists(Rule.objects.filter(sender=OuterRef("sender"), user=user))
    )
    rule_id_subquery = Rule.objects.filter(sender=OuterRef("sender"), user=user).values(
        "id"
    )[:1]
    emails = emails.annotate(rule_id=Subquery(rule_id_subquery))

    # Set of all possible priorities
    all_priorities = {"Important", "Information", "Useless"}
    formatted_data = defaultdict(lambda: defaultdict(list))

    for email in emails:
        email_data = {
            "id": email.id,
            "id_provider": email.provider_id,
            "email": email.sender.email,
            "name": email.sender.name,
            "description": email.email_short_summary,
            "details": [
                {"id": bp.id, "text": bp.content} for bp in email.bulletpoint_set.all()
            ],
            "read": email.read,
            "rule": email.has_rule,
            "rule_id": email.rule_id,
        }
        formatted_data[email.category.name][email.priority].append(email_data)

    # Ensuring all priorities are present for each category
    for category in formatted_data:
        for priority in all_priorities:
            formatted_data[category].setdefault(priority, [])

    return Response(formatted_data, status=status.HTTP_200_OK)


######################## TESTING FUNCTIONS ########################
# TO TEST AUTH API
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def authenticate_service_view(request):
    user = request.user
    email = request.headers.get("email")
    service = google_api.authenticate_service(user, email)

    if service is not None:
        # Return a success response, along with any necessary information
        return Response({"message": "Authentication successful"}, status=200)
    else:
        # Return an error response
        return Response({"error": "Failed to authenticate"}, status=400)


# TO TEST Gmail Save in BDD Last Email
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def save_last_mail_view(request):
    user = request.user
    email = request.headers.get("email")
    service = google_api.authenticate_service(user, email)

    if service is not None:
        google_api.processed_email_to_bdd(request, service)
        return Response({"message": "Save successful"}, status=200)
    else:
        return Response({"error": "Failed to authenticate"}, status=400)


# [OUTLOOK] TO TEST Gmail Save in BDD Last Email
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def save_last_mail_outlook(request):
    user = request.user
    email = request.headers.get("email")

    try:
        microsoft_api.processed_email_to_bdd(user, email)
        return Response({"message": "Save successful"}, status=200)
    except:
        return Response({"error": "Failed to authenticate"}, status=400)


# TO TEST Gmail GET the Mail from id
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_mail_view(request):
    user = request.user
    email = request.headers.get("email")
    service = google_api.authenticate_service(user, email)

    if service is not None:
        subject, from_name, decoded_data, email_id, date = google_api.get_mail(
            service, 0, None
        )
        # Return a success response, along with any necessary information
        return Response(
            {
                "message": "Authentication successful",
                "email": {
                    "subject": subject,
                    "from_name": from_name,
                    "decoded_data": decoded_data,
                    "email_id": email_id,
                    "date": date,
                },
            },
            status=200,
        )
    else:
        # Return an error response
        return Response({"error": "Failed to authenticate"}, status=400)


# TO TEST Gmail GET Last Email
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_mail_by_id_view(request):
    user = request.user
    email = request.headers.get("email")
    service = google_api.authenticate_service(user, email)
    mail_id = request.GET.get("email_id")

    if service is not None and mail_id is not None:

        subject, from_name, decoded_data, cc, bcc, email_id, date = google_api.get_mail(
            service, None, mail_id
        )
        # print(
        #     f"{Fore.CYAN}from_name: {from_name}, cc: {Fore.YELLOW}{cc}, bcc: {Fore.LIGHTGREEN_EX}{bcc}"
        # )

        # clean cc
        if cc:
            cc = tuple(item for item in cc if item is not None)

        # clean bcc
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
                },
            },
            status=200,
        )
    else:
        return Response({"error": "Failed to authenticate"}, status=400)


###############################################################################################################
######################## THESE FUNCTIONS WORKS ONLY WITH GMAIL => DEPRECATED & USELESS ########################
###############################################################################################################


"""@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def get_user_emails(request):
    user = request.user
    emails = Email.objects.filter(id_user=user)
    serializer = UserEmailSerializer(emails, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def get_email_bullet_points(request, email_id):
    user = request.user

    # Check if the email belongs to the authenticated user
    email = get_object_or_404(Email, id_user=user, id=email_id)

    bullet_points = BulletPoint.objects.filter(id_email=email)
    serializer = BulletPointSerializer(bullet_points, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)   
    
def logout_user(request):
    # \"\"\"Handle user logout.\"\"\"
    logout(request)
    return redirect('MailAssistant:login')
"""


######################## Answers to Mails ########################

"""# gets a template to answer in that form
def get_answer_template(mail_size):
    # samples to get work done as intended
    if mail_size<50:
        path = 'chemin_fichier_txt_small.txt'
    elif mail_size<100:
        path = 'chemin_fichier_txt_medium.txt'
    else:
        path = 'chemin_fichier_txt_large.txt'
    # getting data from file
    with open(path,'r',encoding='utf-8') as file:
        template = file
    return template

# gets the size (in words) of text
def get_size(text):
    text_size = len(text.split())
    return text_size
"""


######################## Search bar ########################

"""# decode using 'utf-8'
def decode_email_data(data):
    byte_code = base64.urlsafe_b64decode(data)
    return byte_code.decode("utf-8")"""

"""# goes through parts
def parse_parts(parts, from_name):
    for part in parts:
        # Check for nested parts
        if 'parts' in part:
            parse_parts(part['parts'], from_name)
        # Check for data in part
        data = part.get('data')
        if data:
            text = decode_email_data(data)
            print(f"From: {from_name}\nMessage: {text}\n")"""

"""# Function to extract value after colon for a given field
def extract_value(field,clear_text):
    # start = clear_text.index(field) + len(field)
    # end = clear_text[start:].index("\n") if "\n" in clear_text[start:] else len(clear_text)
    start = clear_text.find(field)
    if start == -1:  # if field is not found in clear_text
        return ""  # or return any default value you want
    
    start += len(field)
    end = clear_text[start:].find("\n")
    if end == -1:
        end = len(clear_text)
    final_text = re.sub(r"\[Model's drafted .+?\]", '', clear_text[start:start+end].strip())
    final_text = re.sub(r"\[Unknown\]", '', final_text.strip())
    final_text = re.sub(r"\[blank\]", '', final_text.strip())
    final_text = re.sub(r"Unknown", '', final_text.strip())
    final_text = re.sub(r"blank", '', final_text.strip())
    return final_text.strip()"""

"""# Function to extract value after colon for a given field
def extract_value_2(field,clear_text):
    # start = clear_text.index(field) + len(field)
    # end = clear_text[start:].index("\n") if "\n" in clear_text[start:] else len(clear_text)
    start = clear_text.find(field)
    if start == -1:  # if field is not found in clear_text
        return ""  # or return any default value you want
    
    start += len(field)
    end = clear_text[start:].find("\n")
    if end == -1:
        end = len(clear_text)
    final_text = re.sub(r"\[Model's drafted .+?\]", '', clear_text[start:start+end].strip())
    final_text = re.sub(r"\[Unknown\]", '', final_text.strip())
    final_text = re.sub(r"\[Blank\]", '', final_text.strip())
    final_text = re.sub(r"Unknown", '', final_text.strip())
    final_text = re.sub(r"Blank", '', final_text.strip())
    return final_text.strip()"""

'''# decompose text from user to key words for API (Google)
def gpt_langchain_decompose_search(chat_data):
    # Ensure chat_data is a list of chat messages
    if not isinstance(chat_data, list):
        raise ValueError("chat_data must be a list of chat messages")

    today = datetime.date.today()
    chat_string = '\n'.join(chat_data)  # Convert chat messages to a string

    # template = (
    # """Given the following chat:
    # {chat}

    # And current date:
    # {date}
    
    # From the chat:
    # 1. Identify the sender of the mail being referred to.
    # 2. Identify the recipient of the mail.
    # 3. Extract key details or keywords mentioned about the mail. These keywords should strictly relate to the content or subject of the mail and should not include names of the sender, recipient, or any date-related terms.
    # 4. Determine the starting date of the mail search range if mentioned. If not, leave it blank.
    # 5. Determine the ending date of the mail search range if mentioned. If not, leave it blank.

    # ---

    # From:
    # [Model's drafted sender]

    # To:
    # [Model's drafted recipient]

    # Key words (excluding sender, recipient, and date-related terms):
    # [Model's drafted key details]

    # Starting date:
    # [Model's drafted starting date in yyyy-mm-dd format]

    # Ending date:
    # [Model's drafted ending date in yyyy-mm-dd format]
    # """
    # )
    template = (
    """Given the following chat:
    {chat}

    Note: The current date is {date}. If no specific date is mentioned in the chat, leave the date fields blank.
    
    Using the details from the chat, provide the following information in the format described below:
    
    1. Sender of the mail being referred to.
    2. Recipient of the mail.
    3. Key details or keywords mentioned about the mail. These keywords should strictly relate to the content or subject of the mail and should not include names of the sender, recipient, or any date-related terms.
    4. The starting date of the mail search range if mentioned (leave blank if not specified).
    5. The ending date of the mail search range if mentioned (leave blank if not specified).

    ---

    From:
    [Model's drafted sender]

    To:
    [Model's drafted recipient]

    Key words (excluding sender, recipient, and date-related terms):
    [Model's drafted key details]

    Starting date (if not mentioned, leave this blank):
    [Model's drafted starting date in yyyy-mm-dd format]

    Ending date (if not mentioned, leave this blank):
    [Model's drafted ending date in yyyy-mm-dd format]
    """
    )


    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])
    chat_completion = ChatOpenAI(temperature=0, openai_api_key=openai.api_key, openai_organization=openai.organization)
    text = chat_completion(chat_prompt.format_prompt(chat=chat_string, date=today).to_messages())

    clear_text = text.content.strip()
    print("clear_text: ",clear_text)
    
    try:
        from_text = extract_value("From:\n",clear_text)
        to_text = extract_value("To:\n",clear_text)
        key_words_text = extract_value("Key words (excluding sender, recipient, and date-related terms):\n",clear_text)
        starting_date_text = extract_value("Starting date (if not mentioned, leave this blank):\n",clear_text)
        ending_date_text = extract_value("Ending date (if not mentioned, leave this blank):\n",clear_text)
    except:
        from_text = extract_value_2("From: ",clear_text)
        to_text = extract_value_2("To: ",clear_text)
        key_words_text = extract_value_2("Key words (excluding sender, recipient, and date-related terms): ",clear_text)
        starting_date_text = extract_value_2("Starting date (if not mentioned, leave this blank): ",clear_text)
        ending_date_text = extract_value_2("Ending date (if not mentioned, leave this blank): ",clear_text)

    from_email,to_email = api_list[api_var].get_email_address(from_text,to_text)
    
    return from_email, to_email, starting_date_text, ending_date_text, key_words_text'''

"""# Questions asked for more details
def search_chat_reply(query_list):
    if query_list[0]==0: # from who
        assistant_question = "0"
    elif query_list[1]==0: # to who
        assistant_question = "1"
    elif query_list[2]==0: # start date
        assistant_question = "2"
    elif query_list[3]==0: # end date
        assistant_question = "3"
    elif query_list[4]==0: # key words
        assistant_question = "4"
    return assistant_question"""


"""# separate multiple mails (from a single mail) to different parts
def separate_concatenated_mails(decoded_text):
    # Using the given separator to split the mails
    separator = "________________________________"
    mails = decoded_text.split(separator)
    
    # Removing any empty strings from the list
    mails = [mail.strip() for mail in mails if mail.strip()]
    
    return mails"""

"""def raw_to_string(raw_data):
    # Decode the base64-encoded raw email
    decoded_bytes = base64.urlsafe_b64decode(raw_data.encode('ASCII'))
    # Convert the decoded bytes to a string using utf-8 encoding
    return decoded_bytes.decode('utf-8')"""

"""def extract_body_from_email(services,int_mail,id_mail):
    service = services['gmail.readonly']

    if int_mail!=None:
        # Call the Gmail API to fetch INBOX
        results = service.users().messages().list(userId='me',labelIds=['INBOX']).execute()
        messages = results.get('messages', [])
        if not messages:
            print('No new messages.')
            return
        else:
            message = messages[int_mail]
            msg_raw = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()
    # 2 lines added to make it work for id as well
    elif id_mail!=None:
        msg_raw = service.users().messages().get(userId='me', id=id_mail, format='raw').execute()


    # Convert the raw data to a string
    email_str = raw_to_string(msg_raw)
    
    # Parse the email string
    msg = message_from_string(email_str)
    
    # Function to extract text/plain or text/html content from a given part
    def extract_content(part, content_type):
        if part.get_content_type() == content_type:
            return part.get_payload(decode=True).decode('utf-8')
        return None

    # Extract the body based on the email type
    if msg.is_multipart():
        # Handle multipart emails
        plain_text = None
        html_text = None
        
        for part in msg.walk():
            content_disposition = str(part.get('Content-Disposition'))
            
            # Skip any part that is an attachment
            if "attachment" in content_disposition:
                continue
            
            # Look for text/plain parts first
            if not plain_text:
                plain_text = extract_content(part, "text/plain")
            
            # If not found, then look for text/html parts
            if not html_text:
                html_text = extract_content(part, "text/html")
        
        # Return text/plain content if found, otherwise return text/html content
        return plain_text or html_text or ""  # Return an empty string if no body content was found
    else:
        # Handle single-part emails
        return msg.get_payload(decode=True).decode('utf-8')

# Usage example:
# raw_email_data = msg['raw']  # Assuming you've fetched the raw email using the Gmail API
# email_body = extract_body_from_email(raw_email_data)"""


######################## Read Mails ########################

"""# get categories from database (no data base set)
def get_db_categories():
    # access database
    category_list = {
    'Esaip':"Ecole d'ingénieur",
    'Entreprenariat':"Tout ce qui est en lien avec l'entreprenariat",
    'Subscriptions': 'Pertaining to periodic payment plans for services or products.',
    'Miscellaneous': 'Items, topics, or subjects that do not fall under any other specific category or for which a dedicated category has not been established.'
    }
    return category_list"""


# TO UPDATE
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_login(request):
    try:
        user = Users.objects.get(id_user=request.user.id)
        serializer = UserLoginSerializer(user)
        return Response(serializer.data)
    except Users.DoesNotExist:
        return Response({"error": "User not found."}, status=404)"""

"""
# TODO: Change later with the list of email of the user saved in a BD for optimization
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def find_user_view(request):
    user = request.user
    email = request.headers.get('email')
    search_query = request.GET.get('query')
    social_api = get_object_or_404(SocialAPI, user=user, email=email)    
    type_api = social_api.type_api

    if search_query:
        if type_api == 'google':
            services = google_api.authenticate_service(user, email)
            found_users = google_api.find_user_in_emails(services, search_query)
        elif type_api == 'microsoft':
            access_token = microsoft_api.refresh_access_token(microsoft_api.get_social_api(user, email))
            found_users = google_api.find_user_in_emails(access_token, search_query)

        return Response(found_users, safe=False, status=200)
    else:
        return Response({"error": "Failed to authenticate or no search query provided"}, status=400)"""


'''@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_parsed_contacts(request):
    """Returns a list of parsed unique contacts"""
    return forward_request(request._request, 'get_parsed_contacts')'''


'''@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unique_email_senders_view(request):
    """Fetches unique email senders' information, combining data from user's contacts and email senders."""
    return forward_request(request._request, 'get_unique_email_senders')'''

'''# THEO API TEST
@api_view(['GET'])
@permission_classes([AllowAny])
def get_message(request):
    """Retrieve and return the data of the first message"""
    # Just getting the first message for simplicity.
    message = Message.objects.first() 
    serializer = MessageSerializer(message)
    return Response(serializer.data)'''


"""@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def get_email_bullet_points(request, email_id):
    user = request.user

    # Check if the email belongs to the authenticated user
    email = get_object_or_404(Email, id_user=user, id=email_id)

    bullet_points = BulletPoint.objects.filter(id_email=email)
    serializer = BulletPointSerializer(bullet_points, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)"""


'''
importance_list = {
    "Important": 'Items or messages that are of high priority, do not contain offers to "unsubscribe", and require immediate attention or action.',
    "Information": 'Details that are relevant and informative but may not require immediate action. Does not contain offers to "unsubscribe".',
    "Useless": 'Items or messages that contain offers to "unsubscribe", might not be relevant to all recipients, are redundant, or do not provide any significant value.',
}
user_description = "Enseignant chercheur au sein d'une école d'ingénieur ESAIP."

response_list = {
    "Answer Required": "Message requires an answer.",
    "Might Require Answer": "Message might require an answer.",
    "No Answer Required": "No answer is required.",
}
relevance_list = {
    "Highly Relevant": "Message is highly relevant to the recipient.",
    "Possibly Relevant": "Message might be relevant to the recipient.",
    "Not Relevant": "Message is not relevant to the recipient.",
}


def processed_email_to_bdd(request, services):
    subject, from_name, decoded_data, cc, bcc, email_id = google_api.get_mail(
        services, 0, None
    )  # microsoft non fonctionnel

    if not Email.objects.filter(provider_id=email_id).exists():

        # Check if data is decoded, then format it
        if decoded_data:
            decoded_data = format_mail(decoded_data)

        # Get user categories
        category_list = get_db_categories(request.user)

        # print("DEBUG -------------> category", category_list)

        # Process the email data with AI/NLP
        topic, importance, answer, summary, sentence, relevance, importance_explain = (
            gpt_langchain_response(subject, decoded_data, category_list)
        )

        # print("TEST -------------->", from_name, "TYPE ------------>", type(from_name))
        # sender_name, sender_email = separate_name_email(from_name) => OLD USELESS
        sender_name, sender_email = from_name[0], from_name[1]

        # Fetch or create the sender
        sender, created = Sender.objects.get_or_create(
            name=sender_name, email=sender_email, user=request.user
        )  # assuming from_name contains the sender's name

        print("DEBUG ----------------> topic", topic)
        # Get the relevant category based on topic or create a new one (for simplicity, I'm getting an existing category)
        category = Category.objects.get_or_create(name=topic, user=request.user)[0]

        provider = "Gmail"

        try:
            # Create a new email record
            email_entry = Email.objects.create(
                provider_id=email_id,
                email_provider=provider,
                email_short_summary=sentence,
                content=decoded_data,
                subject=subject,
                priority=importance[0],
                read=False,  # Default value; adjust as necessary
                answer_later=False,  # Default value; adjust as necessary
                sender=sender,
                category=category,
                user=request.user,
            )

            # If the email has a summary, save it in the BulletPoint table
            if summary:
                # Split summary by line breaks
                lines = summary.split("\n")

                # Filter lines that start with '- ' which indicates a bullet point
                bullet_points = [
                    line[2:].strip() for line in lines if line.strip().startswith("- ")
                ]

                for point in bullet_points:
                    BulletPoint.objects.create(content=point, email=email_entry)
        except IntegrityError:
            print(
                f"An error occurred when trying to create an email with provider_id {email_id}. It might already exist."
            )

        # Debug prints
        print("topic:", topic)
        print("importance:", importance)
        print("answer:", answer)
        print("summary:", summary)
        print("sentence:", sentence)
        print("relevance:", relevance)
        print("importance_explain:", importance_explain)

    else:
        print(f"Email with provider_id {email_id} already exists.")

    # return email_entry  # Return the created email object, if needed
    return


# strips text of unnecessary spacings
def format_mail(text):
    # Delete links
    text = re.sub(r"<http[^>]+>", "", text)
    # Delete patterns like "[image: ...]"
    text = re.sub(r"\[image:[^\]]+\]", "", text)
    # Convert Windows line endings to Unix line endings
    text = text.replace("\r\n", "\n")
    # Remove spaces at the start and end of each line
    text = "\n".join(line.strip() for line in text.split("\n"))
    # Delete multiple spaces
    text = re.sub(r" +", " ", text)
    # Reduce multiple consecutive newlines to two newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text


def fill_lists(categories, percentages):
    base_categories = ["Important", "Information", "Useless"]

    # Determine which category is in the list
    first_category = categories[0]

    # Remove the category found from the base list
    base_categories.remove(first_category)

    # Construct the new categories list based on the first category
    for i in range(1, 3):
        if not categories[i]:
            categories[i] = base_categories.pop(0)
            percentages[i] = "0%"

    return categories, percentages


def get_db_categories(current_user):
    # Query categories specific to the current user from the database.
    categories = Category.objects.filter(user=current_user)

    # Construct the category_list dictionary from the queried data.
    category_list = {category.name: category.description for category in categories}

    return category_list


def separate_name_email(s):
    """
    Separate "Name <email>" or "<email>" into name and email.

    Args:
    - s (str): Input string of format "Name <email>" or "<email>"

    Returns:
    - (str, str): (name, email). If name is not present, it returns (None, email)
    """

    # Regex pattern to capture Name and Email separately
    match = re.match(r"(?:(.*)\s)?<(.+@.+)>", s)
    if match:
        name, email = match.groups()
        return name.strip() if name else None, email
    else:
        return None, None


# TODO: Put in gpt_3_5_turbo.py AFTER testing
# REMOVE hardcoded variables


# Summarize and categorize an email
def gpt_langchain_response(subject, decoded_data, category_list):
    template = """Given the following email:

    Subject:
    {subject}

    Text:
    {text}

    And user description:

    Description:
    {user}

    Using the provided categories:

    Topic Categories:
    {category}

    Importance Categories:
    {importance}

    Response Categories:
    {answer}

    Relevance Categories:
    {relevance}

    1. Please categorize the email by topic, importance, response, and relevance corresponding to the user description.
    2. In French: Summarize the following message
    3. In French: Provide a short sentence summarizing the email.

    ---

    Topic Categorization: [Model's Response for Topic Category]

    Importance Categorization (Taking User Description into account and only using Importance Categories):
    - Category 1: [Model's Response for Importance Category 1]
    - Percentage 1: [Model's Percentage for Importance Category 1]
    - Category 2: [Model's Response for Importance Category 2]
    - Percentage 2: [Model's Percentage for Importance Category 2]
    - Category 3: [Model's Response for Importance Category 3]
    - Percentage 3: [Model's Percentage for Importance Category 3]

    Response Categorization: [Model's Response for Response Category]

    Relevance Categorization: [Model's Response for Relevance Category]

    Résumé court en français: [Model's One-Sentence Summary en français without using response/relevance categorization]

    Résumé en français (without using importance, response or relevance categorization):
    - [Model's Bullet Point 1 en français]
    - [Model's Bullet Point 2 en français]
    ...
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])
    # get a chat completion from the formatted messages
    chat = ChatOpenAI(
        temperature=0,
        openai_api_key="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",
        openai_organization="org-YSlFvq9rM1qPzM15jewopUUt",
    )
    # This line does not work (Augustin)
    response = chat(
        chat_prompt.format_prompt(
            user=user_description,
            category=category_list,
            importance=importance_list,
            answer=response_list,
            subject=subject,
            text=decoded_data,
            relevance=relevance_list,
        ).to_messages()
    )

    clear_response = response.content.strip()
    print("full response: ", clear_response)

    # Extracting Topic Categorization
    topic_category = clear_response.split("Topic Categorization: ")[1].split("\n")[0]

    # Extracting Importance/Action Categorization
    importance_categories = []
    importance_percentages = []
    for i in range(1, 4):
        cat_str = f"Category {i}: "
        perc_str = f"Percentage {i}: "
        importance_categories.append(clear_response.split(cat_str)[1].split("\n")[0])
        importance_percentages.append(clear_response.split(perc_str)[1].split("\n")[0])

    importance_categories, importance_percentages = fill_lists(
        importance_categories, importance_percentages
    )

    # Extracting Response Categorization
    response_category = clear_response.split("Response Categorization: ")[1].split(
        "\n"
    )[0]

    # Extracting Relevance Categorization
    relevance_category = clear_response.split("Relevance Categorization: ")[1].split(
        "\n"
    )[0]

    # Extracting one sentence summary
    short_sentence = clear_response.split("Résumé court en français: ")[1].split("\n")[
        0
    ]

    # # Extracting Summary
    # summary_start = clear_response.index("Résumé en français:") + len("Résumé en français:")
    # summary_end = clear_response[summary_start:].index("\n\n") if "\n\n" in clear_response[summary_start:] else len(clear_response)
    # summary_list = clear_response[summary_start:summary_start+summary_end].strip().split("\n- ")[1:]
    # summary_text = "\n".join(summary_list)

    # Finding start of the summary
    match = re.search(
        r"Résumé en français(\s\(without using importance, response or relevance categorization\))?:",
        clear_response,
    )

    if match:
        # Adjusting the start index based on the match found
        summary_start = match.end()
    else:
        # Fallback or default behavior if the pattern is not found
        summary_start = -1  # Or handle this case as needed

    # Finding the end of the summary
    summary_end = clear_response.find("\n\n", summary_start)
    if (
        summary_end == -1
    ):  # If there's no double newline after the start, consider till the end of the string
        summary_end = len(clear_response)

    # Extracting the summary if a valid start index was found
    if summary_start != -1:
        summary_text = clear_response[summary_start:summary_end].strip()
    else:
        summary_text = "Summary not found."

    """ OLD TO DELETE (only Theo can delete)
    summary_start = clear_response.find("Résumé en français:") + len("Résumé en français:")

    # Finding the end of the summary
    summary_end = clear_response.find("\n\n", summary_start)
    if summary_end == -1:  # If there's no double newline after the start, consider till the end of the string
        summary_end = len(clear_response)

    # Extracting the summary
    summary_text = clear_response[summary_start:summary_end].strip()
    # if summary_text.startswith("- "):  # Remove any leading "- " from the extracted text
    #     summary_text = summary_text[2:].strip()"""

    # Output results
    # print("Topic Category:", topic_category)
    # print("Importance Categories:", importance_categories)
    # print("Importance Percentages:", importance_percentages)
    # print("Response Category:", response_category)
    # print("Relevance Category:", relevance_category)
    # print("Short Sentence:", short_sentence)
    # print("Summary Text:", summary_text)

    return (
        topic_category,
        importance_categories,
        response_category,
        summary_text,
        short_sentence,
        relevance_category,
        importance_percentages,
    )
'''
