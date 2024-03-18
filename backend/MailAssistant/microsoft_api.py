"""
Handles authentication and HTTP requests for the Microsoft Graph API.
"""

import base64
import datetime
import logging
import time
import httpx
import requests
from collections import defaultdict
from django.db import IntegrityError
from urllib.parse import urlencode
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import redirect
from msal import ConfidentialClientApplication
from MailAssistant.constants import (
    GRAPH_URL,
    MICROSOFT_AUTHORITY,
    MICROSOFT_CONFIG,
    MICROSOFT_SCOPES,
    REDIRECT_URI,
)
from .serializers import EmailDataSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Contact, SocialAPI
from requests.exceptions import HTTPError
from .models import SocialAPI, Contact, BulletPoint, Category, Email, Sender
from MailAssistant.ai_providers import gpt_3_5_turbo
from . import library


######################## LOGGING CONFIGURATION ########################
# TODO: add logging conf in constants.py


######################## AUTHENTIFICATION ########################
def generate_auth_url(request):
    """Generate a connection URL to obtain the authorization code"""
    params = {
        "client_id": MICROSOFT_CONFIG["client_id"],
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "response_mode": "query",
        "scope": " ".join(MICROSOFT_SCOPES),
        "state": "0a590ac7-6a23-44b1-9237-287743818d32",
    }
    authorization_url = (
        f"{MICROSOFT_AUTHORITY}/oauth2/v2.0/authorize?{urlencode(params)}"
    )

    return redirect(authorization_url)


def exchange_code_for_tokens(authorization_code):
    """Returns the access token and the refresh token"""
    app = ConfidentialClientApplication(
        client_id=MICROSOFT_CONFIG["client_id"],
        client_credential=MICROSOFT_CONFIG["client_secret"],
        authority=MICROSOFT_AUTHORITY,
    )

    result = app.acquire_token_by_authorization_code(
        authorization_code, scopes=MICROSOFT_SCOPES, redirect_uri=REDIRECT_URI
    )
    if result:
        return result["access_token"], result["refresh_token"]
    else:
        return Response({"error": "tokens not found"}, status=400)


