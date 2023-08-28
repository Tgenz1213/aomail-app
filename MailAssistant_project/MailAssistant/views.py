# Refactoring the entire code based on the changes discussed

import os.path
import base64
import re
import time
import dateutil.parser as parser
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, MailForm
from django.contrib.auth.models import User
import quopri
from email.header import decode_header
from email import message_from_bytes
from base64 import urlsafe_b64encode, urlsafe_b64decode
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from bs4 import BeautifulSoup
import datetime
import requests
from oauthlib.oauth2.rfc6749.errors import OAuth2Error
from googleapiclient.errors import HttpError
import random
import email
from email import message_from_string


# llama2
import replicate

# OpenAI - ChatGPT
import openai

# langchain
from langchain.chains import ConversationChain
from langchain.llms import HuggingFacePipeline
from langchain.memory import ConversationSummaryBufferMemory, ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import SystemMessagePromptTemplate,ChatPromptTemplate,AIMessagePromptTemplate,HumanMessagePromptTemplate
from langchain.schema import AIMessage,HumanMessage,SystemMessage

from torch import cuda, bfloat16
import torch
from transformers import StoppingCriteria, StoppingCriteriaList
import transformers

from langchain.llms import Replicate
from langchain import PromptTemplate, LLMChain

from django.db import models


openai.organization = "org-YSlFvq9rM1qPzM15jewopUUt"
# openai.api_key = "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"
openai.api_key = "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"
gpt_model = "gpt-3.5-turbo"

# os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

configuration = {
    'organization': "org-YSlFvq9rM1qPzM15jewopUUt",
    'api_key' : "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"
}
# response = openai.Engine.list()
# print(response)

GMAIL_READONLY_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'
GMAIL_SEND_SCOPE = 'https://www.googleapis.com/auth/gmail.send'
CALENDAR_READONLY_SCOPE = 'https://www.googleapis.com/auth/calendar.readonly'
CONTACT_READONLY_SCOPE = 'https://www.googleapis.com/auth/contacts.readonly'
# PROFILE_SCOPE = 'https://www.googleapis.com/auth/userinfo.email'
# PROFILE_SCOPE = 'profile'
PROFILE_SCOPE = 'https://www.googleapis.com/auth/userinfo.profile'
EMAIL_SCOPE = 'https://www.googleapis.com/auth/userinfo.email'
OPENID_SCOPE = 'openid'
OTHER_CONTACT_READONLY_SCOPE = 'https://www.googleapis.com/auth/contacts.other.readonly'


# CALENDAR_SCOPE = 'https://www.googleapis.com/auth/calendar'

# category_list = {
#     'Esaip':"Ecole d'ingénieur",
#     'Entreprenariat':"Tout ce qui est en lien avec l'entreprenariat",
#     'Subscriptions': 'Pertaining to periodic payment plans for services or products.',
#     'Miscellaneous': 'Items, topics, or subjects that do not fall under any other specific category or for which a dedicated category has not been established.'
# }
importance_list = {
    'Important': 'Items or messages that are of high priority, do not contain offers to "unsubscribe", and require immediate attention or action.',
    'Information' : 'Details that are relevant and informative but may not require immediate action. Does not contain offers to "unsubscribe".',
    'Useless': 'Items or messages that contain offers to "unsubscribe", might not be relevant to all recipients, are redundant, or do not provide any significant value.'
}

# importance_list = {
#     'Important': 'Items or messages that are of high priority and require immediate attention or action.',
#     'Information': 'General updates, data, or details that are informative but may not require immediate action.',
#     'Useless': 'Items or messages that are not relevant, redundant, or do not provide any significant value.'
# }
# importance_list = {
#     'Highly Important': {
#         'Description': 'Items or messages that are of high priority, concern the user directly, and require immediate attention or action.'
#     },
#     'Informational': {
#         'Description': 'General updates, data, or details that are informative and may concern the user but do not require immediate action.'
#     },
#     'Neutral/Unconcerned': {
#         'Description': "Items or messages that might not directly concern the user but aren't necessarily irrelevant.",
#         'Examples': [
#             'Newsletter: Regular communications, often informational or promotional, which might not concern the user directly.',
#             'Mail de démarchage commerciale: Unsolicited emails promoting products or services, not particularly targeted to the user’s interests.'
#         ]
#     },
#     'Useless/Not Concerning': {
#         'Description': 'Items or messages that do not concern the user, are not relevant, redundant, or do not provide any significant value.',
#         'Examples': [
#             'Spams: Unwanted and unsolicited emails, often with irrelevant or inappropriate content.',
#             'Mail non personnalisé qui semble être envoyé par un robot: Non-personalized emails that appear to be automated or sent by a bot.',
#             'Mail publicitaire: Generic advertising or promotional emails not tailored to the user’s preferences.'
#         ]
#     }
# }

user_description = "Enseignant chercheur au sein d'une école d'ingénieur ESAIP."

example = """Bonjour,
            [...]
            Cordialement,
            Antoine
            """

response_list = {
    'Answer Required': 'Message requires an answer.',
    'Might Require Answer': 'Message might require an answer.',
    'No Answer Required': 'No answer is required.'
}
relevance_list = {
    'Highly Relevant': 'Message is highly relevant to the recipient.',
    'Possibly Relevant': 'Message might be relevant to the recipient.',
    'Not Relevant': 'Message is not relevant to the recipient.'
}


