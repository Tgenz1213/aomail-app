"""
Handles authentication and HTTP requests for the Gmail API.
"""

import base64
import datetime
import logging
import re
import threading
import time
import json
from django.http import JsonResponse
import requests
from collections import defaultdict
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import redirect
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.auth import exceptions as auth_exceptions
from google.auth.transport.requests import Request
from google.oauth2 import credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from httpx import HTTPError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from email.utils import parsedate_to_datetime
from MailAssistant.serializers import EmailDataSerializer
from MailAssistant.ai_providers import gpt_3_5_turbo, claude, mistral
from MailAssistant.constants import (
    DEFAULT_CATEGORY,
    GOOGLE_CONFIG,
    GOOGLE_CREDS,
    GOOGLE_EMAIL_MODIFY,
    GOOGLE_LISTENER_API_KEY,
    GOOGLE_PROJECT_ID,
    GOOGLE_PROVIDER,
    GOOGLE_TOPIC_NAME,
    IMPORTANT,
    USELESS,
    INFORMATION,
    REDIRECT_URI,
    GOOGLE_SCOPES,
)
from .. import library
from ..models import Rule, SocialAPI, Contact, BulletPoint, Category, Email, Sender
from base64 import urlsafe_b64encode


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


######################## AUTHENTIFICATION ########################
def generate_auth_url(request):
    """Generate a connection URL to obtain the authorization code"""
    flow = Flow.from_client_secrets_file(
        GOOGLE_CREDS, scopes=GOOGLE_SCOPES, redirect_uri=REDIRECT_URI
    )

    authorization_url, _ = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )

    # Redirect the user to Google's consent screen
    return redirect(authorization_url)


def exchange_code_for_tokens(authorization_code):
    """Return tokens Exchanged with authorization code"""
    flow = Flow.from_client_secrets_file(
        GOOGLE_CREDS, scopes=GOOGLE_SCOPES, redirect_uri=REDIRECT_URI
    )
    flow.fetch_token(code=authorization_code)

    credentials = flow.credentials

    if credentials:
        access_token = credentials.token
        refresh_token = credentials.refresh_token

        return access_token, refresh_token
    else:
        return Response({"error": "tokens not found"}, status=400)


######################## CREDENTIALS ########################
def get_credentials(user, email):
    try:
        social_api = SocialAPI.objects.get(user=user, email=email)
        creds_data = {
            "token": social_api.access_token,
            "refresh_token": social_api.refresh_token,
            "token_uri": GOOGLE_CONFIG["token_uri"],
            "client_id": GOOGLE_CONFIG["client_id"],
            "client_secret": GOOGLE_CONFIG["client_secret"],
            "scopes": GOOGLE_SCOPES,
        }
        creds = credentials.Credentials.from_authorized_user_info(creds_data)

    except ObjectDoesNotExist:
        LOGGER.error(f"No credentials for user with ID {user.id} and email: {email}")
        creds = None

    return creds


def refresh_credentials(creds):
    try:
        creds.refresh(Request())
    except auth_exceptions.RefreshError as e:
        LOGGER.error(f"Failed to refresh credentials: {str(e)}")
        creds = None
    return creds


def save_credentials(creds, user, email):
    """Update the database with valid access token"""
    try:
        social_api = SocialAPI.objects.get(user=user, email=email)
        social_api.access_token = creds.token
        social_api.save()
    except Exception as e:
        LOGGER.error(f"Failed to save credentials: {str(e)}")


def build_services(creds) -> dict:
    """Returns a dictionary of endpoints"""
    services = {
        "gmail.readonly": build(
            "gmail", "v1", cache_discovery=False, credentials=creds
        ),
        "gmail.modify": build("gmail", "v1", cache_discovery=False, credentials=creds),
        "gmail.send": build("gmail", "v1", cache_discovery=False, credentials=creds),
        "calendar": build("calendar", "v3", cache_discovery=False, credentials=creds),
        "contacts": build("people", "v1", cache_discovery=False, credentials=creds),
        "profile": build("people", "v1", cache_discovery=False, credentials=creds),
        "email": build("people", "v1", cache_discovery=False, credentials=creds),
    }
    return services


def authenticate_service(user, email) -> dict:
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

    services = build_services(creds)
    return services


