import msal
import requests
import os
import pickle
from . import library
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from base64 import urlsafe_b64encode
from django.shortcuts import render, redirect
from .forms import MailForm
import random
import time
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import redirect


SCOPES = ["Mail.Read", "Mail.Send", "Calendars.Read", "Contacts.Read"]
CONFIG = json.load(open('msal_config.json', 'r'))
request_test = None

# simulate 'service' from Google API
class GraphAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json'
        }

    def get(self, endpoint):
        return requests.get(f"https://graph.microsoft.com/v1.0/{endpoint}", headers=self.headers).json()

    def post(self, endpoint, data):
        return requests.post(f"https://graph.microsoft.com/v1.0/{endpoint}", headers=self.headers, json=data).json()


######################## Authentification ########################

# authentication service for all microsoft services needed at once, used on startup, then stored until log out
def create_app():
    """Create and return a ConfidentialClientApplication."""
    return msal.ConfidentialClientApplication(
        CONFIG['client_id'], 
        authority=CONFIG['authority'], 
        client_credential=CONFIG['client_secret']
    )

def get_msal_token():
    print('get_msal_token')
    try:
        with open('msal_token.pickle', 'rb') as token_file:
            token = pickle.load(token_file)
        return token
    except (FileNotFoundError, pickle.UnpicklingError, AttributeError):
        return None

def is_user_connected():
    print('is_user_connected')
    token = get_msal_token()
    if not token:
        return False
    # Additional logic to check the validity of the token, if desired
    return True

def authenticate_service(request):
    print('authenticate_service')
    if not is_user_connected():
        # Direct the user to login view which will handle the redirection to Microsoft's authentication page.
        return login(request)
    else:
        # If the user is already connected (has a token), redirect them to the home_page.
        return redirect('MailAssistant:home_page')

def login(request):
    print('login')
    app = create_app()
    authorization_url = app.get_authorization_request_url(
        SCOPES,
        redirect_uri=request.build_absolute_uri(reverse('MailAssistant:handle_callback'))
    )
    print(request.build_absolute_uri(reverse('MailAssistant:handle_callback')))
    return HttpResponseRedirect(authorization_url)
    # return redirect(authorization_url)

def handle_callback(request):
    print('handle_callback')
    app = create_app()
    code = request.GET.get('code')
    
    if not code:
        return JsonResponse({"error": "No code provided."})

    auth_result = app.acquire_token_by_authorization_code(
        code, 
        SCOPES, 
        redirect_uri=request.build_absolute_uri(reverse('MailAssistant:handle_callback'))
    )

    if 'access_token' in auth_result:
        # Save the token to a pickle file
        with open('msal_token.pickle', 'wb') as token_file:
            pickle.dump(auth_result, token_file)

        # Store access_token in session
        request.session['access_token'] = auth_result['access_token']

        return redirect('MailAssistant:home_page')
    else:
        error_msg = str(auth_result)
        return render(request, 'error_page.html', {'error_msg': error_msg})


# def silent_authentication():
#     print('silent_authentication')
#     app = create_app()

#     token_cache = None
#     # Load token from pickle
#     with open('msal_token.pickle', 'rb') as f:
#         token_cache = pickle.load(f)

#     auth_result = app.acquire_token_silent(SCOPES, account=token_cache.get('account'))

#     return GraphAPI(auth_result['access_token'])

# def login(request):
#     print('login')
#     # authorization_base_url = f"{settings.AUTHORITY}/oauth2/v2.0/authorize"
#     # authorization_url = f"{authorization_base_url}?client_id={settings.CLIENT_ID}&redirect_uri={settings.REDIRECT_URI}&response_type=code&scope={' '.join(settings.SCOPES)}"
#     if not is_user_connected():
#         # app = create_app()
#         # # print('app: ',app)
#         # authorization_url = app.get_authorization_request_url(SCOPES)
        