# loading landing page
def home_page(request):
    # connection to google
    services = authenticate_service()
    subject, from_name, decoded_data = get_mail(services,0,None)

    # subject, from_name, decoded_data = extract_body_from_email(services,0,None) #doesn't work
    
    if decoded_data: decoded_data = format_mail(decoded_data)
    print("decoded_data: ",decoded_data)

    category_list = get_db_categories()
    topic, importance, answer, summary, sentence, relevance, importance_explain = gpt_langchain_response(subject,decoded_data,category_list)

    # print('topic: ',topic)
    # print('importance: ',importance)
    # print('answer: ',answer)
    # print('summary: ',summary)
    # print('sentence: ',sentence)
    # print('relevance: ',relevance)
    # print('importance_explain: ',importance_explain)
    # # print('draft: ',response)
    answer_list = ['No Answer Required: "No answer is required."','No Answer Required']
    if answer not in answer_list:
        draft = gpt_langchain_answer(subject,decoded_data)
        print('draft: ',draft)
    # search_emails("test")
    # input = "Bien reçu, je t'envoie les infos pour le BP au plus vite"
    # # subject_test = None
    # subject,new_mail = gpt_langchain_redaction(input)
    # print('subject: ',subject)
    # print('new_mail: ',new_mail)
    # get_calendar_events(services)
    input_ai = "Que recherchez-vous ?"
    input_text = "Théo Hubert m'a écrit un mail concernant un étudiant entrepreneur en juillet"
    # emails_id = search_emails(email_query(*gpt_langchain_decompose_search([input_ai,input_text])))

    query,query_list = email_query(*gpt_langchain_decompose_search([input_ai,input_text]))

    # email_list_from, email_list_to, starting_date, ending_date, key_words = gpt_langchain_decompose_search([input_ai,input_text])
    # query = email_query(email_list_from,email_list_to,starting_date,ending_date,key_words)
    emails_id = search_emails(query)
    
    # print('from_who: ',from_who)
    # print('to_who: ',to_who)
    # print('key_words: ',key_words)
    # print('starting_date: ',starting_date)
    # print('ending_date: ',ending_date)
    # print("query: ",query)
    # emails_id = search_emails(query)
    # print('emails_id: ',emails_id)
    if emails_id:
        for email_id in emails_id:
            # print('email found: ',get_mail(services,None,email_id))
            subject, from_name, decoded_data = get_mail(services,None,email_id)
            if decoded_data: decoded_data = format_mail(decoded_data)
            # print('email found: ',decoded_data)
            # print('email found: ',get_email_by_id(email_id)) #doesn't work


    # emailist = 'gmail'
    # full_emailist = get_contacts(emailist,'contacts','connections')
    # print('full_emailist: ',full_emailist)
    # full_emailist = get_contacts(emailist,'other.contacts','otherContacts')
    # print('full_emailist: ',full_emailist)

    
    return render(request, 'home_page.html', {'subject': subject,'sender': from_name, 'content': decoded_data})

# authentication service for all google services needed at once, used on startup, then stored until log out
def authenticate_service():
    SCOPES = [GMAIL_READONLY_SCOPE,GMAIL_SEND_SCOPE,CALENDAR_READONLY_SCOPE,CONTACT_READONLY_SCOPE,PROFILE_SCOPE,EMAIL_SCOPE,OPENID_SCOPE,OTHER_CONTACT_READONLY_SCOPE]
    """Authenticate and return service objects for Google APIs."""
    creds = None
    # Check if token.pickle exists and load credentials if it does
    if os.path.exists('token.pickle'):
        if os.stat("token.pickle").st_size > 0:
            with open('token.pickle', 'rb') as token:
                try:
                    creds = pickle.load(token)
                except EOFError:
                    print("EOFError: The file 'token.pickle' is empty or corrupted. Please regenerate the token.")
                    creds = None
        else:
            print("The file 'token.pickle' is empty. Please regenerate the token.")
            creds = None
    else:
        print("The file 'token.pickle' does not exist. Please generate the token.")
        creds = None

    # If there are no valid credentials, create them
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
            # try:
            #     creds = flow.run_local_server(port=8080)
            # except Warning as w:
            #     if "Scope has changed" in str(w):
            #         print("Warning: Scopes have changed. Proceeding with authentication.")
            #         auth_url, _ = flow.authorization_url(prompt='consent')
            #         print(f"Please go to this URL: {auth_url}")
            #         auth_code = input("Enter the authorization code you received: ")
            #         try:
            #             creds = flow.fetch_token(code=auth_code)
            #         except OAuth2Error as e:
            #             print(f"OAuth2Error: {e}")
            #             return None
            # except OAuth2Error as e:
            #     print(f"OAuth2Error: {e}")
            #     return None
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Build services for Gmail and Calendar based on the passed SCOPES
    service = {}
    if 'https://www.googleapis.com/auth/gmail.readonly' in SCOPES:
        service['gmail.readonly'] = build('gmail', 'v1', credentials=creds)
    if 'https://www.googleapis.com/auth/gmail.send' in SCOPES:
        service['gmail.send'] = build('gmail', 'v1', credentials=creds)
    if 'https://www.googleapis.com/auth/calendar.readonly' in SCOPES:
        service['calendar'] = build('calendar', 'v3', credentials=creds)
    if 'https://www.googleapis.com/auth/contacts.readonly' in SCOPES:
        service['contacts'] = build('people', 'v1', credentials=creds)
    # if 'https://www.googleapis.com/auth/userinfo.email' in SCOPES:
    #     service['profile'] = build('people', 'v1', credentials=creds)
    if 'https://www.googleapis.com/auth/userinfo.profile' in SCOPES:
        service['profile'] = build('people', 'v1', credentials=creds)
    if 'https://www.googleapis.com/auth/userinfo.email' in SCOPES:
        service['email'] = build('people', 'v1', credentials=creds)
    if 'https://www.googleapis.com/auth/contacts.other.readonly' in SCOPES:
        service['other.contacts'] = build('people', 'v1', credentials=creds)


    # return services
    return service


