"""Azure AD connections and Outlook API calls

TODO Upgrade the licence
{'error': {'code': 'MailboxNotEnabledForRESTAPI', 'message': 'The mailbox is either inactive, soft-deleted, or is hosted on-premise.'}}
"""
import json
import logging
from urllib.parse import urlencode
from urllib.parse import urlparse, parse_qs
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from requests import post, get
from msal import ConfidentialClientApplication
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import logging
from colorama import init, Fore


# Initialize colorama with autoreset
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
AUTHORITY = f'https://login.microsoftonline.com/{CONFIG["tenant_id"]}'
GRAPH_URL = 'https://graph.microsoft.com/v1.0/'
REDIRECT_URI = 'https://localhost:9000/MailAssistant/microsoft/auth_callback/'
# https://localhost:9000/MailAssistant/microsoft/auth_url/



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
    auth_url = f'{AUTHORITY}/oauth2/v2.0/authorize?{urlencode(params)}'
    return redirect(auth_url)

def auth_callback(request):
    """Retrieve the authorization code from the callback response"""
    parsed_url = urlparse(request.build_absolute_uri())
    query_params = parse_qs(parsed_url.query)
    authorization_code = query_params.get('code', [''])[0]

    if authorization_code:
        tokens = exchange_code_for_tokens(authorization_code)
        access_token = tokens['access_token']        
        refresh_token = tokens['refresh_token']


        # TODO: Save tokens in DB
        
        if access_token:
            # testing access token
            print(get_mails(access_token))


            return HttpResponseRedirect('http://localhost:8080/')
        else:
            return JsonResponse({'error': 'Failed to obtain access token'}, status=400)
    else:
        return JsonResponse({'error': 'Code not found'}, status=400)

def exchange_code_for_tokens(authorization_code):
    """Returns the access token"""
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
        return result
    else:
        return JsonResponse({'error': 'Access token not found'}, status=400)


######################## MICROSOFT GRAPH API REQUESTS ########################
def get_perso_info(access_token):
    """Returns several public informations about the profile"""

    # Define the Microsoft Graph API endpoint for reading emails
    graph_api_endpoint = f'{GRAPH_URL}me'

    # Set the headers with the access token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Make a GET request to the API endpoint
    response = get(graph_api_endpoint, headers=headers)

    if response.status_code == 200:
        # The response contains your email data
        email_data = response.json()
        return email_data
    else:
        # Handle the error case
        logging.error(f'{Fore.RED}Error reading emails. Status code: {response.status_code}')
        return None

#https://localhost:9000/MailAssistant/microsoft/auth_url/

def get_mails(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = get(f'{GRAPH_URL}me/contacts', headers=headers)
    print(response.reason, response.json())

    if response.status_code == 200:
        email_data = response.json()
        for email in email_data.get('value', []):
            # Process the email data as needed
            subject = email.get('subject', '')
            sender = email.get('from', {}).get('emailAddress', {}).get('address', '')
            print(f'Subject: {subject}, Sender: {sender}')
    else:
        print('\n\nERROR')
        print(f'Error reading emails. Status code: {response.status_code}')

def send_mail(access_token, subject, message, to, cc=None, bcc=None, attachment=None):
    # Set up the headers with the access token for authentication
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Construct the email
    multipart_message = MIMEMultipart()
    multipart_message["Subject"] = subject
    multipart_message["To"] = to
    if cc:
        multipart_message["Cc"] = cc
    if bcc:
        multipart_message["Bcc"] = bcc

    multipart_message.attach(MIMEText(message, "plain"))

    if attachment:
        attached_file = MIMEApplication(attachment.read())
        attached_file.add_header('Content-Disposition', 'attachment', filename='attachment.pdf')
        multipart_message.attach(attached_file)

    # Send the email using Outlook API
    endpoint = f"{GRAPH_URL}me/sendMail"  # Replace with the correct API endpoint
    response = requests.post(endpoint, headers=headers, json={
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": message
            },
            "toRecipients": [{"emailAddress": {"address": to}}],
            "ccRecipients": [{"emailAddress": {"address": cc}}] if cc else [],
            "bccRecipients": [{"emailAddress": {"address": bcc}}] if bcc else [],
        }
    })

    if response.status_code == 202:
        return True
    else:
        # Log the error
        logging.error('Failed to send email: %s', response.text)
        return False