#         # return HttpResponseRedirect(authorization_url)
#         callback(request)
#         # return redirect('MailAssistant:home_page')
#     else:
#         return silent_authentication()


# def callback(request):
#     print('callback')
#     code = request.GET.get('code')
#     if not code:
#         return JsonResponse({"error": "No code provided."})
#     app = create_app()
#     # token_url = f"{settings.AUTHORITY}/oauth2/v2.0/token"
#     # token_data = {
#     #     'grant_type': 'authorization_code',
#     #     'code': code,
#     #     'redirect_uri': settings.REDIRECT_URI,
#     #     'client_id': settings.CLIENT_ID,
#     #     'client_secret': settings.CLIENT_SECRET,
#     #     'scope': ' '.join(settings.SCOPES)
#     # }
#     # response = requests.post(token_url, data=token_data)
#     # token = response.json().get('access_token')
#     # Use the acquire_token_by_authorization_code method to get the token
#     result = app.acquire_token_by_authorization_code(
#         code, 
#         scopes=SCOPES,
#         redirect_uri='MailAssistant:handle_callback'
#     )
#     token = result.get('access_token')

#     if not token:
#         return JsonResponse({"error": "Error fetching token."})

#     headers = {
#         'Authorization': f'Bearer {token}',
#         'Content-Type': 'application/json'
#     }
#     response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
#     return JsonResponse(response.json())  # Display user data for example purposes.



# def authenticate_service(request):
#     global request_test
#     request_test = request
#     app = create_app()
#     authorization_url = app.get_authorization_request_url(
#         SCOPES,
#         redirect_uri=request.build_absolute_uri(reverse('MailAssistant:handle_callback'))
#     )
#     # redirect(authorization_url)
#     return HttpResponseRedirect(authorization_url)

# def handle_callback(request):
#     print('handle_callback')
#     app = create_app()
#     print('request: ',request)
#     code = request.GET.get('code')
#     auth_result = app.acquire_token_by_authorization_code(code, SCOPES, redirect_uri=request.build_absolute_uri(reverse('MailAssistant:handle_callback')))

#     # Check if the authentication was successful by looking for an access token
#     if 'access_token' in auth_result:
#         # Save the token to a pickle file
#         with open('msal_token.pickle', 'wb') as token_file:
#             pickle.dump(auth_result, token_file)

#         # Optionally, if you still want to use sessions alongside
#         request.session['token'] = auth_result
#         request.session['account'] = auth_result.get('account')

#         # Redirect to a success page
#         return redirect('MailAssistant:home_page')
#     else:
#         # Extract the full error message from the auth_result
#         error_msg = str(auth_result)
#         print('error_msg: ',error_msg)

#         # Render an error page and pass the error message as context
#         # return render(request, 'error_page.html', {'error_msg': error_msg})
    
# def handle_callback(request):
#     print('handle_callback')
#     app = create_app()
#     code = request.GET.get('code')
#     auth_result = app.acquire_token_by_authorization_code(code, SCOPES, redirect_uri=request.build_absolute_uri(reverse('MailAssistant:handle_callback')))

#     # Save the token to a pickle file
#     with open('msal_token.pickle', 'wb') as token_file:
#         pickle.dump(auth_result, token_file)

#     # Save the token (using sessions here, but could also be a database model)
#     request.session['token'] = auth_result
#     request.session['account'] = auth_result.get('account')

#     # Redirect to a success page or handle further
#     # return JsonResponse(auth_result)
#     return redirect('MailAssistant:home_page') 

# def authenticate_service():
#     app = create_app()

#     authorization_url = app.get_authorization_request_url(
#         SCOPES,
#         redirect_uri="http://localhost:9000/MailAssistant/"
#     )
#     return authorization_url

# def handle_callback(request):
#     app = create_app()

#     # Extract the code from the callback request
#     code = request.GET.get('code')
#     auth_result = app.acquire_token_by_authorization_code(code, SCOPES, redirect_uri="http://localhost:9000/MailAssistant/")