######################## EMAIL REQUESTS ########################
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_email(request):
    """Sends an email using the Gmail API."""
    try:
        user = request.user
        email = request.headers.get("email")
        service = authenticate_service(user, email)["gmail.send"]
        serializer = EmailDataSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            subject = data["subject"]
            message = data["message"]
            to = data["to"]
            cc = data["cc"]
            bcc = data["cci"]
            attachments = data.get("attachments", "")

            multipart_message = MIMEMultipart()
            multipart_message["Subject"] = subject
            multipart_message["from"] = "me"
            multipart_message["to"] = to

            if cc:
                multipart_message["cc"] = cc
            if bcc:
                multipart_message["bcc"] = bcc

            multipart_message.attach(MIMEText(message, "html"))

            # Attach each file in the attachments list
            if attachments:
                for uploaded_file in attachments:
                    # Read the contents of the uploaded file
                    file_content = uploaded_file.read()
                    part = MIMEApplication(file_content)
                    part.add_header(
                        "Content-Disposition", "attachment", filename=uploaded_file.name
                    )
                    multipart_message.attach(part)

            raw_message = urlsafe_b64encode(
                multipart_message.as_string().encode("UTF-8")
            ).decode()
            body = {"raw": raw_message}
            service.users().messages().send(userId="me", body=body).execute()

            return Response({"message": "Email sent successfully!"}, status=200)

        else:
            keys = serializer.errors.keys()

            if "to" in keys:
                return Response({"error": "recipient is missing"}, status=400)
            elif "subject" in keys:
                return Response({"error": "subject is missing"}, status=400)
            else:
                return Response({"error": serializer.errors}, status=400)

    except Exception as e:
        LOGGER.error(f"Failed to send email: {str(e)}")
        return Response({"error": str(e)}, status=500)


def delete_email(user, email, email_id) -> dict:
    """Moves the email to the bin of the user"""
    gmail_service = authenticate_service(user, email)["gmail.modify"]

    if not gmail_service:
        return {"error": "No gmail service provided"}

    try:
        response = (
            gmail_service.users().messages().trash(userId="me", id=email_id).execute()
        )

        if "id" in response:
            return {"message": "Email moved to trash successfully!"}
        else:
            LOGGER.error(f"Failed to move email with ID: {email_id} to trash")
            return {"error": f"Failed to move email to trash"}
    except HTTPError as e:
        if "Requested entity was not found" in str(e):
            return {"message": "Email moved to trash successfully!"}
        else:
            LOGGER.error(f"Error when deleting email: {str(e)}")
            return {"error": str(e)}


def get_info_contacts(services):
    """Fetch the name and the email of the contacts of the user"""
    service = services["contacts"]

    # Request a list of all the user's connections (contacts)
    results = (
        service.people()
        .connections()
        .list(
            resourceName="people/me",
            pageSize=1000,  # Adjust the page size as needed
            personFields="names,emailAddresses",
        )
        .execute()
    )

    contacts = results.get("connections", [])

    names_emails = []
    for contact in contacts:
        # Extract the name and email address of each contact
        name = contact.get("names", [{}])[0].get("displayName")
        email_addresses = [
            email["value"] for email in contact.get("emailAddresses", [])
        ]

        names_emails.append({"name": name, "emails": email_addresses})

    return names_emails


def get_mail(services, int_mail=None, id_mail=None):
    """Retrieve email information including subject, sender, content, CC, BCC, and ID"""
    service = services["gmail.readonly"]
    plaintext_var = [0]
    plaintext_var[0] = 0

    if int_mail is not None:
        results = (
            service.users().messages().list(userId="me", labelIds=["INBOX"]).execute()
        )
        messages = results.get("messages", [])
        if not messages:
            LOGGER.info("No new messages.")
            return None
        message = messages[int_mail]
        email_id = message["id"]
    elif id_mail is not None:
        email_id = id_mail
    else:
        LOGGER.info("Either int_mail or id_mail must be provided")
        return None

    msg = service.users().messages().get(userId="me", id=email_id).execute()

    subject = from_info = cc_info = bcc_info = decoded_data = None
    email_data = msg["payload"]["headers"]
    web_link = f"https://mail.google.com/mail/u/0/#inbox/{email_id}"

    for values in email_data:
        name = values["name"]
        if name == "Subject":
            subject = values["value"]
        elif name == "From":
            from_info = parse_name_and_email(values["value"])
        elif name == "Cc":
            cc_info = parse_name_and_email(values["value"])
        elif name == "Bcc":
            bcc_info = parse_name_and_email(values["value"])
        elif name == "Date":
            sent_date = parsedate_to_datetime(values["value"])

    if "parts" in msg["payload"]:
        for part in msg["payload"]["parts"]:
            decoded_data_temp = library.process_part(part, plaintext_var)
            if decoded_data_temp:
                decoded_data = library.concat_text(decoded_data, decoded_data_temp)
    elif "body" in msg["payload"]:
        data = msg["payload"]["body"]["data"]
        data = data.replace("-", "+").replace("_", "/")
        decoded_data_temp = base64.b64decode(data).decode("utf-8")
        decoded_data = library.html_clear(decoded_data_temp)

    preprocessed_data = library.preprocess_email(decoded_data)

    return (
        subject,
        from_info,
        preprocessed_data,
        cc_info,
        bcc_info,
        email_id,
        sent_date,
        web_link,
    )