######################## Read Mails ########################

# get categories from database (no data base set)
def get_db_categories():
    # access database
    category_list = {
    'Esaip':"Ecole d'ingénieur",
    'Entreprenariat':"Tout ce qui est en lien avec l'entreprenariat",
    'Subscriptions': 'Pertaining to periodic payment plans for services or products.',
    'Miscellaneous': 'Items, topics, or subjects that do not fall under any other specific category or for which a dedicated category has not been established.'
    }
    return category_list

# Summarize and categorize an email
def gpt_langchain_response(subject,decoded_data,category_list):
    # template = (
    #     """Given the following email:

    #     Subject:
    #     {subject}

    #     Text:
    #     {text}

    #     And user description:

    #     Description:
    #     {user}

    #     Using the provided categories:

    #     Topic Categories:
    #     {category}

    #     Importance Categories:
    #     {importance}

    #     Response Categories:
    #     {answer}

    #     Relevance Categories:
    #     {relevance}

    #     1. Please categorize the email by topic, importance, response and relevance corresponding to the user description.
    #     2. In French: Summarize the following message
    #     3. In French: Provide a short sentence summarizing the email.

    #     ---

    #     Topic Categorization:
    #     - [Model's Response for Topic Category]

    #     Importance Categorization (Taking User Description into account):
    #     - [Model's Response for Importance Category]
    #     - [Model's Second Response for Importance Category]
    #     - [Model's Third Response for Importance Category]


    #     Importance Categorization Percentage:
    #     - [Model's Response for Importance Percentage]
    #     - [Model's Second Response for Importance Percentage]
    #     - [Model's Third Response for Importance Percentage]

    #     Response Categorization:
    #     - [Model's Response for Response Category]

    #     Relevance Categorization:
    #     - [Model's Response for Response Category]

    #     Résumé court en français:
    #     - [Model's One-Sentence Summary en français]

    #     Résumé en français:
    #     - [Model's Bullet Point 1 en français]
    #     - [Model's Bullet Point 2 en français]
    #     ...
    #     """
    # )
    template = (
    """Given the following email:

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

    Importance Categorization (Taking User Description into account):
    - Category 1: [Model's Response for Importance Category 1]
    - Percentage 1: [Model's Percentage for Importance Category 1]
    - Category 2: [Model's Response for Importance Category 2]
    - Percentage 2: [Model's Percentage for Importance Category 2]
    - Category 3: [Model's Response for Importance Category 3]
    - Percentage 3: [Model's Percentage for Importance Category 3]

    Response Categorization: [Model's Response for Response Category]

    Relevance Categorization: [Model's Response for Relevance Category]

    Résumé court en français: [Model's One-Sentence Summary en français]

    Résumé en français:
    - [Model's Bullet Point 1 en français]
    - [Model's Bullet Point 2 en français]
    ...
    """
    )

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])
    # get a chat completion from the formatted messages
    chat = ChatOpenAI(temperature=0,openai_api_key=openai.api_key,openai_organization=openai.organization)
    response = chat(chat_prompt.format_prompt(user=user_description,category=category_list,importance=importance_list,answer=response_list,subject=subject,text=decoded_data,relevance=relevance_list).to_messages())

    clear_response = response.content.strip()
    # # print('response: ',response)
    # # print('clear_response: ',clear_response)
    # # Extracting Topic Categorization
    # topic_category = clear_response.split("Topic Categorization:\n- ")[1].split("\n")[0]
    # # Extracting Importance/Action Categorization
    # importance_category = clear_response.split("Importance Categorization (Taking User Description into account):\n- ")[1].split("\n")[0]
    # # Extracting Importance/Action Categorization
    # importance_explanation = clear_response.split("Importance Categorization Percentage:\n- ")[1].split("\n")[0]
    # # Extracting Importance/Action Categorization
    # response_category = clear_response.split("Response Categorization:\n- ")[1].split("\n")[0]
    # # Extracting Importance/Action Categorization
    # relevance_category = clear_response.split("Relevance Categorization:\n- ")[1].split("\n")[0]
    # # Extracting one sentence summary
    # short_sentence = clear_response.split("Résumé court en français:\n- ")[1].split("\n")[0]
    # # Extracting Summary
    # summary_start = clear_response.index("Résumé en français:") + len("Résumé en français:")
    # summary_end = clear_response[summary_start:].index("\n\n") if "\n\n" in clear_response[summary_start:] else len(clear_response)
    # # Extracting Drafted Response
    # # response_start = clear_response.index("Drafted Response:") + len("Drafted Response:")
    # # drafted_response = clear_response[response_start:].strip()
    # # summary = clear_response[summary_start:summary_start+summary_end].strip().split("\n- ")[1:]
    # # summary = [line.replace("- ", "").strip() for line in clear_response[summary_start:summary_start+summary_end].strip().split("\n")]
    # summary_list = clear_response[summary_start:summary_start+summary_end].strip().split("\n")
    # summary_text = "\n".join(summary_list)

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

    # Extracting Response Categorization
    response_category = clear_response.split("Response Categorization: ")[1].split("\n")[0]

    # Extracting Relevance Categorization
    relevance_category = clear_response.split("Relevance Categorization: ")[1].split("\n")[0]

    # Extracting one sentence summary
    short_sentence = clear_response.split("Résumé court en français: ")[1].split("\n")[0]

    # Extracting Summary
    summary_start = clear_response.index("Résumé en français:") + len("Résumé en français:")
    summary_end = clear_response[summary_start:].index("\n\n") if "\n\n" in clear_response[summary_start:] else len(clear_response)
    summary_list = clear_response[summary_start:summary_start+summary_end].strip().split("\n- ")[1:]
    summary_text = "\n".join(summary_list)

    # Output results
    print("Topic Category:", topic_category)
    print("Importance Categories:", importance_categories)
    print("Importance Percentages:", importance_percentages)
    print("Response Category:", response_category)
    print("Relevance Category:", relevance_category)
    print("Short Sentence:", short_sentence)
    print("Summary Text:", summary_text)


    return topic_category,importance_categories,response_category,summary_text,short_sentence,relevance_category,importance_percentages