######################## CREDENTIALS ########################
def get_headers(access_token) -> dict:
    """Returns the default access headers"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    return headers


def get_social_api(user, email):
    """Returns the SocialAPI instance"""
    try:
        social_api = SocialAPI.objects.get(user=user, email=email)
        return social_api
    except SocialAPI.DoesNotExist:
        logging.error(
            f"No credentials found for user {user.username} and email {email}"
        )
        return None


def is_token_valid(access_token):
    """Check if the access token is still valid by making a sample request"""
    sample_url = f"{GRAPH_URL}me"
    headers = get_headers(access_token)
    response = requests.get(sample_url, headers=headers)
    return response.status_code == 200


def refresh_access_token(social_api):
    """Returns a valid access token"""
    access_token = social_api.access_token

    if is_token_valid(access_token):
        return access_token

    refresh_url = f"{MICROSOFT_AUTHORITY}/oauth2/v2.0/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": social_api.refresh_token,
        "client_id": MICROSOFT_CONFIG["client_id"],
        "client_secret": MICROSOFT_CONFIG["client_secret"],
        "scope": MICROSOFT_SCOPES,
    }

    response = requests.post(refresh_url, data=data)
    response_data = response.json()

    print(response_data)

    # Check if the refresh was successful
    if "access_token" in response_data:
        social_api.access_token = response_data["access_token"]
        social_api.save()
        return response_data["access_token"]
    else:
        return None


######################## PROFILE REQUESTS ########################
def get_info_contacts(access_token):
    """Fetch the name and the email of the contacts of the user"""
    graph_endpoint = f"{GRAPH_URL}me/contacts"

    try:
        headers = get_headers(access_token)

        params = {"$top": 1000}

        response = requests.get(graph_endpoint, headers=headers, params=params)
        response.raise_for_status()

        contacts = response.json().get("value", [])

        names_emails = []
        for contact in contacts:
            # Extract the name and email address of each contact
            name = contact.get("displayName")
            email_addresses = [
                email["address"] for email in contact.get("emailAddresses", [])
            ]

            names_emails.append({"name": name, "emails": email_addresses})

        return names_emails

    except HTTPError as e:
        logging.error(f"Error in Microsoft Graph API request: {str(e)}")
        return []


def get_unique_senders(access_token) -> dict:
    """Fetches unique sender information from Microsoft Graph API messages"""
    senders_info = {}

    try:
        headers = get_headers(access_token)

        limit = 50
        graph_endpoint = f"{GRAPH_URL}me/messages?$select=sender&$top={limit}"
        response = requests.get(graph_endpoint, headers=headers)

        if response.status_code == 200:
            messages = response.json().get("value", [])
            for message in messages:
                sender = message.get("sender", {})
                email_address = sender.get("emailAddress", {}).get("address", "")
                name = sender.get("emailAddress", {}).get("name", "")
                senders_info[email_address] = name
        else:
            logging.error(f"Failed to fetch messages: {response.text}")

        return senders_info

    except Exception as e:
        logging.exception(f"Error fetching senders: {e}")
        return senders_info


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile_image(request):
    """Returns the profile image URL of the user"""
    user = request.user
    email = request.headers.get("email")
    access_token = refresh_access_token(get_social_api(user, email))

    try:
        headers = get_headers(access_token)

        graph_endpoint = f"{GRAPH_URL}me/photo/$value"
        response = requests.get(graph_endpoint, headers=headers)

        if response.status_code == 200:
            photo_data = response.content

            if photo_data:
                # convert image to url
                photo_data_base64 = base64.b64encode(photo_data).decode("utf-8")
                photo_url = f"data:image/png;base64,{photo_data_base64}"
                return Response({"profile_image_url": photo_url}, status=200)
            else:
                return Response(
                    {"error": "Profile image not found in response"}, status=404
                )
        elif response.status_code == 404:
            return Response({"error": "Profile image not found"}, status=404)
        else:
            logging.error(
                f"Failed to retrieve profile image: {response.status_code}\nReason: {response.reason}"
            )
            return Response(
                {"error": f"Failed to retrieve profile image: {response.reason}"},
                status=404,
            )

    except Exception as e:
        logging.exception(f"An exception occurred: {str(e)}")
        return Response({"error": f"An exception occurred: {str(e)}"}, status=500)


def get_email(access_token):
    """Returns the primary email of the user from Microsoft Graph API"""
    if not access_token:
        return Response({"error": "Access token is missing"}, status=400)

    try:
        graph_api_endpoint = f"{GRAPH_URL}me"
        headers = get_headers(access_token)
        response = requests.get(graph_api_endpoint, headers=headers)

        if response.status_code == 200:
            email_data = response.json()
            email = email_data.get("mail")
            return email
        else:
            return None
    except:
        return None


######################## EMAIL REQUESTS ########################
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def unread_mails(request):
    """Returns the number of unread emails"""
    user = request.user
    email = request.headers.get("email")
    access_token = refresh_access_token(get_social_api(user, email))

    try:
        if access_token:
            headers = get_headers(access_token)
            unread_count = 0

            # Get unread messages using Microsoft Graph API
            graph_endpoint = (
                f"{GRAPH_URL}me/messages"  # ?$count=true&$filter=isRead eq false'
            )
            response = requests.get(graph_endpoint, headers=headers)

            response_json = response.json()

            if response.status_code == 200:
                unread_count = response_json.get("@odata.count", 0)
                return JsonResponse({"unreadCount": unread_count}, status=200)
            else:
                error_message = response_json.get("error", {}).get(
                    "message", "No error message"
                )
                error_code = response_json.get("error", {}).get("code")

                if error_code == "MailboxNotEnabledForRESTAPI":
                    # TODO: display a pop-up
                    print(
                        f"The account you are using does not have a proper license to access the required endpoints"
                    )

                logging.error(f"Failed to retrieve unread count: {error_message}")
                return JsonResponse({"unreadCount": 0}, status=response.status_code)

        return JsonResponse({"unreadCount": 0}, status=400)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return JsonResponse({"unreadCount": 0}, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_email(request):
    """Sends an email using the Microsoft Graph API."""
    user = request.user
    email = request.headers.get("email")
    access_token = refresh_access_token(get_social_api(user, email))
    serializer = EmailDataSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.validated_data
        try:
            # Prepare email data
            subject = data["subject"]
            message = data["message"]
            to = data["to"]
            cc = data.get("cc")
            bcc = data.get("cci")
            attachments = data.get("attachments")

            graph_endpoint = f"{GRAPH_URL}me/sendMail"
            headers = get_headers(access_token)

            recipients = {"emailAddress": {"address": to}}
            if cc:
                recipients["ccRecipients"] = [{"emailAddress": {"address": cc}}]
            if bcc:
                recipients["bccRecipients"] = [{"emailAddress": {"address": bcc}}]

            email_content = {
                "message": {
                    "subject": subject,
                    "body": {"contentType": "HTML", "content": message},
                    "toRecipients": [recipients],
                }
            }

            if attachments:
                email_content["message"]["attachments"] = []

                for file_data in attachments:
                    file_name = file_data.name
                    file_content = file_data.read()

                    attachment = base64.b64encode(file_content).decode("utf-8")
                    email_content["message"]["attachments"].append(
                        {
                            "@odata.type": "#microsoft.graph.fileAttachment",
                            "name": file_name,
                            "contentBytes": attachment,
                        }
                    )
            try:
                response = requests.post(
                    graph_endpoint, headers=headers, json=email_content
                )

                if response.status_code == 202:
                    return JsonResponse(
                        {"message": "Email sent successfully!"}, status=202
                    )
                else:
                    return JsonResponse(
                        {"error": "Failed to send email"}, status=response.status_code
                    )
            except Exception as e:
                logging.exception(f"Error sending email: {e}")
                return JsonResponse({"error": str(e)}, status=500)

        except Exception as e:
            logging.exception(f"Error preparing email data: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    logging.error(f"Serializer errors: {serializer.errors}")
    return JsonResponse(serializer.errors, status=400)


def get_unique_email_senders(request):
    user = request.user
    email = request.headers.get("email")
    access_token = refresh_access_token(get_social_api(user, email))

    senders_info = get_unique_senders(access_token)
    contacts_info = get_info_contacts(access_token)
    # Convert contacts_info to a dictionary format
    contacts_dict = {
        email: contact["name"]
        for contact in contacts_info
        for email in contact["emails"]
    }

    # Merge the two dictionaries and remove duplicates
    merged_info = {
        **contacts_dict,
        **senders_info,
    }  # In case of duplicates, senders_info will overwrite contacts_dict

    return Response(merged_info, status=200)


def find_user_in_emails(access_token, search_query):
    messages = search_emails(access_token, search_query)

    if not messages:
        return "No matching emails found."

    return messages


def search_emails(access_token, search_query, max_results=2):
    graph_endpoint = f"{GRAPH_URL}me/messages"

    try:
        headers = get_headers(access_token)

        # Use $filter to achieve search functionality
        filter_expression = f"startswith(subject, '{search_query}') or startswith(body/content, '{search_query}')"

        params = {"$filter": filter_expression, "$top": max_results}

        response = requests.get(graph_endpoint, headers=headers, params=params)
        response.raise_for_status()

        messages = response.json().get("value", [])

        found_emails = {}

        for message in messages:
            sender = message.get("from", {}).get("emailAddress", {}).get("address", "")

            if sender:
                email = sender.lower()
                name = sender.split("@")[0].lower()

                # Additional filtering: Check if the sender email/name matches the search query
                if search_query.lower() in email or search_query.lower() in name:
                    if email and not any(
                        substring in email for substring in ["noreply", "no-reply"]
                    ):
                        found_emails[email] = name

        return found_emails

    except HTTPError as e:
        logging.error(f"ERROR in Microsoft Graph API request: {str(e)}")
        return {}


######################## UNDER CONSTRUCTION ########################
def set_all_contacts(access_token, user):
    """Stores all unique contacts of an email account in DB"""
    start = time.time()

    # Microsoft Graph API endpoint for getting contacts
    graph_api_endpoint = f"{GRAPH_URL}me/contacts"
    headers = get_headers(access_token)

    try:
        # Get all contacts without specifying a page size
        with httpx.Client() as client:
            response = client.get(graph_api_endpoint, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            connections = response_data.get("value", [])

            # Combine all contacts into a dictionary to ensure uniqueness
            all_contacts = defaultdict(set)

            # Parse and add connections
            for contact in connections:
                name = contact.get("displayName", "")
                email_address = contact.get("emailAddresses", [{}])[0].get(
                    "address", ""
                )
                all_contacts[name].add(email_address)

            # Add contacts to the database
            for name, emails in all_contacts.items():
                for email in emails:
                    try:
                        Contact.objects.create(email=email, username=name, user=user)
                    except IntegrityError:
                        # TODO: Handle duplicates gracefully (e.g., update existing records)
                        pass

            formatted_time = str(datetime.timedelta(seconds=time.time() - start))
            logging.info(
                f"Retrieved {len(all_contacts)} unique contacts in {formatted_time}"
            )

    except httpx.HTTPError as e:
        logging.exception(f"Error fetching contacts: {str(e)}")


def parse_name_and_email(sender):
    if not sender:
        return None, None

    name = sender.get("emailAddress", {}).get("name")
    email = sender.get("emailAddress", {}).get("address")

    return name, email


def parse_recipients(recipients):
    if not recipients:
        return []

    parsed_recipients = []
    for recipient in recipients:
        name, email = parse_name_and_email(recipient)
        parsed_recipients.append((name, email))

    return parsed_recipients


def parse_message_body(message_data):
    if "body" in message_data:
        body = message_data["body"]
        if body["contentType"] == "text":
            return body["content"]
        elif body["contentType"] == "html":
            return body["content"]
        elif body["contentType"] == "multipart":
            return body["content"]
    return None


def get_mail(access_token, int_mail=None, id_mail=None):
    """Retrieve email information including subject, sender, content, CC, BCC, and ID"""

    url = f"{GRAPH_URL}me/messages"
    headers = get_headers(access_token)

    if int_mail is not None:
        # Fetch specific message by index
        response = requests.get(url, headers=headers)
        messages = response.json().get("value", [])

        if not messages:
            return None

        message_id = messages[int_mail]["id"]
    elif id_mail is not None:
        # Fetch message by message id
        message_id = id_mail
    else:
        return None

    # Make request to fetch specific message
    message_url = f"{url}/{message_id}"
    response = requests.get(message_url, headers=headers)
    message_data = response.json()

    # Extract necessary information from the message data
    subject = message_data.get("subject")
    sender = message_data.get("from")
    from_info = parse_name_and_email(sender)
    cc_info = parse_recipients(message_data.get("ccRecipients"))
    bcc_info = parse_recipients(message_data.get("bccRecipients"))
    decoded_data = parse_message_body(message_data)

    # Perform additional processing as needed
    preprocessed_data = library.preprocess_email(decoded_data)

    return subject, from_info, preprocessed_data, cc_info, bcc_info, message_id


def processed_email_to_bdd(user, email):
    access_token = refresh_access_token(get_social_api(user, email))
    subject, from_name, decoded_data, cc, bcc, email_id = get_mail(
        access_token, 0, None
    )

    if not Email.objects.filter(provider_id=email_id).exists():

        if decoded_data:
            decoded_data = library.format_mail(decoded_data)

        category_list = library.get_db_categories(user)

        user_description = ""
        topic, importance, answer, summary, sentence, relevance, importance_explain = (
            gpt_3_5_turbo.categorize_and_summarize_email(
                subject, decoded_data, category_list, user_description
            )
        )

        sender_name, sender_email = from_name[0], from_name[1]

        sender, _ = Sender.objects.get_or_create(name=sender_name, email=sender_email)

        category = Category.objects.get_or_create(name=topic, user=user)[0]

        provider = "Outlook"

        try:
            email_entry = Email.objects.create(
                provider_id=email_id,
                email_provider=provider,
                email_short_summary=sentence,
                content=decoded_data,
                subject=subject,
                priority=importance[0],
                read=False,
                answer_later=False,
                sender=sender,
                category=category,
                user=user,
            )

            if summary:
                lines = summary.split("\n")
                bullet_points = [
                    line[2:].strip() for line in lines if line.strip().startswith("- ")
                ]

                for point in bullet_points:
                    BulletPoint.objects.create(content=point, email=email_entry)

        except IntegrityError:
            pass

    else:
        pass

    return


'''@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_parsed_contacts(request) -> list:
    """Returns a list of parsed unique contacts with email types"""
    user = request.user
    email = request.headers.get("email")
    access_token = refresh_access_token(get_social_api(user, email))

    try:
        if access_token:
            headers = get_headers(access_token)

            # Get contacts using Microsoft Graph API
            graph_endpoint = (
                f"{GRAPH_URL}me/contacts?$select=displayName,emailAddresses"
            )
            response = requests.get(graph_endpoint, headers=headers)

            parsed_contacts = []
            if response.status_code == 200:
                contacts = response.json().get("value", [])
                for contact in contacts:
                    names = contact.get("displayName", "")
                    emails = contact.get("emailAddresses", [])
                    if names and emails:
                        for email_info in emails:
                            email = email_info.get("address", "")
                            email_type = email_info.get(
                                "type", ""
                            )  # Get the email type if available
                            if email_type:
                                name_with_type = f"[{email_type}] {names}"
                                parsed_contacts.append(
                                    {"name": name_with_type, "email": email}
                                )
                            else:
                                parsed_contacts.append({"name": names, "email": email})

                # Get unique sender information from Outlook
                unique_senders = get_unique_senders(access_token)
                for email, name in unique_senders.items():
                    parsed_contacts.append({"name": name, "email": email})

                logging.info(
                    f"{Fore.YELLOW}Retrieved {len(parsed_contacts)} unique contacts"
                )
                return JsonResponse(parsed_contacts)

            else:
                error_message = (
                    response.json()
                    .get("error", {})
                    .get("message", "Failed to fetch contacts")
                )
                return JsonResponse(
                    {"error": error_message}, status=response.status_code
                )

        else:
            return JsonResponse({"error": "Access token not found"}, status=400)

    except Exception as e:
        logging.exception(f"{Fore.YELLOW}Error fetching contacts: {e}")
        return JsonResponse({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)'''
