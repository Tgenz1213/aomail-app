"""
Provides email search and operation functions using Microsoft Graph API.

Endpoints:
- ✅ send_schedule_email: Schedule the sending of an email.
- ✅ send_email: Sends an email using the Microsoft Graph API.
- ✅ get_mail: Retrieves email details by index or message ID.
"""

import base64
import datetime
import json
import logging
import threading
import requests
from django.http import HttpRequest
from django.core.files.uploadedfile import UploadedFile
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from aomail.utils.security import subscription
from aomail.utils.serializers import (
    EmailDataSerializer,
    EmailScheduleDataSerializer,
)
from aomail.email_providers.microsoft.authentication import (
    get_headers,
    get_social_api,
    refresh_access_token,
)
from aomail.utils import email_processing
from aomail.constants import (
    FREE_PLAN,
    GRAPH_URL,
)
from aomail.models import SocialAPI


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


def parse_name_and_email(
    sender: dict[str, dict]
) -> tuple[str, str] | tuple[None, None]:
    """
    Parses the name and email address from a sender dictionary.

    Args:
        sender (dict): Dictionary containing sender information.

    Returns:
        tuple: Tuple containing name and email address
    """
    if not sender:
        return None, None

    name = sender.get("emailAddress", {}).get("name")
    email = sender.get("emailAddress", {}).get("address")

    return name, email


def parse_recipients(recipients: list[dict[str, dict]]) -> list[tuple[str, str]]:
    """
    Parses names and email addresses from a list of recipient dictionaries.

    Args:
        recipients (list): List of dictionaries containing recipient information.

    Returns:
        list[tuple[str, str]]: List of tuples containing names and email addresses of recipients.

    """
    if not recipients:
        return []

    parsed_recipients = []
    for recipient in recipients:
        name, email = parse_name_and_email(recipient)
        parsed_recipients.append((name, email))

    return parsed_recipients


def parse_message_body(message_data: dict) -> str | None:
    """
    Parses the message body content from a message data dictionary.

    Args:
        message_data (dict): Dictionary containing message data.

    Returns:
        str | None: Message body content as string, or None if no valid content type found.

    """
    if "body" in message_data:
        body = message_data["body"]
        if body["contentType"] in ["text", "html", "multipart"]:
            return body["content"]

    return None


