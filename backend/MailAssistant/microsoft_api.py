"""
Handles authentication and HTTP requests for the Microsoft Graph API.
"""
import json
import logging
import requests
from urllib.parse import urlencode
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import redirect
from msal import ConfidentialClientApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from colorama import init, Fore
from rest_framework import status
from .serializers import EmailDataSerializer
from base64 import urlsafe_b64encode
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import SocialAPI
from requests.exceptions import HTTPError


######################## LOGGING CONFIGURATION ########################
init(autoreset=True)



######################## MICROSOFT GRAPH API PROPERTIES ########################
MAIL_READ_SCOPE = 'Mail.Read'
MAIL_SEND_SCOPE = 'Mail.Send'
CALENDAR_READ_SCOPE = 'Calendars.Read'
CONTACTS_READ_SCOPE = 'Contacts.Read'
SCOPES = [
    MAIL_READ_SCOPE,
    MAIL_SEND_SCOPE,
    CALENDAR_READ_SCOPE,
    CONTACTS_READ_SCOPE
]
CONFIG = json.load(open('creds/microsoft_creds.json', 'r'))
# PRODUCTION authority
AUTHORITY = f'https://login.microsoftonline.com/common'
# localhost authority
# AUTHORITY = f'https://login.microsoftonline.com/{CONFIG["tenant_id"]}'
GRAPH_URL = 'https://graph.microsoft.com/v1.0/'
REDIRECT_URI = 'http://localhost:8080/signup_part2'



######################## AUTHENTIFICATION ########################
def generate_auth_url(request):
    """Generate a connection URL to obtain the authorization code"""
    params = {
        'client_id': CONFIG["client_id"],
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'response_mode': 'query',
        'scope': ' '.join(SCOPES),
        'state': '0a590ac7-6a23-44b1-9237-287743818d32'
    }
    authorization_url = f'{AUTHORITY}/oauth2/v2.0/authorize?{urlencode(params)}'

    # Redirect the user to Microsoft's consent screen
    return redirect(authorization_url)

def exchange_code_for_tokens(authorization_code):
    """Returns the access token and the refresh token"""
    app = ConfidentialClientApplication(
        client_id=CONFIG["client_id"],
        client_credential=CONFIG["client_secret"],
        authority=AUTHORITY
    )
    
    result = app.acquire_token_by_authorization_code(
        authorization_code,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )    
    if result:
        return result['access_token'], result['refresh_token']
    else:
        return Response({'error': 'tokens not found'}, status=400)

######################## CREDENTIALS ########################
def get_social_api(user, email):
    """Returns the SocialAPI instance"""
    try:
        social_api = SocialAPI.objects.get(user=user, email=email)
        return social_api
    except SocialAPI.DoesNotExist:
        logging.error(f"{Fore.RED}No credentials found for user {user.username} and email {email}")
        return None

def is_token_valid(access_token):
    """Check if the access token is still valid by making a sample request"""
    sample_url = f'{GRAPH_URL}me'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(sample_url, headers=headers)
    return response.status_code == 200

def refresh_access_token(social_api):
    """Returns a valid access token"""
    access_token = social_api.access_token

    if is_token_valid(access_token):
        return access_token

    refresh_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': social_api.refresh_token,
        'client_id': CONFIG["client_id"],
        'client_secret': CONFIG["client_secret"],
        'scope': SCOPES
    }

    response = requests.post(refresh_url, data=data)
    response_data = response.json()

    # Check if the refresh was successful
    if 'access_token' in response_data:
        social_api.access_token = response_data['access_token']
        social_api.save()
        return response_data['access_token']
    else:
        return None