# uses BeautifulSoup to clear html from text
def html_clear(text):
    # Utiliser BeautifulSoup pour parser le HTML et extraire le texte
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text('\n') 
    return text

# removes greetings and sign-offs
def preprocess_email(email_content):
    # List of common greetings and sign-offs
    greetings = ["Bonjour", "Hello", "Hi", "Dear", "Salut"]
    sign_offs = ["Regards", "Sincerely", "Best regards", "Cordially", "Yours truly", "Cordialement", "Bien à vous"]
    
    # Create patterns to identify lines with greetings and sign-offs
    greeting_pattern = r"^\s*(" + "|".join(greetings) + r").*\n"
    sign_off_pattern = r"\n\s*(" + "|".join(sign_offs) + r").*$"
    
    # Remove greetings
    email_content = re.sub(greeting_pattern, "", email_content, flags=re.IGNORECASE | re.MULTILINE)
    
    # Remove sign-offs
    email_content = re.sub(sign_off_pattern, "", email_content, flags=re.IGNORECASE | re.MULTILINE)
    
    return email_content.strip()

# strips text of unnecessary spacings
def format_mail(text):
    # Delete links
    text = re.sub(r'<http[^>]+>', '', text)
    # Delete patterns like "[image: ...]"
    text = re.sub(r'\[image:[^\]]+\]', '', text)
    # Convert Windows line endings to Unix line endings
    text = text.replace('\r\n', '\n')
    # Remove spaces at the start and end of each line
    text = '\n'.join(line.strip() for line in text.split('\n'))
    # Delete multiple spaces
    text = re.sub(r' +', ' ', text)
    # Reduce multiple consecutive newlines to two newlines
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text

# checks the type of new text added and adjusts it if necessary before putting it inside text_final
def concat_text(text_final,text):
    if text_final:
        if type(text)==bytes:
            text_str = text.decode('utf-8')
        else:
            text_str = text
        text_final+=text_str
    else:
        if type(text)==bytes:
            text_str = text.decode('utf-8')
        else:
            text_str = text
        text_final=text_str
    return text_final

# if mime_type is correct, text is extracted from email body
def get_text_from_mail(mime_type,part,decoded_data_temp):
    # The email body is in the "data" of the "body" payload
    data = part['body']["data"]
    # The data is base64url encoded. We can decode it and print the email body
    data = data.replace("-","+").replace("_","/")
    decoded_data_temp = base64.b64decode(data)
    if mime_type== "text/html":
        decoded_data_temp = html_clear(decoded_data_temp)
        # print("get_text_from_mail: ",decoded_data_temp)
    return decoded_data_temp

# True/False from text input if html is present
def contains_html(text):
    if isinstance(text, bytes):
        text = text.decode('utf-8', 'ignore')
    html_patterns = [
        r'<[a-z]+>',         # Opening tags
        r'</[a-z]+>',        # Closing tags
        r'&[a-z]+;',         # HTML entities
        r'<!DOCTYPE html>'   # DOCTYPE declaration
    ]
    
    for pattern in html_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