#     # Save the token
#     with open('msal_token.pickle', 'wb') as f:
#         pickle.dump({
#             'token': auth_result,
#             'account': auth_result.get('account')
#         }, f)

#     print('auth_result: ', auth_result)
#     return GraphAPI(auth_result['access_token'])


# def authenticate_service():
#     # SCOPES = [
#     #     "Mail.Read",
#     #     "Mail.Send",
#     #     "Calendars.Read",
#     #     "Contacts.Read",
#     # ]
#     SCOPES = ["https://graph.microsoft.com/.default"]

#     # ... (rest of your existing code for loading configurations, checking token cache, etc.) ...
#     # Load application configuration from a file (This should contain details like client_id, tenant_id, etc.)
#     with open('msal_config.json', 'r') as f:
#         config = json.load(f)

#     app = msal.ConfidentialClientApplication(config['client_id'], authority=config['authority'], client_credential=config['client_secret'])

#     token_cache = None
#     # Check if msal_token.pickle exists and load credentials if it does
#     if os.path.exists('msal_token.pickle'):
#         if os.stat("msal_token.pickle").st_size > 0:
#             with open('msal_token.pickle', 'rb') as token:
#                 try:
#                     token_cache = pickle.load(token)
#                 except EOFError:
#                     print("EOFError: The file 'msal_token.pickle' is empty or corrupted. Please regenerate the token.")
#                     token_cache = None
#         else:
#             print("The file 'msal_token.pickle' is empty. Please regenerate the token.")
#             token_cache = None
#     else:
#         print("The file 'msal_token.pickle' does not exist. Please generate the token.")
#         token_cache = None

#     if not token_cache:
#         # This is where things differ. ConfidentialClientApplication doesn't have 'acquire_token_interactive'.
#         # Instead, you'd use acquire_token_for_client.
#         auth_result = app.acquire_token_for_client(SCOPES)
    # else:
    #     # If token cache is available, try acquiring token silently
    #     auth_result = app.acquire_token_silent(SCOPES, account=token_cache.get('account'))
    
    # # Check if the silent auth was successful; if not, revert to acquire_token_for_client
    # if not auth_result or 'access_token' not in auth_result:
    #     auth_result = app.acquire_token_for_client(SCOPES)

    # # Save the updated token
    # with open('msal_token.pickle', 'wb') as f:
    #     pickle.dump({
    #         'token': auth_result,
    #         'account': auth_result.get('account')
    #     }, f)
    
    # # print('auth_result: ',auth_result)

    # # Instantiate the GraphAPI class with the access token and return it.
    # # graph_service = GraphAPI(auth_result['access_token'])
    # if 'access_token' in auth_result:
    #     graph_service = GraphAPI(auth_result['access_token'])
    #     return graph_service
    # # return graph_service

# def initiate_authentication():
# def authenticate_service():
#     SCOPES = ["Mail.Read", "Mail.Send", "Calendars.Read", "Contacts.Read"]
    
#     with open('msal_config.json', 'r') as f:
#         config = json.load(f)
    
#     app = msal.ConfidentialClientApplication(
#         config['client_id'], 
#         authority=config['authority'], 
#         client_credential=config['client_secret']
#     )

#     authorization_url = app.get_authorization_request_url(
#         SCOPES,
#         redirect_uri="http://localhost:9000/MailAssistant/"
#     )
#         # login_hint="OPTIONAL_USER_EMAIL"

#     # This should redirect the user to the Microsoft login page
#     return authorization_url

# def handle_callback(request):
#     SCOPES = ["Mail.Read", "Mail.Send", "Calendars.Read", "Contacts.Read"]

#     with open('msal_config.json', 'r') as f:
#         config = json.load(f)

#     app = msal.ConfidentialClientApplication(
#         config['client_id'],
#         authority=config['authority'],
#         client_credential=config['client_secret']
#     )