# ----------------------- READ EMAIL -----------------------#
def find_user_in_emails(services, search_query):
    """Search for user in emails based on a query"""
    emails = search_emails(services, search_query)

    if not emails:
        return "No matching emails found."

    return emails


def parse_name_and_email(header_value):
    if not header_value:
        return None, None

    # Regex to extract name and email
    match = re.match(r"(.*)\s*<(.+)>", header_value)
    if match:
        name, email = match.groups()
        return name.strip(), email.strip()
    else:
        # If the format doesn't match, assume the entire value is the email
        return None, header_value.strip()


# V2 : better to check the mail structure (comparing with the input)
def search_emails(services, search_query, max_results=2):
    """Searches for emails in the user's mailbox based on the provided search query in both the subject and body."""
    service = services["gmail.readonly"]

    # Fetch the list of emails based on the query
    try:
        results = (
            service.users()
            .messages()
            .list(userId="me", q=search_query, maxResults=max_results)
            .execute()
        )
        messages = results.get("messages", [])
        found_emails = {}

        for message in messages:
            msg = (
                service.users()
                .messages()
                .get(
                    userId="me",
                    id=message["id"],
                    format="metadata",
                    metadataHeaders=["From"],
                )
                .execute()
            )
            headers = msg.get("payload", {}).get("headers", [])
            sender = next(
                (header["value"] for header in headers if header["name"] == "From"),
                None,
            )

            if sender:
                email = sender.split("<")[-1].split(">")[0].strip().lower()
                name = sender.split("<")[0].strip().lower() if "<" in sender else email

                # Additional filtering: Check if the sender email/name matches the search query
                if search_query.lower() in email or search_query.lower() in name:
                    if email and not any(
                        substring in email for substring in ["noreply", "no-reply"]
                    ):
                        found_emails[email] = name

        return found_emails

    except Exception as e:
        LOGGER.error(f"Failed to search emails: {str(e)}")
        return {}


######################## PROFILE REQUESTS ########################
def set_all_contacts(user, email):
    """Stores all unique contacts of an email account in DB"""
    start = time.time()

    credentials = get_credentials(user, email)
    services = build_services(credentials)
    contacts_service = services["contacts"]
    gmail_service = services["gmail.readonly"]

    try:
        all_contacts = defaultdict(set)

        # Part 1: Retrieve from Google Contacts
        next_page_token = None
        while True:
            response = (
                contacts_service.people()
                .connections()
                .list(
                    resourceName="people/me",
                    personFields="names,emailAddresses,metadata",
                    pageSize=1000,
                    pageToken=next_page_token,
                )
                .execute()
            )

            connections = response.get("connections", [])
            next_page_token = response.get("nextPageToken")

            for contact in connections:
                names = contact.get("names", [{}])
                email_addresses = contact.get("emailAddresses", [])
                metadata = contact.get("metadata", {})
                contact_id = metadata.get("sources", [{}])[0].get("id", "")
                name = names[0].get("displayName", "") if names else ""

                for email_info in email_addresses:
                    email_address = email_info.get("value", "")
                    if email_address:
                        all_contacts[(name, email_address, user.id, contact_id)].add(
                            email_address
                        )

            if not next_page_token:
                break

        # Part 2: Retrieving from Gmail
        response = gmail_service.users().messages().list(userId="me", q="").execute()
        messages = response.get("messages", [])

        for msg in messages[:500]:  # Limit to the first 500 messages
            message = (
                gmail_service.users()
                .messages()
                .get(
                    userId="me",
                    id=msg["id"],
                    format="metadata",
                    metadataHeaders=["From"],
                )
                .execute()
            )
            headers = message.get("payload", {}).get("headers", [])
            from_header = next(
                (item for item in headers if item["name"] == "From"), None
            )
            if from_header:
                from_value = from_header["value"]
                if "reply" in from_value.lower():
                    continue

                email_match = re.search(r"[\w\.-]+@[\w\.-]+", from_value)
                name_match = re.search(r'(?:"?([^"]*)"?\s)?', from_value)

                email = email_match.group(0) if email_match else None
                name = (
                    name_match.group(1) if name_match and name_match.group(1) else email
                )

                if not email:
                    continue

                if (name, email, user.id, "") in all_contacts:
                    continue
                else:
                    all_contacts[(name, email, user.id, "")].add(email)

        # Part 3: Add the contacts to the database
        for contact_info, _ in all_contacts.items():
            name, email, _, contact_id = contact_info
            if name and email:
                library.save_email_sender(user, name, email, contact_id)

        formatted_time = str(datetime.timedelta(seconds=time.time() - start))
        LOGGER.info(
            f"Retrieved {len(all_contacts)} unique contacts in {formatted_time}"
        )

    except Exception as e:
        LOGGER.error(f"Error fetching contacts: {str(e)}")