# if email is structured in "multiparts", goes through all to get the email body
def process_part(part,plaintext_var):
    mime_type = part['mimeType']
    # print("mime_type: ",mime_type,plaintext_var[0])
    decoded_data = None

    if mime_type == "text/plain":
        decoded_data = get_text_from_mail(mime_type,part,decoded_data)
        # if decoded_data != None and decoded_data != "" and decoded_data != b'':
        if contains_html(decoded_data):
            decoded_data = get_text_from_mail('text/html',part,decoded_data.decode('utf-8'))
        # elif decoded_data and decoded_data.strip() not in ["", " ", " b'' ",b'']:
        elif decoded_data and decoded_data.strip() not in ["",b'']:
            # print('decoded_data_test: ',decoded_data,'___',decoded_data.strip())
            plaintext_var[0] = 1
        # else:
        #     decoded_data = None
    elif mime_type == "text/html" and plaintext_var[0]==0:
    # if mime_type == "text/html" or (mime_type == "text/plain" and not decoded_data):
        decoded_data = get_text_from_mail(mime_type,part,decoded_data)
    elif "multipart/" in mime_type:
        # For every subpart, call this function
        subpart_datas = {'html':None,'plain':None}
        for subpart in part['parts']:
            subpart_data = process_part(subpart,plaintext_var)
            if subpart_data:
                if plaintext_var[0]==0:
                    subpart_datas['html']=subpart_data
                else:
                    subpart_datas['plain']=subpart_data
        if subpart_datas:
            # print("subpart_datas: ",subpart_datas)
            if plaintext_var[0]==0:
                subpart_data = subpart_datas['html']
            else:
                subpart_data = subpart_datas['plain']
            
            decoded_data = concat_text(decoded_data,subpart_data)
            # deletes unwanted remnant of images ([images])
            if plaintext_var[0]==1 and decoded_data:
                decoded_data = re.sub(r'\[image[^\]]+\]\s*<\S+>','',decoded_data)
                decoded_data = re.sub(r'\[image[^\]]+\]','',decoded_data)
    # print("decoded_data_process: ",decoded_data)
    return decoded_data

# used to get mail number "int_mail" (minus one as lists starts from 0) and returns subject, expeditor and body 
def get_mail(services,int_mail,id_mail):
    service = services['gmail.readonly']
    plaintext_var = [0]
    plaintext_var[0] = 0

    if int_mail!=None:
        # Call the Gmail API to fetch INBOX
        results = service.users().messages().list(userId='me',labelIds=['INBOX']).execute()
        messages = results.get('messages', [])
        if not messages:
            print('No new messages.')
        else:
            message = messages[int_mail]
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
    # 2 lines added to make it work for id as well
    elif id_mail!=None:
        msg = service.users().messages().get(userId='me', id=id_mail).execute()
    # lines idented back to work as intended
    email_data = msg['payload']['headers']
    for values in email_data:
        name = values['name']
        if name == 'Subject':
            subject = values['value']
        if name == 'From':
            from_name = values['value']
            print("From: ", from_name)
    decoded_data=None
    if 'parts' in msg['payload']:
        for part in msg['payload']['parts']:
            decoded_data_temp = process_part(part,plaintext_var)
            if decoded_data_temp:
                decoded_data = concat_text(decoded_data,decoded_data_temp)

    # If there's no 'parts' field, the body of the email could be in the 'body' field
    elif 'body' in msg['payload']:
        data = msg['payload']['body']["data"]
        data = data.replace("-","+").replace("_","/")
        decoded_data_temp = base64.b64decode(data).decode('utf-8')
        decoded_data = html_clear(decoded_data_temp)
    preprocessed_data = preprocess_email(decoded_data)
                    
    return subject,from_name,preprocessed_data

# separate multiple mails (from a single mail) to different parts
def separate_concatenated_mails(decoded_text):
    # Using the given separator to split the mails
    separator = "________________________________"
    mails = decoded_text.split(separator)
    
    # Removing any empty strings from the list
    mails = [mail.strip() for mail in mails if mail.strip()]
    
    return mails




def raw_to_string(raw_data):
    # Decode the base64-encoded raw email
    decoded_bytes = base64.urlsafe_b64decode(raw_data.encode('ASCII'))
    # Convert the decoded bytes to a string using utf-8 encoding
    return decoded_bytes.decode('utf-8')

def extract_body_from_email(services,int_mail,id_mail):
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
# email_body = extract_body_from_email(raw_email_data)





######################## Answers to Mails ########################

# gets a template to answer in that form
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

# suggests an answer from parameters and email data
def gpt_langchain_answer(subject, decoded_data):
    template = (
        """Given the following email:

        Subject:
        {subject}

        Text:
        {text}

        Draft a {length} and appropriate {formality} response based on the subject and text of the email in French based on the following:
        {example}

        ---

        Response:
        [Model's drafted response to the email]
        """
    )    
    length = 'really short'
    formality = 'very informal'
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])
    # get a chat completion from the formatted messages
    chat = ChatOpenAI(temperature=0,openai_api_key=openai.api_key,openai_organization=openai.organization)
    response = chat(chat_prompt.format_prompt(example=example,subject=subject,text=decoded_data,length=length,formality=formality).to_messages())

    clear_response = response.content.strip()
    # print('clear_response: ',clear_response)

    return clear_response


######################## Redaction ########################