#     # Extract the code from the callback request
#     code = request.GET.get('code')

#     auth_result = app.acquire_token_by_authorization_code(code, SCOPES, redirect_uri="YOUR_REDIRECT_URI")

#     # Save the token
#     with open('msal_token.pickle', 'wb') as f:
#         pickle.dump({
#             'token': auth_result,
#             'account': auth_result.get('account')
#         }, f)

#     print('auth_result: ', auth_result)

#     return GraphAPI(auth_result['access_token'])

# def silent_authentication():
#     SCOPES = ["Mail.Read", "Mail.Send", "Calendars.Read", "Contacts.Read"]

#     with open('msal_config.json', 'r') as f:
#         config = json.load(f)

#     app = msal.ConfidentialClientApplication(
#         config['client_id'],
#         authority=config['authority'],
#         client_credential=config['client_secret']
#     )

#     token_cache = None
#     # ... (your code for loading the token from pickle file) ...

#     # Try acquiring token silently
#     auth_result = app.acquire_token_silent(SCOPES, account=token_cache.get('account'))

#     return GraphAPI(auth_result['access_token'])


# def authenticate_service():
#     SCOPES = [
#         "Mail.Read",
#         "Mail.Send",
#         "Calendars.Read",
#         "Contacts.Read",
#     ]
    
#     # Load application configuration from a file (This should contain details like client_id, tenant_id, etc.)
#     with open('msal_config.json', 'r') as f:
#         config = json.load(f)
    
#     app = msal.ConfidentialClientApplication(config['client_id'], authority=config['authority'], client_credential=config['client_secret'])

#     token_cache = None
#     # Check if msal_token.pickle exists and load credentials if it does
#     if os.path.exists('msal_token.pickle'):
#         if os.stat("msal_token.pickle").st_size > 0:
#             with open('msal_token.pickle', 'rb') as token:
#                 try:
#                     token_cache = pickle.load(token)
#                 except EOFError:
#                     print("EOFError: The file 'msal_token.pickle' is empty or corrupted. Please regenerate the token.")
#                     token_cache = None
#         else:
#             print("The file 'msal_token.pickle' is empty. Please regenerate the token.")
#             token_cache = None
#     else:
#         print("The file 'msal_token.pickle' does not exist. Please generate the token.")
        # token_cache = None
    # # # Attempt to load existing token cache
    # # token_cache = None
    # # if os.path.exists('msal_token.pickle'):
    # #     with open('msal_token.pickle', 'rb') as f:
    # #         token_cache = pickle.load(f)
    
    # if not token_cache:
    #     # If no cache found, authenticate interactively
    #     auth_result = app.acquire_token_interactive(SCOPES)
    # else:
    #     # If token cache is available, try acquiring token silently
    #     auth_result = app.acquire_token_silent(SCOPES, account=token_cache.get('account'))
    
    # # If authentication is unsuccessful, revert to interactive
    # if not auth_result or 'access_token' not in auth_result:
    #     auth_result = app.acquire_token_interactive(SCOPES)

    # # Save the updated token
    # with open('msal_token.pickle', 'wb') as f:
    #     pickle.dump({
    #         'token': auth_result,
    #         'account': auth_result.get('account')
    #     }, f)
    
    # print('auth_result: ',auth_result)

    # return GraphAPI(auth_result['access_token'])


######################## Read Mails ########################

# used to get mail number "int_mail" (minus one as lists starts from 0) or mail ID 'id_mail' and returns subject, expeditor and body 
# def get_mail(service, int_mail, id_mail):
#     # Fetch mail from the Microsoft Graph API
#     if int_mail is not None:
#         # Get messages from Inbox
#         results = service.get('me/mailFolders/Inbox/messages?$top=50')  # top=50 limits it to the 50 most recent emails
#         messages = results.get('value', [])
        