######################## PROFILE REQUESTS ########################
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_parsed_contacts(request) -> list:
    """Returns a list of parsed unique contacts with email types"""
    user = request.user
    email = request.headers.get('email')
    access_token = refresh_access_token(get_social_api(user, email))
    
    try:
        if access_token:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }

            # Get contacts using Microsoft Graph API
            graph_endpoint = 'https://graph.microsoft.com/v1.0/me/contacts?$select=displayName,emailAddresses'
            response = requests.get(graph_endpoint, headers=headers)

            parsed_contacts = []
            if response.status_code == 200:
                contacts = response.json().get('value', [])
                for contact in contacts:
                    names = contact.get('displayName', '')
                    emails = contact.get('emailAddresses', [])
                    if names and emails:
                        for email_info in emails:
                            email = email_info.get('address', '')
                            email_type = email_info.get('type', '')  # Get the email type if available
                            if email_type:
                                name_with_type = f"[{email_type}] {names}"
                                parsed_contacts.append({'name': name_with_type, 'email': email})
                            else:
                                parsed_contacts.append({'name': names, 'email': email})

                # Get unique sender information from Outlook
                unique_senders = get_unique_senders(access_token)
                for email, name in unique_senders.items():
                    parsed_contacts.append({'name': name, 'email': email})
                
                logging.info(f"{Fore.YELLOW}Retrieved {len(parsed_contacts)} unique contacts")
                return JsonResponse(parsed_contacts)

            else:
                error_message = response.json().get('error', {}).get('message', 'Failed to fetch contacts')
                return JsonResponse({'error': error_message}, status=response.status_code)

        else:
            return JsonResponse({'error': 'Access token not found'}, status=400)

    except Exception as e:
        logging.exception(f"{Fore.YELLOW}Error fetching contacts: {e}")
        return JsonResponse({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_info_contacts(access_token):
    """Fetch the name and the email of the contacts of the user"""
    graph_endpoint = 'https://graph.microsoft.com/v1.0/me/contacts'

    try:
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        params = {
            '$top': 1000
        }

        response = requests.get(graph_endpoint, headers=headers, params=params)
        response.raise_for_status()

        contacts = response.json().get('value', [])

        names_emails = []
        for contact in contacts:
            # Extract the name and email address of each contact
            name = contact.get('displayName')
            email_addresses = [email['address'] for email in contact.get('emailAddresses', [])]

            names_emails.append({'name': name, 'emails': email_addresses})

        return names_emails

    except HTTPError as e:
        logging.error(f"{Fore.RED}Error in Microsoft Graph API request: {str(e)}")
        return []


def get_unique_senders(access_token) -> dict:
    """Fetches unique sender information from Microsoft Graph API messages"""
    senders_info = {}

    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        limit = 50
        graph_endpoint = f'https://graph.microsoft.com/v1.0/me/messages?$select=sender&$top={limit}'
        response = requests.get(graph_endpoint, headers=headers)

        if response.status_code == 200:
            messages = response.json().get('value', [])
            for message in messages:
                sender = message.get('sender', {})
                email_address = sender.get('emailAddress', {}).get('address', '')
                name = sender.get('emailAddress', {}).get('name', '')
                senders_info[email_address] = name
        else:
            logging.error(f"{Fore.RED}Failed to fetch messages: {response.text}")

        return senders_info

    except Exception as e:
        logging.exception(f"{Fore.RED}Error fetching senders: {e}")
        return senders_info


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_image(request):
    """Returns the profile image URL of the user"""
    user = request.user
    email = request.headers.get('email')
    access_token = refresh_access_token(get_social_api(user, email))

    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        graph_endpoint = 'https://graph.microsoft.com/v1.0/me/photo/$value'
        response = requests.get(graph_endpoint, headers=headers)

        if response.status_code == 200:
            photo_url = response.url
            if photo_url:
                return Response({'profile_image_url': photo_url}, status=200)
            else:
                return Response({'error': 'Profile image URL not found in response'}, status=404)
        elif response.status_code == 404:
            return Response({'error': 'Profile image not found'}, status=404)
        else:
            logging.error(f"{Fore.RED}Failed to retrieve profile image: {response.status_code}\nReason: {response.reason}")
            return Response({'error': f"Failed to retrieve profile image: {response.reason}"}, status=404)

    except Exception as e:
        logging.exception(f"{Fore.RED}An exception occurred: {str(e)}")
        return Response({'error': f"An exception occurred: {str(e)}"}, status=500)


def get_email(access_token):
    """Returns the primary email of the user from Microsoft Graph API"""
    if not access_token:
        return Response({'error': 'Access token is missing'}, status=400)

    try:
        graph_api_endpoint = f'{GRAPH_URL}me'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(graph_api_endpoint, headers=headers)

        if response.status_code == 200:
            email_data = response.json()
            email = email_data.get('mail')
            return email
        else:
            return None
    except:
        return None
    


######################## EMAIL REQUESTS ########################
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_mails(request):
    """Returns the number of unread emails"""
    user = request.user
    email = request.headers.get('email')
    access_token = refresh_access_token(get_social_api(user, email))

    try:
        if access_token:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            unread_count = 0

            # Get unread messages using Microsoft Graph API
            graph_endpoint = 'https://graph.microsoft.com/v1.0/me/messages' # ?$count=true&$filter=isRead eq false'
            response = requests.get(graph_endpoint, headers=headers)
            
            response_json = response.json()            
            print(f'{Fore.YELLOW}RESPONSE: {response_json}')

            if response.status_code == 200:
                unread_count = response_json.get('@odata.count', 0)
                return JsonResponse({'unreadCount': unread_count}, status=200)
            else:
                error_message = response_json.get('error', {}).get('message', 'No error message')
                error_code = response_json.get('error', {}).get('code')

                if error_code == 'MailboxNotEnabledForRESTAPI':
                    print(f'{Fore.RED}The account you are using does not have a proper license to access the required endpoints')

                logging.error(f"{Fore.RED}Failed to retrieve unread count: {error_message}")
                return JsonResponse({'unreadCount': 0}, status=response.status_code)

        return JsonResponse({'unreadCount': 0}, status=400)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return JsonResponse({'unreadCount': 0}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_email(request):
    """Sends an email using the Microsoft Graph API."""  
    user = request.user
    email = request.headers.get('email')
    access_token = refresh_access_token(get_social_api(user, email))
    serializer = EmailDataSerializer(data=request.data)
    
    if serializer.is_valid():
        data = serializer.validated_data

        try:
            # Prepare email data
            subject = data['subject']
            message = data['message']
            to = data['to']
            cc = data.get('cc')
            bcc = data.get('cci')
            attachments = data.get('attachments')

            graph_endpoint = 'https://graph.microsoft.com/v1.0/me/sendMail'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }

            recipients = {'emailAddress': {'address': to}}
            if cc:
                recipients['ccRecipients'] = [{'emailAddress': {'address': cc}}]
            if bcc:
                recipients['bccRecipients'] = [{'emailAddress': {'address': bcc}}]

            body = {
                'message': {
                    'subject': subject,
                    'body': {
                        'contentType': 'HTML',
                        'content': message
                    },
                    'toRecipients': [recipients]
                }
            }

            if attachments:
                message_body = MIMEMultipart()
                message_body.attach(MIMEText(message, 'html'))

                for file_data in attachments:
                    file_name = file_data.name
                    file_content = file_data.read()
                    attachment = MIMEApplication(file_content)
                    attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
                    message_body.attach(attachment)

                encoded_message = urlsafe_b64encode(message_body.as_bytes()).decode('utf-8')
                body['message']['raw'] = encoded_message

            try:
                response = requests.post(graph_endpoint, headers=headers, json=body)
                if response.status_code == 202:
                    return JsonResponse({"message": "Email sent successfully!"}, status=202)
                else:
                    return JsonResponse({"error": "Failed to send email"}, status=response.status_code)
            except Exception as e:
                logging.exception(f"Error sending email: {e}")
                return JsonResponse({"error": str(e)}, status=500)

        except Exception as e:
            logging.exception(f"Error preparing email data: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    logging.error(f"{Fore.RED}Serializer errors: {serializer.errors}")
    return JsonResponse(serializer.errors, status=400)


def get_unique_email_senders(request):
    user = request.user
    email = request.headers.get('email')
    access_token = refresh_access_token(get_social_api(user, email))
    
    senders_info = get_unique_senders(access_token)
    contacts_info = get_info_contacts(access_token)
    # Convert contacts_info to a dictionary format
    contacts_dict = {email: contact['name'] for contact in contacts_info for email in contact['emails']}

    # Merge the two dictionaries and remove duplicates
    merged_info = {**contacts_dict, **senders_info}  # In case of duplicates, senders_info will overwrite contacts_dict

    return Response(merged_info, status=200)


def find_user_in_emails(access_token, search_query):
    messages = search_emails(access_token, search_query)

    if not messages:
        return "No matching emails found."

    return messages


def search_emails(access_token, search_query, max_results=2):
    graph_endpoint = 'https://graph.microsoft.com/v1.0/me/messages'

    try:
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        # Use $filter to achieve search functionality
        filter_expression = f"startswith(subject, '{search_query}') or startswith(body/content, '{search_query}')"
        
        params = {
            '$filter': filter_expression,
            '$top': max_results
        }

        response = requests.get(graph_endpoint, headers=headers, params=params)
        response.raise_for_status()

        messages = response.json().get('value', [])

        found_emails = {}

        for message in messages:
            sender = message.get('from', {}).get('emailAddress', {}).get('address', '')

            if sender:
                email = sender.lower()
                name = sender.split('@')[0].lower()

                # Additional filtering: Check if the sender email/name matches the search query
                if search_query.lower() in email or search_query.lower() in name:
                    if email and not any(substring in email for substring in ["noreply", "no-reply"]):
                        found_emails[email] = name

        return found_emails

    except HTTPError as e:
        logging.error(f'{Fore.RED}ERROR in Microsoft Graph API request: {str(e)}')
        return {}