# Writes a email based on a draft
# def gpt_langchain_redaction(subject, input_data, parameters):
def gpt_langchain_redaction(input_data):
    # if (subject!=None):
    template = (
        """Given the following draft:

        {input}
        
        1. Write a subject to the email based on the draft in French
        2. Write a {length} and appropriate {formality} mail based on the draft in French.

        ---

        Subject:
        [Model's drafted subject]

        Draft:
        [Model's drafted email]
        """
    )
    length = 'really short'
    formality = 'formal'
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])
    # get a chat completion from the formatted messages
    chat = ChatOpenAI(temperature=0,openai_api_key=openai.api_key,openai_organization=openai.organization)
    text = chat(chat_prompt.format_prompt(input=input_data,length=length,formality=formality).to_messages())

    clear_text = text.content.strip()
    print('clear_text: ',clear_text)
    # if subject==None:
    # Extracting Subject
    subject_start = clear_text.index("Subject:") + len("Subject:")
    subject_end = clear_text[subject_start:].index("\n\n") if "\n\n" in clear_text[subject_start:] else len(clear_text)
    subject_list = clear_text[subject_start:subject_start+subject_end].strip().split("\n")
    subject_text = "\n".join(subject_list)
    # Extracting Email
    mail_start = clear_text.index("Draft:") + len("Draft:")
    # mail_end = clear_text[mail_start:].index("\n\n") if "\n\n" in clear_text[mail_start:] else len(clear_text)
    mail_list = clear_text[mail_start:len(clear_text)].strip().split("\n")
    mail_text = "\n".join(mail_list)
    # else:
    #     subject_text=subject
    #     mail_text=clear_text
    # return clear_text
    return subject_text,mail_text


######################## Search bar ########################

def get_email_by_id(email_id):
    services = authenticate_service()
    service = services['gmail.readonly']
    
    # Fetch the email by its ID
    # msg = service.users().messages().get(userId='me', id=email_id, format='raw').execute()
    msg = service.users().messages().get(userId='me', id=email_id, format='full').execute()
    print("msg :",msg)

    msg_raw = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
    mime_msg = email.message_from_bytes(msg_raw)

    payload = msg['payload']
    email_body = process_part(payload, 0)

    # Parsing email content based on your requirements
    email_subject = mime_msg['subject']
    email_from = mime_msg['from']

    return {
        'subject': email_subject,
        'from': email_from,
        'body': email_body
    }

def decode_email_data(data):
    byte_code = base64.urlsafe_b64decode(data)
    return byte_code.decode("utf-8")

def parse_parts(parts, from_name):
    for part in parts:
        # Check for nested parts
        if 'parts' in part:
            parse_parts(part['parts'], from_name)
        # Check for data in part
        data = part.get('data')
        if data:
            text = decode_email_data(data)
            print(f"From: {from_name}\nMessage: {text}\n")

# constructs query for searching through emails
def email_query(from_list,to_list,after,before,keywords):
    # print("_",from_list,"_")
    # print("_",to_list,"_")
    # print("_",after,"_")
    # print("_",before,"_")
    # print("_",keywords,"_")
    query = ""
    query_list = [0,0,0,0,0]
    if from_list:
        query_list[0]=1
        int_from = 0
        for email_int in range(len(from_list)):
            query+="from:"+from_list[email_int]+" "
            if int_from < len(from_list)-1:
                query+= "OR "
                int_from+=1
    if to_list:
        query_list[1]=1
        # for email in to_list:
        #     query+="from:"+email+" "
        int_to = 0
        for email_int in range(len(to_list)):
            query+="to:"+to_list[email_int]+" "
            if int_to < len(to_list)-1:
                query+= "OR "
                int_to+=1
    if after:
        query_list[2]=1
        query+='after:'+after+" "
    if before:
        query_list[3]=1
        query+='before:'+before+" "
    if keywords:
        query_list[4]=1
        query+=keywords
    # print(len(to_list))
    return query, query_list

# Search for emails
def search_emails(query):
    services = authenticate_service()
    service = services['gmail.readonly']
    # print('query: ',query)
    email_ids = []
    
    # Initial API request
    response = service.users().messages().list(userId='me', q=query).execute()
    
    while 'messages' in response:
        while 'messages' in response:
            for message in response['messages']:
                email_ids.append(message['id'])
            
            # Check if there are more pages of results
            if 'nextPageToken' in response:
                response = service.users().messages().list(userId='me', q=query, pageToken=response['nextPageToken']).execute()
            else:
                break

        # If you want to print out the IDs
        for email_id in email_ids:
            print(email_id)
        print("Number of mails: ",len(email_ids))

        return email_ids

# Function to extract value after colon for a given field
def extract_value(field,clear_text):
    start = clear_text.index(field) + len(field)
    end = clear_text[start:].index("\n") if "\n" in clear_text[start:] else len(clear_text)
    final_text = re.sub(r"\[Model's drafted .+?\]", '', clear_text[start:start+end].strip())
    final_text = re.sub(r"\[Unknown .+?\]", '', final_text.strip())
    return final_text.strip()