#         if not messages:
#             print('No new messages.')
#             return
#         else:
#             message = messages[int_mail]
#             msg = service.get(f"me/messages/{message['id']}")
#     elif id_mail is not None:
#         msg = service.get(f"me/messages/{id_mail}")

#     # Extract headers
#     subject = msg.get('subject', '')
#     from_name = msg.get('from', {}).get('emailAddress', {}).get('address', '')

#     print("From: ", from_name)

#     # Decode the body of the message
#     # Note: For simplicity, this example only handles plain text. You might need to adjust for HTML or other formats.
#     decoded_data = msg.get('body', {}).get('content', '')
    
#     preprocessed_data = library.preprocess_email(decoded_data)
    
#     return subject, from_name, preprocessed_data
def get_mail(service, int_mail=None, id_mail=None):
    if int_mail is not None:
        try:
            results = service.get('me/mailFolders/Inbox/messages?$top=50')
            print('results: ',results)
            messages = results.get('value', [])
            if not messages:
                print('No new messages.')
                return None, None, None
            else:
                message = messages[int_mail]
                msg = service.get(f"me/messages/{message['id']}")
        except Exception as e:
            print(f"Error fetching mail by index: {e}")
            return None, None, None

    elif id_mail is not None:
        try:
            msg = service.get(f"me/messages/{id_mail}")
        except Exception as e:
            print(f"Error fetching mail by ID: {e}")
            return None, None, None
    else:
        print("Either int_mail or id_mail should be provided.")
        return None, None, None

    subject = msg.get('subject', '')
    from_name = msg.get('from', {}).get('emailAddress', {}).get('address', '')
    decoded_data = msg.get('body', {}).get('content', '')
    preprocessed_data = library.preprocess_email(decoded_data)

    return subject, from_name, preprocessed_data



######################## Search bar ########################

def email_query(from_list, to_list, after, before, keywords, int_attachement):
    filters = []

    if from_list:
        from_filters = " OR ".join([f"from/emailAddress/address eq '{email}'" for email in from_list])
        filters.append(f"({from_filters})")

    if to_list:
        to_filters = " OR ".join([f"toRecipients/any(t: t/emailAddress/address eq '{email}')" for email in to_list])
        filters.append(f"({to_filters})")

    if after:
        filters.append(f"receivedDateTime ge {after}T00:00:00Z")  # Assumes date is in 'YYYY-MM-DD' format

    if before:
        filters.append(f"receivedDateTime le {before}T23:59:59Z")  # Assumes date is in 'YYYY-MM-DD' format

    # The Graph API does not have a direct query parameter for emails with attachments
    # This may need to be checked on the client side after fetching messages if necessary.

    if keywords:
        # This assumes a basic search where the keyword can be in any part of the email.
        # Graph API doesn't support full-text search directly in the filter query.
        # For a more comprehensive search, consider using Microsoft Search API or filter results on the client side.
        filters.append(f"(subject eq '{keywords}' or body/preview eq '{keywords}')")

    filter_query = " and ".join(filters)

    # query_list seems to be a way to indicate which filters were used.
    # Just translating this to work with the new filter logic.
    query_list = [
        1 if from_list else 0,
        1 if to_list else 0,
        1 if after else 0,
        1 if before else 0,
        1 if keywords else 0
    ]

    return filter_query, query_list


# Search for emails
def search_emails(query):
    service = authenticate_service(request_test)

    email_ids = []
    skip_count = 0  # To handle pagination

    while True:
        # Use the $search parameter to perform the search and $top to limit results
        # Microsoft's Graph API uses OData parameters, so $top specifies the number of results per page, 
        # and $skip can be used for pagination.
        response = service.get(f'me/messages?$search="{query}"&$top=100&$skip={skip_count}')

        if 'value' in response:
            for message in response['value']:
                email_ids.append(message['id'])

        # Check if we've received fewer results than the maximum, indicating that there may not be more results
        if len(response.get('value', [])) < 100:
            break
        else:
            skip_count += 100

    # If you want to print out the IDs
    for email_id in email_ids:
        print(email_id)
    print("Number of mails: ", len(email_ids))

    return email_ids