def get_unique_senders(services) -> dict:
    """Fetches unique sender information from Gmail messages"""
    service = services["gmail.readonly"]
    limit = 50
    results = (
        service.users()
        .messages()
        .list(userId="me", labelIds=["INBOX"], maxResults=limit)
        .execute()
    )
    messages = results.get("messages", [])

    senders_info = {}

    if not messages:
        LOGGER.info("No messages found")
    else:
        for message in messages:
            try:
                msg = (
                    service.users()
                    .messages()
                    .get(
                        userId="me",
                        id=message["id"],
                        format="metadata",
                        metadataHeaders=["From"],
                    )
                    .execute()
                )
                headers = msg["payload"]["headers"]
                sender_header = next(
                    header["value"] for header in headers if header["name"] == "From"
                )

                # Extracting the email address and name
                sender_parts = sender_header.split("<")
                sender_name = sender_parts[0].strip().strip('"')
                sender_email = (
                    sender_parts[-1].split(">")[0].strip()
                    if len(sender_parts) > 1
                    else sender_name
                )

                # Store the sender's name with the email address as the key
                senders_info[sender_email] = sender_name
            except Exception as e:
                LOGGER.error(
                    f"Error processing message with ID {message['id']}: {str(e)}"
                )

    return senders_info


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile_image(request):
    """Returns the profile image of the user"""
    user = request.user
    email = request.headers.get("email")
    credentials = get_credentials(user, email)
    service = build_services(credentials)["profile"]

    try:
        profile = (
            service.people()
            .get(resourceName="people/me", personFields="photos")
            .execute()
        )

        if "photos" in profile:
            photos = profile["photos"]
            if photos:
                photo_url = photos[0]["url"]
                return Response({"profile_image_url": photo_url})

        return Response(
            {"profile_image_url": "Profile image URL not found in response"}, status=404
        )

    except Exception as e:
        return Response(
            {"error": f"Error retrieving profile image: {str(e)}"}, status=505
        )


def get_email(access_token, refresh_token):
    """Returns the primary email of the user"""
    creds_data = {
        "token": access_token,
        "refresh_token": refresh_token,
        "token_uri": GOOGLE_CONFIG["token_uri"],
        "client_id": GOOGLE_CONFIG["client_id"],
        "client_secret": GOOGLE_CONFIG["client_secret"],
        "scopes": GOOGLE_SCOPES,
    }
    creds = credentials.Credentials.from_authorized_user_info(creds_data)

    try:
        service = build_services(creds)["profile"]
        user_info = (
            service.people()
            .get(resourceName="people/me", personFields="emailAddresses")
            .execute()
        )
        email = user_info.get("emailAddresses", [{}])[0].get("value", "")
        return email

    except Exception as e:
        LOGGER.error(f"Could not get email: {str(e)}")
        return None


######################## GOOGLE LISTENER ########################
def subscribe_to_email_notifications(user, email) -> bool:
    """Subscribe the user to email notifications for a specific topic in Google."""

    try:
        LOGGER.info(
            f"Initiationg the subscription to Google listener for: {user} with email: {email}"
        )
        credentials = get_credentials(user, email)
        services = build_services(credentials)
        if services is None:
            return False

        gmail_service = services["gmail.readonly"]

        request_body = {
            "labelIds": ["INBOX"],
            "topicName": f"projects/{GOOGLE_PROJECT_ID}/topics/{GOOGLE_TOPIC_NAME}",
        }

        response = gmail_service.users().watch(userId="me", body=request_body).execute()

        if "historyId" in response:
            LOGGER.info(
                f"Successfully subscribed to email notifications for user {user.username} and email {email}"
            )
            return True
        else:
            LOGGER.error(
                f"Failed to subscribe to email notifications for user with ID: {user.id} and email {email}"
            )
            return False

    except Exception as e:
        LOGGER.error(
            f"An error occurred while subscribing to email notifications: {str(e)}"
        )
        return False