# from text get corresponding email addresses
def get_email_address(from_who,to_who):
    myself_list = ['me','[Your Name]']
    if from_who in myself_list:
        email_list_from = get_user_email()
    else:
        email_list_from_in = get_contacts(from_who,'contacts','connections')
        email_list_from_ext = get_contacts(from_who,'other.contacts','otherContacts')
        email_list_from = email_list_from_in+email_list_from_ext
    if to_who in myself_list:
        email_list_to = get_user_email()
    else:
        email_list_to_in = get_contacts(to_who,'contacts','connections')
        email_list_to_ext = get_contacts(to_who,'other.contacts','otherContacts')
        email_list_to = email_list_to_in+email_list_to_ext
    return email_list_from,email_list_to

# decompose text from user to key words for API (Google)
def gpt_langchain_decompose_search_old(input_data):
    today = datetime.date.today()
    template = (
    """Given the following draft:

    {input}

    And current date:

    {date}
    
    Based on the draft:
    1. Identify the sender (For example, if the text says 'John wrote to me', 'From:' should be 'John').
    2. Identify the recipient (If the draft implies it was written to the reader, fill in with 'me').
    3. Extract key details avoiding words from 'From' and 'To' fields or the word 'mail'.
    4. Determine the timing of the mail based on the provided date, and present it in the format 'yyyy-mm-dd'.

    ---

    From:
    [Model's drafted sender]

    To:
    [Model's drafted recipient]

    Key words:
    [Model's drafted key details]

    Starting date:
    [Model's drafted starting date in yyyy-mm-dd format]

    Ending date:
    [Model's drafted ending date in yyyy-mm-dd format]

    """
)
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])
    # get a chat completion from the formatted messages
    chat = ChatOpenAI(temperature=0,openai_api_key=openai.api_key,openai_organization=openai.organization)
    text = chat(chat_prompt.format_prompt(input=input_data,date=today).to_messages())

    clear_text = text.content.strip()
    # print("clear_text: ",clear_text)

    # Function to extract value after colon for a given field
    def extract_value(field):
        start = clear_text.index(field) + len(field)
        end = clear_text[start:].index("\n") if "\n" in clear_text[start:] else len(clear_text)
        final_text = re.sub(r"\[Model's drafted .+?\]",'',clear_text[start:start+end].strip())
        return final_text
    
    from_text = extract_value("From:\n")
    to_text = extract_value("To:\n")
    key_words_text = extract_value("Key words:\n")
    starting_date_text = extract_value("Starting date:\n")
    ending_date_text = extract_value("Ending date:\n")
    
    return from_text, to_text, key_words_text, starting_date_text, ending_date_text

# decompose text from user to key words for API (Google)
def gpt_langchain_decompose_search(chat_data):
    # Ensure chat_data is a list of chat messages
    if not isinstance(chat_data, list):
        raise ValueError("chat_data must be a list of chat messages")

    today = datetime.date.today()
    chat_string = '\n'.join(chat_data)  # Convert chat messages to a string

#     template = (
#     """Given the following chat:

#     {chat}

#     And current date:

#     {date}
    
#     From the chat:
#     1. Identify the sender of the mail being referred to.
#     2. Identify the recipient of the mail.
#     3. Extract key details or keywords mentioned about the mail.
#     4. Determine the starting date of the mail search range.
#     5. Determine the ending date of the mail search range.

#     ---

#     From:
#     [Model's drafted sender]

#     To:
#     [Model's drafted recipient]

#     Key words:
#     [Model's drafted key details]

#     Starting date:
#     [Model's drafted starting date in yyyy-mm-dd format]

#     Ending date:
#     [Model's drafted ending date in yyyy-mm-dd format]
#     """
# )
    template = (
    """Given the following chat:

    {chat}

    And current date:

    {date}
    
    From the chat:
    1. Identify the sender of the mail being referred to.
    2. Identify the recipient of the mail.
    3. Extract key details or keywords mentioned about the mail. These keywords should strictly relate to the content or subject of the mail and should not include names of the sender, recipient, or any date-related terms.
    4. Determine the starting date of the mail search range.
    5. Determine the ending date of the mail search range.

    ---

    From:
    [Model's drafted sender]

    To:
    [Model's drafted recipient]

    Key words (excluding sender, recipient, and date-related terms):
    [Model's drafted key details]

    Starting date:
    [Model's drafted starting date in yyyy-mm-dd format]

    Ending date:
    [Model's drafted ending date in yyyy-mm-dd format]
    """
    )

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])
    chat_completion = ChatOpenAI(temperature=0, openai_api_key=openai.api_key, openai_organization=openai.organization)
    text = chat_completion(chat_prompt.format_prompt(chat=chat_string, date=today).to_messages())

    clear_text = text.content.strip()
    print("clear_text: ",clear_text)
    
    from_text = extract_value("From:\n",clear_text)
    to_text = extract_value("To:\n",clear_text)
    key_words_text = extract_value("Key words (excluding sender, recipient, and date-related terms):\n",clear_text)
    starting_date_text = extract_value("Starting date:\n",clear_text)
    ending_date_text = extract_value("Ending date:\n",clear_text)

    from_email,to_email = get_email_address(from_text,to_text)
    
    return from_email, to_email, starting_date_text, ending_date_text, key_words_text