def get_contacts(name, max_retries=5):
    for attempt in range(max_retries):
        try:
            return _get_contacts(name)
        except Exception as e:  # You may want to narrow this down to specific exceptions
            if 'status_code' in dir(e) and e.status_code == 429 and attempt < max_retries - 1:
                # Exponential backoff with jitter.
                sleep_time = (2 ** attempt) + random.uniform(0, 0.1 * (2 ** attempt))
                time.sleep(sleep_time)
            else:
                raise
    return []

def _get_contacts(name):
    service = authenticate_service(request_test)
    
    # Fetch contacts for the user
    response = service.get(f"me/contacts?$top=1000&$filter=startswith(displayName, '{name}') or startswith(emailAddresses/any(a:a/address), '{name}')")
    
    contacts = response.get('value', [])
    matching_contacts = []

    for contact in contacts:
        email = contact.get('emailAddresses', [{}])[0].get('address')
        full_name = contact.get('displayName', None)

        # Given the $filter parameter in the API call, these names will always match, 
        # but this step can be kept for redundancy
        if name.lower() in full_name.lower() or (email and name.lower() in email.lower()):
            # matching_contacts.append((full_name, email))
            matching_contacts.append(email)
    
    return matching_contacts

def get_email_address(from_who, to_who):
    myself_list = ['me', '[Your Name]']  # Replace [Your Name] with your name

    if from_who in myself_list:
        email_list_from = get_user_email()
    else:
        email_list_from = get_contacts(from_who)

    if to_who in myself_list:
        email_list_to = get_user_email()
    else:
        email_list_to = get_contacts(to_who)

    return email_list_from, email_list_to

def get_user_email():
    service = authenticate_service()
    
    # Retrieve user's profile information from Microsoft Graph API
    user = service.get("me")
    
    email = user.get("mail")
    
    return [email]


######################## Other ########################


def send_mail(request):
    """Handle the process of sending emails."""
    service = authenticate_service(request)
    if request.method == 'POST':
        form = MailForm(request.POST, request.FILES)  # Note the addition of request.FILES
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            to = form.cleaned_data['to']
            cc = form.cleaned_data['cc']
            bcc = form.cleaned_data['bcc']
            piece_jointe = request.FILES['piece_jointe']  # Note this change

            multipart_message = MIMEMultipart()
            multipart_message["Subject"] = subject
            multipart_message["from"] = "me"  # You might need to replace this with the actual email
            multipart_message["to"] = to
            multipart_message["cc"] = cc
            multipart_message["bcc"] = bcc

            multipart_message.attach(MIMEText(message, "plain"))

            if piece_jointe:
                piece_jointe = MIMEApplication(piece_jointe.read())
                piece_jointe.add_header('Content-Disposition', 'attachment', filename='attachment.pdf')
                multipart_message.attach(piece_jointe)

            # Convert the message to a base64 encoded string
            raw_message = urlsafe_b64encode(multipart_message.as_bytes()).decode()

            # Construct the message for Graph API
            body = {
                "message": {
                    "subject": subject,
                    "body": {
                        "contentType": "HTML",
                        "content": message
                    },
                    "toRecipients": [{"emailAddress": {"address": to}}],
                    "ccRecipients": [{"emailAddress": {"address": cc}}],
                    "bccRecipients": [{"emailAddress": {"address": bcc}}],
                    "attachments": [{
                        "@odata.type": "#microsoft.graph.fileAttachment",
                        "name": "attachment.pdf",
                        "contentType": "application/pdf",
                        "contentBytes": raw_message
                    }]
                },
                "saveToSentItems": "true"
            }

            # Send the email using Graph API
            service.post('/me/sendMail', json=body)

            return redirect('MailAssistant:home_page')
    else:
        form = MailForm()
    return render(request, 'send_mails.html', {'form': form})