@api_view(["POST"])
@permission_classes([AllowAny])
def receive_mail_notifications(request):
    """Process email notifications from Google listener"""

    try:
        print("!!! [GOOGLE] EMAIL RECEIVED !!!")
        envelope = json.loads(request.body.decode("utf-8"))
        message_data = envelope["message"]

        decoded_data = base64.b64decode(message_data["data"]).decode("utf-8")
        decoded_json = json.loads(decoded_data)
        attributes = message_data.get("attributes", {})
        email_id = attributes.get("emailId")
        email = decoded_json.get("emailAddress")

        try:
            social_api = SocialAPI.objects.get(email=email)
            services = authenticate_service(social_api.user, email)

            print("STARTING THREAD TO PROCESS EMAIL SUCCESFULLY")

            threading.Thread(
                target=email_to_bdd, args=(social_api.user, services, email_id)
            ).start()
        except SocialAPI.DoesNotExist:
            LOGGER.error(f"SocialAPI entry not found for the email: {email}")

        # TODO: add API key to avoid error 403
        # ack_url = f"https://pubsub.googleapis.com/v1/{subscription_path}:acknowledge?key={GOOGLE_LISTENER_API_KEY}"
        # authenticate_service(social_api.user, email)
        # social_api = SocialAPI.objects.get(email=email)
        # headers = {"Authorization": f"Bearer {social_api.access_token}"}
        # print(f"\n\n\ncreds: {social_api.access_token}\n\n\n")
        # response = requests.post(ack_url, json=ack_payload, headers=headers)

        # Sending the reception message to Google to confirm the email reception
        subscription_path = envelope["subscription"]
        #print("DEBUG subscription path >>>>>>>>>>>>", subscription_path)
        ack_id = message_data["messageId"]
        ack_url = f"https://pubsub.googleapis.com/v1/{subscription_path}:acknowledge"
        ack_payload = {"ackIds": [ack_id]}

        response = requests.post(ack_url, json=ack_payload)

        if response.status_code == 200:
            LOGGER.info("Acknowledgement sent successfully")

        elif response.status_code == 403:
            LOGGER.info(
                "Acknowledgement sent successfully, You just do not have the right KEY to do it properly"
            )
        else:
            LOGGER.info("DEBUG RESPONSE====================>", response.json())
            LOGGER.error(
                f"Failed to send acknowledgement for gmail with id {email_id}: {response.reason}"
            )

        return Response(status=200)

    except IntegrityError:
        return Response(status=200)

    except Exception as e:
        LOGGER.error(f"Error processing the notification: {str(e)}")
        return Response({"error": str(e)}, status=500)

#######################################################################################################
############################################# UNDER TEST ##############################################
#######################################################################################################

def email_to_bdd(user, services, id_email):
    """Saves email notifications from Google listener to database"""

    subject, from_name, decoded_data, _, _, email_id, sent_date, web_link = get_mail(
        services, 0, id_email
    )

    if not Email.objects.filter(provider_id=email_id).exists():
        sender = Sender.objects.filter(email=from_name[1]).first()

        if not decoded_data:
            return

        decoded_data = library.format_mail(decoded_data)
        category_dict = library.get_db_categories(user)
        category = Category.objects.get(name=DEFAULT_CATEGORY, user=user)
        rules = Rule.objects.filter(sender=sender)
        rule_category = None

        if rules.exists():
            for rule in rules:
                if rule.block:
                    return

                if rule.category:
                    # Find the category by checking if a sender has a category
                    category = rule.category
                    rule_category = True

        # user_description = "Enseignant chercheur au sein d'une école d'ingénieur ESAIP."
        user_description = ""
        (
            topic,
            importance_dict,
            answer,
            summary_list,
            sentence,
            relevance,
        ) = claude.categorize_and_summarize_email(
            subject, decoded_data, category_dict, user_description
        )

        if (
            importance_dict["UrgentWorkInformation"] >= 50
        ):  # MAYBE TO UPDATE TO >50 =>  To test
            importance = IMPORTANT 
        elif importance_dict['Promotional'] <= 50 and importance_dict['RoutineWorkUpdates'] > 10: # To avoid some error that might put a None promotional email in Useless => Ask Theo before Delete
            importance = INFORMATION
        else:
            max_percentage = 0
            for key, value in importance_dict.items():
                if value > max_percentage:
                    importance = key
                    if importance == "Promotional" or importance == "News":
                        importance = USELESS
                    elif (
                        importance == "RoutineWorkUpdates"
                        or importance == "InternalCommunications"
                    ):
                        importance = INFORMATION
                    elif importance == "UrgentWorkInformation":
                        importance = IMPORTANT
                    max_percentage = importance_dict[key]
            if max_percentage == 0:
                importance = INFORMATION

        if not rule_category:
            if topic in category_dict.keys():
                category = Category.objects.get(name=topic, user=user)

        if not sender:
            sender_name, sender_email = from_name[0], from_name[1]
            if not sender_name:
                sender_name = sender_email
            sender, _ = Sender.objects.get_or_create(
                name=sender_name, email=sender_email
            )

        try:
            email_entry = Email.objects.create(
                provider_id=email_id,
                email_provider=GOOGLE_PROVIDER,
                email_short_summary=sentence,
                content=decoded_data,
                subject=subject,
                priority=importance,
                read=False,
                answer_later=False,
                sender=sender,
                category=category,
                user=user,
                date=sent_date,
                web_link=web_link,
            )

            if summary_list:
                for point in summary_list:
                    BulletPoint.objects.create(content=point, email=email_entry)

        except Exception as e:
            LOGGER.error(
                f"An error occurred when trying to create an email with ID {email_id}: {str(e)}"
            )