@api_view(["POST"])
@subscription([FREE_PLAN])
def send_schedule_email(request: HttpRequest) -> Response:
    """
    Schedule the sending of an email using the Microsoft Graph API with deferred delivery.

    Args:
        request (HttpRequest): HTTP request object containing POST data with email details.

    Returns:
        Response: Response indicating success or error.
    """
    user = request.user
    parameters: dict = json.loads(request.body)
    email = parameters.get("email")
    social_api = get_social_api(user, email)

    if not social_api:
        return Response(
            {"error": "Social API credentials not found"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    access_token = refresh_access_token(social_api)
    serializer = EmailScheduleDataSerializer(data=parameters)

    if serializer.is_valid():
        data = serializer.validated_data
        try:
            send_datetime: datetime.datetime = data["datetime"]
            subject = data["subject"]
            message = data["message"]
            to = data["to"]
            cc = data.get("cc")
            bcc = data.get("bcc")
            attachments: list[UploadedFile] = data.get("attachments", [])
            all_recipients = to + (cc if cc else []) + (bcc if bcc else [])

            graph_endpoint = f"{GRAPH_URL}me/sendMail"
            headers = get_headers(access_token)

            email_content = {
                "message": {
                    "subject": subject,
                    "body": {"contentType": "HTML", "content": message},
                    "toRecipients": [
                        {"emailAddress": {"address": email}} for email in to
                    ],
                    "singleValueExtendedProperties": [
                        {"id": "SystemTime 0x3FEF", "value": send_datetime.isoformat()}
                    ],
                }
            }

            if cc:
                email_content["message"]["ccRecipients"] = [
                    {"emailAddress": {"address": email}} for email in cc
                ]

            if bcc:
                email_content["message"]["bccRecipients"] = [
                    {"emailAddress": {"address": email}} for email in bcc
                ]

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
                    threading.Thread(
                        target=email_processing.save_contacts,
                        args=(user, email, all_recipients),
                    ).start()
                    return Response(
                        {"message": "Email scheduled successfully!"},
                        status=status.HTTP_202_ACCEPTED,
                    )
                else:
                    response_data: dict = response.json()
                    error = response_data.get("error", response.reason)
                    LOGGER.error(f"Failed to schedule email: {error}")
                    return Response({"error": error}, status=response.status_code)

            except Exception as e:
                LOGGER.error(f"Failed to send email: {str(e)}")
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        except Exception as e:
            LOGGER.error(f"Error preparing email data: {str(e)}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@subscription([FREE_PLAN])
def send_email(request: HttpRequest) -> Response:
    """
    Sends an email using the Microsoft Graph API.

    Args:
        request (HttpRequest): HTTP request object containing POST data with email details.

    Returns:
        Response: Response indicating success or error.
    """
    user = request.user
    parameters: dict = json.loads(request.body)
    email = parameters.get("email")
    social_api = get_social_api(user, email)

    if not social_api:
        return Response(
            {"error": "Social API credentials not found"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    access_token = refresh_access_token(social_api)
    serializer = EmailDataSerializer(data=parameters)

    if serializer.is_valid():
        data = serializer.validated_data
        try:
            subject = data["subject"]
            message = data["message"]
            to = data["to"]
            cc = data.get("cc")
            bcc = data.get("bcc")
            attachments: list[UploadedFile] = data.get("attachments", [])
            all_recipients = to + (cc if cc else []) + (bcc if bcc else [])

            graph_endpoint = f"{GRAPH_URL}me/sendMail"
            headers = get_headers(access_token)

            email_content = {
                "message": {
                    "subject": subject,
                    "body": {"contentType": "HTML", "content": message},
                    "toRecipients": [
                        {"emailAddress": {"address": email}} for email in to
                    ],
                }
            }

            if cc:
                email_content["message"]["ccRecipients"] = [
                    {"emailAddress": {"address": email}} for email in cc
                ]

            if bcc:
                email_content["message"]["bccRecipients"] = [
                    {"emailAddress": {"address": email}} for email in bcc
                ]

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
                    threading.Thread(
                        target=email_processing.save_contacts,
                        args=(user, email, all_recipients),
                    ).start()
                    return Response(
                        {"message": "Email sent successfully!"},
                        status=status.HTTP_202_ACCEPTED,
                    )
                else:
                    response_data: dict = response.json()
                    error = response_data.get("error", response.reason)
                    LOGGER.error(f"Failed to send email: {error}")
                    return Response({"error": error}, status=response.status_code)

            except Exception as e:
                LOGGER.error(f"Failed to send email: {str(e)}")
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        except Exception as e:
            LOGGER.error(f"Error preparing email data: {str(e)}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


def delete_email(email_id: int, social_api: SocialAPI) -> dict:
    """
    Moves the email to the bin of the user using the Microsoft Graph API.

    Args:
        email_id (int): The ID of the email to be moved to the bin.
        social_api (SocialAPI): The SocialAPI instance containing the user's access and refresh tokens.

    Returns:
        dict: A dictionary containing a success message if the email is moved to the trash successfully,
              or an error message if the operation fails.
    """
    access_token = refresh_access_token(social_api)
    headers = get_headers(access_token)
    url = f"{GRAPH_URL}/me/messages/{email_id}/move"
    data = {"destinationId": "deleteditems"}

    response = requests.post(url, headers=headers, json=data)

    if "id" in response.text:
        return {"message": "Email moved to trash successfully!"}
    elif "error" in response.text:
        return {"message": "Email moved to trash successfully!"}
    else:
        LOGGER.error(
            f"Failed to move email to trash for Social API email: {social_api.email}: {response.text}"
        )
        return {"error": f"Failed to move email to trash: {response.text}"}


def set_email_read(social_api: SocialAPI, email_id: int):
    """
    Sets the status of the email to 'read' on Outlook.

    Args:
        social_api (SocialAPI): The SocialAPI instance containing the user's access and refresh tokens.
        email_id (int): The ID of the email to be marked as read.
    """
    access_token = refresh_access_token(social_api)
    headers = get_headers(access_token)
    data = {"isRead": True}
    requests.patch(f"{GRAPH_URL}/me/messages/{email_id}/", headers=headers, json=data)


def set_email_unread(social_api: SocialAPI, email_id: int):
    """
    Sets the status of the email to 'unread' on Outlook.

    Args:
        social_api (SocialAPI): The SocialAPI instance containing the user's access and refresh tokens.
        email_id (int): The ID of the email to be marked as unread.
    """
    access_token = refresh_access_token(social_api)
    headers = get_headers(access_token)
    data = {"isRead": False}
    requests.patch(f"{GRAPH_URL}/me/messages/{email_id}/", headers=headers, json=data)


def search_emails_ai(
    access_token: str,
    max_results: int = 100,
    filenames: list = None,
    from_addresses: list = None,
    to_addresses: list = None,
    subject: str = None,
    body: str = None,
    keywords: list = None,
    date_from: str = None,
    search_in: dict = None,
) -> list:
    """
    Searches for emails matching the specified query parameters using Microsoft Graph API.

    Args:
        access_token (str): The access token for authenticating with Microsoft Graph API.
        max_results (int): The maximum number of email results to retrieve. Default is 100.
        filenames (list): A list of filenames to search for in the attachments.
        from_addresses (list): A list of sender email addresses to filter emails.
        to_addresses (list): A list of recipient email addresses to filter emails.
        subject (str): A subject string to filter emails.
        body (str): A body string to filter emails.
        keywords (list): A list of keywords to search for in the email body.
        date_from (str): A date string in the format 'YYYY-MM-DD' to filter emails received after this date.
        search_in (dict): A dictionary specifying the folders to search in. Possible keys are:
            spams: Search in spam/junk folder.
            deleted_emails: Search in deleted items folder.
            drafts: Search in drafts folder.
            sent_emails: Search in sent items folder.

    Returns:
        list: A list of email IDs that match the search criteria.
    """
    folder_url = f"{GRAPH_URL}me/mailFolders/"
    message_ids = []
    params = {"$top": max_results, "$select": "id", "$count": "true"}

    if from_addresses:
        from_query = " OR ".join(
            ["from/emailAddress:" + from_address for from_address in from_addresses]
        )
        params["from/emailAddress"] = from_query
    if to_addresses:
        recipient_query = " OR ".join(
            ["toRecipients/emailAddress:" + to_address for to_address in to_addresses]
        )
        params["toRecipients/emailAddress"] = recipient_query
    if subject:
        params["subject"] = subject
    if body:
        params["body"] = body
    if keywords:
        keyword_query = " OR ".join(keywords)
        params["body"] = (
            keyword_query
            if not params.get("body")
            else params["body"] + " OR " + keyword_query
        )
    if date_from:
        params["receivedDateTime"] = "gt" + date_from + "T00:00:00Z"
    if filenames:
        # TODO: first retrieve emails + filenames and then check with a for loop
        pass

    def run_request(graph_endpoint: str):
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(graph_endpoint, headers=headers, params=params)
            response.raise_for_status()
            data: dict = response.json()
            messages = data.get("value", [])
            message_ids.extend([message["id"] for message in messages])
        except Exception as e:
            LOGGER.error(f"Failed to search emails with AI filled parameters: {str(e)}")

    endpoints = {
        "spams": "junkemail/messages",
        "deleted_emails": "deleteditems/messages",
        "drafts": "drafts",
        "sent_emails": "sentitems",
    }
    for folder in search_in:
        if folder in endpoints and search_in[folder]:
            graph_endpoint = f"{folder_url}{endpoints[folder]}"
            run_request(graph_endpoint)

    graph_endpoint = f"{folder_url}inbox/messages"
    run_request(graph_endpoint)

    return message_ids


def search_emails_manually(
    access_token: str,
    search_query: str,
    max_results: int,
    file_extensions: list,
    advanced: bool = False,
    search_in: dict = None,
    from_addresses: list = None,
    to_addresses: list = None,
    subject: str = None,
    body: str = None,
    date_from: str = None,
) -> list:
    """
    Searches for emails matching the specified query parameters using Microsoft Graph API.

    Args:
        access_token (str): The access token for authenticating with Microsoft Graph API.
        search_query (str): The search query string to search for in emails.
        max_results (int): The maximum number of email results to retrieve.
        file_extensions (list): A list of file extensions to filter attachments by.
        advanced (bool, optional): Flag indicating whether to use advanced search options. Defaults to False.
        search_in (dict, optional): A dictionary specifying the folders to search in. Possible keys are:
            spams: Search in spam/junk folder.
            deleted_emails: Search in deleted items folder.
            drafts: Search in drafts folder.
            sent_emails: Search in sent items folder.
        from_addresses (list, optional): A list of sender email addresses to filter emails.
        to_addresses (list, optional): A list of recipient email addresses to filter emails.
        subject (str, optional): A subject string to filter emails.
        body (str, optional): A body string to filter emails.
        date_from (str, optional): A date string in the format 'YYYY-MM-DD' to filter emails received after this date.

    Returns:
        list: A list of email IDs that match the search criteria.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    folder_url = f"{GRAPH_URL}me/mailFolders/"
    graph_endpoint = f"{folder_url}inbox/messages"
    message_ids = []

    def run_request(graph_endpoint, params):
        try:
            response = requests.get(graph_endpoint, headers=headers, params=params)
            response.raise_for_status()
            data: dict = response.json()
            messages = data.get("value", [])
            message_ids.extend([message["id"] for message in messages])

        except Exception as e:
            LOGGER.error(
                f"Failed to search_emails_ai for url: {graph_endpoint}: {str(e)}"
            )

    try:
        params = {"$top": max_results, "$select": "id", "$count": "true"}

        if advanced:
            if from_addresses:
                from_query = " OR ".join(
                    [f"from/emailAddress:{address}" for address in from_addresses]
                )
                params["from/emailAddress"] = from_query
            if to_addresses:
                recipient_query = " OR ".join(
                    [f"toRecipients/emailAddress:{address}" for address in to_addresses]
                )
                params["toRecipients/emailAddress"] = recipient_query
            if subject:
                params["subject"] = subject
            if body:
                params["body"] = body
            if date_from:
                params["receivedDateTime"] = f"gt{date_from}T00:00:00Z"
            if file_extensions:
                # TODO: Retrieve emails + filenames and check with a for loop
                pass

            endpoints = {
                "spams": "junkemail/messages",
                "deleted_emails": "deleteditems/messages",
                "drafts": "drafts",
                "sent_emails": "sentitems",
            }
            for folder in search_in or []:
                if folder in endpoints and search_in[folder]:
                    endpoint = f"{folder_url}{endpoints[folder]}"
                    run_request(endpoint, params)

        else:
            filter_expression = f"""
            contains(subject,'{search_query}') or 
            contains(body/content,'{search_query}') or 
            contains(sender/emailAddress/address,'{search_query}')
            """
            params["$filter"] = filter_expression

        response = requests.get(graph_endpoint, headers=headers, params=params)
        response.raise_for_status()
        response_data: dict = response.json()
        messages = response_data.get("value", [])

        return [message["id"] for message in messages]

    except Exception as e:
        LOGGER.error(f"Failed to search emails from Microsoft API: {str(e)}")
        return []


def get_mail_to_db(social_api: SocialAPI, email_id: str) -> dict:
    """
    Retrieve email information for processing email to database.

    Args:
        social_api (SocialAPI): SocialAPI object containing authentication information.
        email_id (str): ID of the specific email message to retrieve.

    Returns:
        dict: Dictionary containing email information for processing:
            str: Subject of the email.
            tuple[str, str]: Tuple containing sender name and email address.
            str: Preprocessed email content.
            str: ID of the email message.
            datetime.datetime: Sent date and time of the email.
            bool: Flag indicating whether the email has attachments.
            bool: Flag indicating whether the email is a reply ('RE:' in subject).
    """
    url = f"{GRAPH_URL}me/mailFolders/inbox/messages"
    access_token = refresh_access_token(social_api)
    headers = get_headers(access_token)

    message_url = f"{url}/{email_id}"
    response = requests.get(message_url, headers=headers)
    message_data: dict = response.json()

    has_attachments = message_data["hasAttachments"]
    subject: str = message_data.get("subject")
    is_reply: bool = subject.lower().startswith("re:")
    sender = message_data.get("from")
    from_info = parse_name_and_email(sender)
    sent_date_str = message_data.get("sentDateTime")
    sent_date = None
    if sent_date_str:
        sent_date = datetime.datetime.strptime(sent_date_str, "%Y-%m-%dT%H:%M:%SZ")
        sent_date = make_aware(sent_date)
    decoded_data = parse_message_body(message_data)
    decoded_data_temp = email_processing.html_clear(decoded_data)
    preprocessed_data = email_processing.preprocess_email(decoded_data_temp)

    return {
        "subject": subject,
        "from_info": from_info,
        "preprocessed_data": preprocessed_data,
        "email_id": email_id,
        "sent_date": sent_date,
        "has_attachments": has_attachments,
        "is_reply": is_reply,
    }


def get_mail(access_token: str, int_mail: int = None, id_mail: str = None) -> tuple:
    """
    Retrieve email information for processing.

    Args:
        access_token (str): The access token for authenticating with the Microsoft Graph API.
        int_mail (int, optional): The zero-based index to retrieve the nth email from the inbox.
                                  If provided, this takes precedence over the `id_mail` parameter.
        id_mail (str, optional): The unique identifier of a specific email message to retrieve.
                                 Used if `int_mail` is not provided.

    Returns:
        tuple: A tuple containing the following information about the email:
            - subject (str): The subject line of the email.
            - from_info (tuple[str, str]): A tuple containing the sender's name and email address in the format (name, email).
            - decoded_data (str): The processed content of the email body, after parsing and any necessary preprocessing.
            - cc_info (list[tuple[str, str]]): A list of tuples with names and email addresses of CC (carbon copy) recipients.
            - bcc_info (list[tuple[str, str]]): A list of tuples with names and email addresses of BCC (blind carbon copy) recipients.
            - email_id (str): The unique ID of the email message.
            - sent_date (datetime.datetime): The sent date and time of the email, converted to an aware datetime object.

    Returns:
        None: If neither `int_mail` nor `id_mail` is specified, if no email is found with the provided index or ID, or if a request error occurs.
    """
    url = f"{GRAPH_URL}me/mailFolders/inbox/messages"
    headers = get_headers(access_token)

    if int_mail:
        response = requests.get(url, headers=headers)
        response_data: dict = response.json()
        messages = response_data.get("value", [])

        if not messages:
            return None

        email_id = messages[int_mail]["id"]
    elif id_mail:
        email_id = id_mail

    message_url = f"{url}/{email_id}"
    response = requests.get(message_url, headers=headers)
    message_data: dict = response.json()

    subject = message_data.get("subject")
    sender = message_data.get("from")
    from_info = parse_name_and_email(sender)
    cc_info = parse_recipients(message_data.get("ccRecipients"))
    bcc_info = parse_recipients(message_data.get("bccRecipients"))
    sent_date_str = message_data.get("sentDateTime")
    sent_date = None

    if sent_date_str:
        sent_date = datetime.datetime.strptime(sent_date_str, "%Y-%m-%dT%H:%M:%SZ")
        sent_date = make_aware(sent_date)

    for header in message_data.get("internetMessageHeaders", []):
        if header["name"] == "Date":
            sent_date = datetime.datetime.strptime(
                header["value"], "%a, %d %b %Y %H:%M:%S %z"
            )
            break

    decoded_data = parse_message_body(message_data)

    return (
        subject,
        from_info,
        decoded_data,
        cc_info,
        bcc_info,
        email_id,
        sent_date,
    )