# gets list of contact based on name
def get_contacts_name(name):
    services = authenticate_service()
    service = services['contacts']

    # Call the People API
    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=1000,
        personFields='names,emailAddresses').execute()
    connections = results.get('connections', [])

    matching_contacts = []
    for person in connections:
        names = person.get('names', [])
        if names:
            full_name = names[0].get('displayName')
            if name.lower() in full_name.lower():
                matching_contacts.append(full_name)

    return matching_contacts

# gets list of emails based on names
def _get_contacts(name, service_name,resource_name):
    services = authenticate_service()
    service = services[service_name]
    # print("_"+name+"_")
    if name:
        # Call the People API
        if service_name=='contacts':
            results = service.people().connections().list(
                resourceName='people/me',
                pageSize=1000,
                personFields='names,emailAddresses').execute()
        else:
            results = service.otherContacts().list(
                pageSize=1000,
                readMask='names,emailAddresses').execute()
        # if resource_name == 'otherContacts':print('results: ',results)
        connections = results.get(resource_name, [])
        matching_contacts = []

        for person in connections:
            names = person.get('names', [])
            email_addresses = person.get('emailAddresses', [])
            if email_addresses:  # checking if there's an email address
                email = email_addresses[0].get('value')  # get the primary email address
                
                # If there's a display name and it matches the search, add it
                if names and name.lower() in names[0].get('displayName', '').lower():
                    full_name = names[0].get('displayName')
                    # matching_contacts.append((full_name, email))
                    matching_contacts.append(email)
                elif name.lower() in email.lower():
                    if names:
                        full_name = names[0].get('displayName')
                    else:
                        full_name = None
                    # matching_contacts.append((full_name, email))
                    matching_contacts.append(email)

        return matching_contacts
    else:
        return []

# delays retries after error 429 sync quota exceeded
def get_contacts(name,service_name,resource_name, max_retries=5):
    for attempt in range(max_retries):
        try:
            return _get_contacts(name,service_name,resource_name)
        except HttpError as e:
            if e.resp.status == 429 and attempt < max_retries - 1:
                # Exponential backoff with jitter.
                sleep_time = (2 ** attempt) + random.uniform(0, 0.1 * (2 ** attempt))
                time.sleep(sleep_time)
            else:
                raise
    return []

# gets the user's email
def get_user_email():
    services = authenticate_service()
    service = services['contacts']

    # Retrieve user's profile information
    results = service.people().get(resourceName='people/me', personFields='emailAddresses').execute()

    # Extract the email address from the response
    email_addresses = results.get('emailAddresses', [])
    if email_addresses:
        email = email_addresses[0].get('value')
    
    return [email]

# Questions asked for more details
def search_chat_reply(query_list):
    if query_list[0]==0: # from who
        assistant_question = ""
    elif query_list[1]==0: # to who
        assistant_question = ""
    elif query_list[2]==0: # start date
        assistant_question = ""
    elif query_list[3]==0: # end date
        assistant_question = ""
    elif query_list[4]==0: # key words
        assistant_question = ""
    return assistant_question

######################## Other ########################

def send_mail(request):
    # \"\"\"Handle the process of sending emails.\"\"\"
    # service = authenticate_service(GMAIL_SEND_SCOPE)
    services = authenticate_service()
    service = services['gmail.send']
    if request.method == 'POST' :
        form = MailForm(request.POST)
        if form.is_valid() :
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            to = form.cleaned_data['to']
            cc = form.cleaned_data['cc']
            bcc = form.cleaned_data['bcc']
            piece_jointe = form.cleaned_data['piece_jointe']

            multipart_message = MIMEMultipart()
            multipart_message["Subject"] = subject
            multipart_message["from"] = "me"
            multipart_message["to"] = to
            multipart_message["cc"] = cc
            multipart_message["bcc"] = bcc

            # Attach the message content to the email, regardless of whether
            # there's an attachment.
            multipart_message.attach(MIMEText(message, "plain"))

            if piece_jointe != None :
                piece_jointe = MIMEApplication(open(piece_jointe, 'rb').read())
                piece_jointe.add_header('Content-Disposition', 'attachment', filename='attachment.pdf')
                multipart_message.attach(piece_jointe)

            raw_message = urlsafe_b64encode(multipart_message.as_string().encode('UTF-8')).decode()

            body = {'raw': raw_message}

            multipart_message = service.users().messages().send(userId="me", body=body).execute()

            return redirect('MailAssistant:home_page')

    else : 
        form = MailForm()         
    return render(request, 'send_mails.html', {'form': form})

def get_calendar_events(services):
    # \"\"\"Retrieve events from Google Calendar.\"\"\"
    # service = authenticate_service(CALENDAR_READONLY_SCOPE)
    service = authenticate_service()
    service = services['calendar']
    events_result = service.events().list(calendarId='primary', maxResults=10).execute()
    events = events_result.get('items',[])
    
    for item in events:
        print('item: ',item)

def logout_user(request):
    # \"\"\"Handle user logout.\"\"\"
    logout(request)
    return redirect('MailAssistant:login_page')

def login_page(request):
    # \"\"\"Render the login page and handle user authentication.\"\"\"
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('MailAssistant:home_page')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    # \"\"\"Handle user registration.\"\"\"
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid() :
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            user = User.objects.create_user(username, email, password)
            user.save()
            return redirect('MailAssistant:login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