"""
####################################################################
######################## UNDER CONSTRUCTION ########################
####################################################################


# TODO: handle all email providers
# TODO: remove hardcoded user_desription and ask user to input its own description on signu-up
# TODO: add possibility to modify user_desription in settings
def processed_email_to_bdd(request, services):
    subject, from_name, decoded_data, _, _, email_id, date = get_mail(services, 0, None)

    if not Email.objects.filter(provider_id=email_id).exists():
        if decoded_data:
            decoded_data = library.format_mail(decoded_data)

        # Get user categories
        category_dict = library.get_db_categories(request.user)

        # Process the email data with AI/NLP
        # user_description = "Enseignant chercheur au sein d'une école d'ingénieur ESAIP."
        user_description = ""
        (
            topic,
            importance_dict,
            answer,
            summary,
            sentence,
            relevance,
        ) = (
            # gpt_3_5_turbo
            # claude
            mistral.categorize_and_summarize_email(
                subject, decoded_data, category_dict, user_description
            )
        )

        # Extract the importance of the email
        if importance_dict[IMPORTANT] == 50:
            importance = IMPORTANT
        else:
            for key, value in importance_dict.items():
                if value >= 51:
                    importance = key

        sender_name, sender_email = from_name[0], from_name[1]
        sender, _ = Sender.objects.get_or_create(name=sender_name, email=sender_email)

        # Get the relevant category based
        # TODO: if not exist put in other
        category = Category.objects.get_or_create(name=topic, user=request.user)[0]

        try:
            email_entry = Email.objects.create(
                provider_id=email_id,
                email_provider=GOOGLE_PROVIDER,
                email_short_summary=sentence,
                content=decoded_data,
                subject=subject,
                priority=importance,
                read=False,
                answer_later=False,
                sender=sender,
                category=category,
                user=request.user,
                date=date,
            )

            # If the email has a summary, save it in the BulletPoint table
            if summary:
                for point in summary:
                    BulletPoint.objects.create(content=point, email=email_entry)

        except Exception as e:
            LOGGER.error(
                f"An error occurred when trying to create an email with ID {email_id}: {str(e)}"
            )

        # Debug prints
        LOGGER.info(f"topic: {topic}")
        LOGGER.info(f"importance: {importance}")
        LOGGER.info(f"answer: {answer}")
        LOGGER.info(f"summary: {summary}")
        LOGGER.info(f"sentence:  {sentence}")
        LOGGER.info(f"relevance: {relevance}")
        LOGGER.info(f"importance_dict:  {importance_dict}")"""


'''@api_view(["GET"])
@permission_classes([IsAuthenticated])
def unread_mails(request):
    """Returns the number of unread emails"""
    try:
        user = request.user
        email = request.headers.get("email")
        unread_count = 0
        service = authenticate_service(user, email)

        if service is not None:
            try:
                response = (
                    service["gmail.readonly"]
                    .users()
                    .messages()
                    .list(userId="me", q="is:unread")
                    .execute()
                )
                unread_count = len(response.get("messages", []))
                return JsonResponse({"unreadCount": unread_count}, status=200)
            except Exception as e:
                logging.error(f"Error getting unread emails: {e}")
                return JsonResponse(
                    {"error": "Failed to retrieve unread count"}, status=500
                )

        logging.error("Failed to authenticate")
        return JsonResponse({"unreadCount": unread_count}, status=400)

    except Exception as e:
        logging.error("An error occurred: {e}")
        return JsonResponse({"unreadCount": 0}, status=400)'''


'''@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_parsed_contacts(request) -> list:
    """Returns a list of parsed unique contacts e.g: [{name: example, email: example@test.com}]"""
    start = time.time()

    user = request.user
    email = request.headers.get("email")
    # Authenticate the user and build the service
    credentials = get_credentials(user, email)
    services = build_services(credentials)
    contacts_service = services["contacts"]

    try:
        # Get contacts
        contacts = (
            contacts_service.people()
            .connections()
            .list(resourceName="people/me", personFields="names,emailAddresses")
            .execute()
        )

        # Get other contacts
        other_contacts = (
            contacts_service.otherContacts()
            .list(pageSize=1000, readMask="names,emailAddresses")
            .execute()
        )

        # Get unique sender information from Gmail
        unique_senders = get_unique_senders(services)

        # Combine all contacts into a dictionary to ensure uniqueness
        all_contacts = defaultdict(set)

        # Parse contacts and other contacts
        contact_types = {
            "connections": contacts.get("connections", []),
            "otherContacts": other_contacts.get("otherContacts", []),
        }

        # Parse contacts and other contacts
        for _, contact_list in contact_types.items():
            for contact in contact_list:
                names = contact.get("names", [])
                emails = contact.get("emailAddresses", [])
                if names and emails:
                    name = names[0].get("displayName", "")
                    email = emails[0].get("value", "")
                    all_contacts[email].add(name)

        # Add unique sender information
        for email, name in unique_senders.items():
            all_contacts[email].add(name)

        # Format the parsed contacts
        parsed_contacts = [
            {"name": ", ".join(names), "email": email}
            for email, names in all_contacts.items()
        ]

        formatted_time = str(datetime.timedelta(seconds=time.time() - start))
        print(f"{Fore.BLUE}{parsed_contacts}")
        logging.info(
            f"{Fore.YELLOW}Retrieved {len(parsed_contacts)} unique contacts in {formatted_time}"
        )

        return Response(parsed_contacts)
    except Exception as e:
        logging.exception("Error fetching contacts:")
        return Response({"error": str(e)}, status=500)'''


'''
def set_all_contacts(user, email):
    """Stores all unique contacts of an email account in DB"""
    start = time.time()

    # Authenticate the user and build the service
    credentials = get_credentials(user, email)
    services = build_services(credentials)
    contacts_service = services["contacts"]

    try:
        # Get all contacts without specifying a page size
        all_contacts = defaultdict(set)
        next_page_token = None

        while True:
            connections = (
                contacts_service.people()
                .connections()
                .list(
                    resourceName="people/me",
                    personFields="names,emailAddresses",
                    pageSize=1000,
                    pageToken=next_page_token,
                )
                .execute()
                .get("connections", [])
            )

            # Parse and add connections
            for contact in connections:
                name = contact.get("names", [{}])[0].get("displayName", "")
                email_address = contact.get("emailAddresses", [{}])[0].get("value", "")
                all_contacts[name].add(email_address)

            # Update next_page_token directly from the list
            next_page_token = connections[-1].get("nextPageToken")

            if not next_page_token:
                break

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
            f"{Fore.GREEN}Retrieved {len(all_contacts)} unique contacts in {formatted_time}"
        )

    except Exception as e:
        logging.exception(f"Error fetching contacts: {str(e)}")'''


"""def get_unique_email_senders(request):
    user = request.user
    email = request.headers.get("email")
    services = authenticate_service(user, email)

    if services:
        senders_info = get_unique_senders(services)
        contacts_info = get_info_contacts(services)
    else:
        return Response(
            {"error": "Failed to authenticate or access services"}, status=400
        )

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

    return Response(merged_info, status=200)"""


"""# TODO: handle all email providers
# TODO: remove hardcoded user_desription and ask user to input its own description on signu-up
# TODO: add possibility to modify user_desription in settings
def processed_email_to_bdd(request, services):
    subject, from_name, decoded_data, cc, bcc, email_id, date = get_mail(
        services, 0, None
    )

    if not Email.objects.filter(provider_id=email_id).exists():

        # Check if data is decoded, then format it
        if decoded_data:
            decoded_data = library.format_mail(decoded_data)

        # Get user categories
        category_dict = library.get_db_categories(request.user)

        # print("DEBUG -------------> category", category_dict)

        # Process the email data with AI/NLP
        # user_description = "Enseignant chercheur au sein d'une école d'ingénieur ESAIP."
        user_description = ""
        (
            topic,
            importance_dict,
            answer,
            summary,
            sentence,
            relevance,
            importance_dict,
        ) = (
            # gpt_3_5_turbo
            # claude
            mistral.categorize_and_summarize_email(
                subject, decoded_data, category_dict, user_description
            )
        )

        # Extract the importance of the email
        if importance_dict[IMPORTANT] == 50:
            importance = IMPORTANT
        else:
            for key, value in importance_dict.items():
                if value >= 51:
                    importance = key

        # print("TEST -------------->", from_name, "TYPE ------------>", type(from_name))
        # sender_name, sender_email = separate_name_email(from_name) => OLD USELESS
        sender_name, sender_email = from_name[0], from_name[1]

        # Fetch or create the sender
        sender, _ = Sender.objects.get_or_create(name=sender_name, email=sender_email)

        LOGGER.info(f"[processed_email_to_bdd] topic: {topic}")
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
                priority=importance,
                read=False,
                answer_later=False,
                sender=sender,
                category=category,
                user=request.user,
                date=date,
            )

            # If the email has a summary, save it in the BulletPoint table
            if summary:
                for point in summary:
                    BulletPoint.objects.create(content=point, email=email_entry)

                # # Split summary by line breaks
                # lines = summary.split("\n")

                # # Filter lines that start with '- ' which indicates a bullet point
                # bullet_points = [
                #     line[2:].strip() for line in lines if line.strip().startswith("- ")
                # ]

                # for point in bullet_points:
                #     BulletPoint.objects.create(content=point, email=email_entry)

        except Exception as e:
            LOGGER.error(
                f"An error occurred when trying to create an email with ID {email_id}: {str(e)}"
            )

        # Debug prints
        LOGGER.info("topic:", topic)
        LOGGER.info("importance:", importance)
        LOGGER.info("answer:", answer)
        LOGGER.info("summary:", summary)
        LOGGER.info("sentence:", sentence)
        LOGGER.info("relevance:", relevance)
        LOGGER.info("importance_dict:", importance_dict)

    else:
        LOGGER.error(f"The email with ID {email_id} already exists.")"""

'''def set_all_contacts(user, email):
    """Stores all unique contacts of an email account in DB"""
    start = time.time()

    credentials = get_credentials(user, email)
    services = build_services(credentials)
    contacts_service = services["contacts"]
    gmail_service = services["gmail.readonly"]

    try:
        all_contacts = defaultdict(set)

        # Part 1 : Retreive from Google Contact
        next_page_token = None
        while True:
            response = (
                contacts_service.people()
                .connections()
                .list(
                    resourceName="people/me",
                    personFields="names,emailAddresses",
                    pageSize=1000,
                    pageToken=next_page_token,
                )
                .execute()
            )

            connections = response.get("connections", [])
            next_page_token = response.get("nextPageToken")

            for contact in connections:
                names = contact.get("names", [{}])
                email_addresses = contact.get("emailAddresses", [])
                name = names[0].get("displayName", "") if names else ""

                for email_info in email_addresses:
                    email_address = email_info.get("value", "")
                    if email_address:
                        all_contacts[name].add(email_address)

            if not next_page_token:
                break

        # Part 2 : Retreiving from Gmail
        response = gmail_service.users().messages().list(userId="me", q="").execute()
        messages = response.get("messages", [])

        for msg in messages[:500]:  # Limit to the first 500 messages
            message = (
                gmail_service.users()
                .messages()
                .get(
                    userId="me",
                    id=msg["id"],
                    format="metadata",
                    metadataHeaders=["From"],
                )
                .execute()
            )
            headers = message.get("payload", {}).get("headers", [])
            from_header = next(
                (item for item in headers if item["name"] == "From"), None
            )
            if from_header:
                from_value = from_header["value"]
                if "reply" in from_value.lower():
                    continue

                email_match = re.search(r"[\w\.-]+@[\w\.-]+", from_value)
                name_match = re.search(r'(?:"?([^"]*)"?\s)?', from_value)

                email = email_match.group(0) if email_match else None
                name = (
                    name_match.group(1) if name_match and name_match.group(1) else email
                )

                if not email:
                    continue

                if name in all_contacts:
                    continue
                else:
                    all_contacts[name].add(email)

        # Part 3 : Add the contact to the database
        for name, emails in all_contacts.items():
            for email in emails:
                if name and email:
                    library.save_email_sender(user, name, email)

        formatted_time = str(datetime.timedelta(seconds=time.time() - start))
        LOGGER.info(
            f"Retrieved {len(all_contacts)} unique contacts in {formatted_time}"
        )

    except Exception as e:
        LOGGER.error(f"Error fetching contacts: {str(e)}")'''
