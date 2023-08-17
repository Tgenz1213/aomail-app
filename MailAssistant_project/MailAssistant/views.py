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


# os.environ["REPLICATE_API_TOKEN"] = "r8_Il2lMT0sFWC4XRvcEapuQIBgjZfI4gX1lRItk" #old
os.environ["REPLICATE_API_TOKEN"] = "r8_6oXyodq8QOcv1rbSPcF2kxfcyzOcF2i3mL3AH" #new
hf_auth = "r8_6oXyodq8QOcv1rbSPcF2kxfcyzOcF2i3mL3AH"


openai.organization = "org-YSlFvq9rM1qPzM15jewopUUt"
# openai.api_key = "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"
openai.api_key = "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"
# openai.Model.list()
gpt_model = "gpt-3.5-turbo"

configuration = {
    'organization': "org-YSlFvq9rM1qPzM15jewopUUt",
    # 'api_key': os.environ[openai.api_key],
    'api_key' : "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"
}
# response = openai.Engine.list()
# print(response)

GMAIL_READONLY_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'
GMAIL_SEND_SCOPE = 'https://www.googleapis.com/auth/gmail.send'
CALENDAR_READONLY_SCOPE = 'https://www.googleapis.com/auth/calendar.readonly'
# CALENDAR_SCOPE = 'https://www.googleapis.com/auth/calendar'

# model_id = 'replicate/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1' # LLM Model

# device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'

category_list = {'To answer': 'Mails where an answer is needed','Subscriptions': 'Pertaining to periodic payment plans for services or products.', 'Miscellaneous': 'Items, topics, or subjects that do not fall under any other specific category or for which a dedicated category has not been established.'}
importance_list = {'Important': 'Items or messages that are of high priority and require immediate attention or action.','Answer Required': 'Queries or topics that specifically need a response or feedback.','Information': 'General updates, data, or details that are informative but may not require immediate action.','Useless': 'Items or messages that are not relevant, redundant, or do not provide any significant value.'}

# loading landing page
def home_page(request):
    # connection to google
    services = authenticate_service()
    subject, from_name, decoded_data = get_mail(services,0)
    if decoded_data: decoded_data = format_mail(decoded_data)
    # print("decoded_data: ",decoded_data)

    # # chain = llama_langchain_chain(0.75,1,500,1)
    # chain = llama_langchain_chain(0.6,0.9,300,1.2)
    # translation = llama_langchain_translation(0.6,0.9,300,1.2)
    # # response = llama_langchain_response(chain,"Summarize the following: "+decoded_data)
    # response = llama_langchain_response(chain,decoded_data)
    # print(response)
    # translated_response = llama_langchain_response(translation,response)
    # prompt = "Summarize with bullets points in French the following email. Key parts only: "
    topic, importance, summary = gpt_langchain_response(decoded_data,category_list)

    print('topic: ',topic)
    print('importance: ',importance)
    print('summary: ',summary)
    # get_calendar_events(services)
    return render(request, 'home_page.html', {'subject': subject,'sender': from_name, 'content': decoded_data})

# authentication service for all google services needed at once, used on startup, then stored until log out
def authenticate_service():
    SCOPES = [GMAIL_READONLY_SCOPE,GMAIL_SEND_SCOPE,CALENDAR_READONLY_SCOPE]
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

    # return services
    return service


######################## Llama 2 requests ########################

# def llama_langchain_chain(pre_prompt,prompt_input,temperature,top_p,max_length,repetition_penalty):
# creation of chain used to work with llama2
def llama_langchain_chain(temperature,top_p,max_length,repetition_penalty):
    # # small emails
    # DEFAULT_TEMPLATE = """<s>[INST]<<SYS>>
    # You are an advanced assistant that excels at summarizing email in French. You are to never greet me.
    # <</SYS>>
    # Provide a concise summary of the following email in French : {input} [/INST]"""


    # DEFAULT_TEMPLATE = """<s>[INST]<<SYS>>
    # You are an advanced assistant that excels at summarizing email. You only answer in French. You are to never greet me.
    # <</SYS>>
    # Write a concise summary of the following email with bullet points on key parts. Traduce it and only give the traduction: {input} [/INST]"""
    
    DEFAULT_TEMPLATE = """<s>[INST]<<SYS>>
    You are an advanced assistant that excels at summarizing email. You are to never greet me.
    <</SYS>>
    Write a concise summary of the following email with bullet points on key parts: {input} [/INST]"""

    PROMPT = PromptTemplate(input_variables=["input"], template=DEFAULT_TEMPLATE)
    llm = Replicate(model=model_id,streaming=True,input={"temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":repetition_penalty})

    chain = LLMChain(llm=llm, prompt=PROMPT)
    return chain

# asking llama2 about summarising email and getting a summary
def llama_langchain_response(chain,prompt_input):
    response = chain.predict(input=prompt_input)
    return response

# asking llama2 about translating summary and getting translation
def llama_langchain_translation(temperature,top_p,max_length,repetition_penalty):
    DEFAULT_TEMPLATE = """<s>[INST]<<SYS>>
    You are an advanced assistant that excels in translation. You are to never greet me.
    <</SYS>>
    Translate the following in French while keeping the bullet points format: {input} [/INST]"""

    PROMPT = PromptTemplate(input_variables=["input"], template=DEFAULT_TEMPLATE)
    llm = Replicate(model=model_id,streaming=True,input={"temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":repetition_penalty})

    chain = LLMChain(llm=llm, prompt=PROMPT)
    return chain

# asking llama2 to categorize email by category and importance
def llama_langchain_sorting(temperature,top_p,max_length,repetition_penalty):
    DEFAULT_TEMPLATE = """<s>[INST]<<SYS>>
    You are an advanced assistant that excels in translation. You are to never greet me.
    <</SYS>>
    Translate the following in French while keeping the bullet points format: {input} [/INST]"""

    PROMPT = PromptTemplate(input_variables=["input"], template=DEFAULT_TEMPLATE)
    llm = Replicate(model=model_id,streaming=True,input={"temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":repetition_penalty})

    chain = LLMChain(llm=llm, prompt=PROMPT)
    return chain


######################## ChatGPT requests ########################

def chatgpt(pre_prompt,prompt_mail):
    response = openai.Completion.create(
        model=gpt_model,
        # messages=[
        #     {"role": "system", "content": "You are the best in all you do."},
        #     {"role": "user", "content": pre_prompt+"["+prompt_mail+"]"}
        # ])
        prompt=pre_prompt+"["+prompt_mail+"]")
    # return response.choices[0].text.strip()
    return response.choices[0].message['content'].strip()

# def gpt_langchain_response(prompt,decoded_data):
#     template = (
#         # "You are a helpful assistant that translates {input_language} to {output_language}."
#         "You're the best in all you do."
#     )
#     system_message_prompt = SystemMessagePromptTemplate.from_template(template)
#     human_template = "{text}"
#     human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
#     chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
#     # get a chat completion from the formatted messages
#     chat = ChatOpenAI(temperature=0,openai_api_key=openai.api_key,openai_organization=openai.organization)
#     response = chat(chat_prompt.format_prompt(text=prompt+decoded_data).to_messages())

#     return response.content.strip()


def gpt_langchain_response(decoded_data,category_list):
    # prompt = "Summarize with bullets points in French the following email. Key parts only: "
    template = (
        """Given the following topic categories and their descriptions:
        {category}
        And the following importance/action categories:
        {importance}

        Please categorize and summarize the following message:

        {text}

        Topic Categorization:
        - [Model's Response for Topic Category]

        Importance/Action Categorization:
        - [Model's Response for Importance/Action Category]

        Summary:
        - [Model's Bullet Point 1]
        - [Model's Bullet Point 2]
        ..."""

    )
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    # human_template = "{text}"
    # human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    # chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])
    # get a chat completion from the formatted messages
    chat = ChatOpenAI(temperature=0,openai_api_key=openai.api_key,openai_organization=openai.organization)
    response = chat(chat_prompt.format_prompt(category=category_list,importance=importance_list,text=decoded_data).to_messages())

    clear_response = response.content.strip()
    # print('response: ',response)
    # print('clear_response: ',clear_response)
    # Extracting Topic Categorization
    topic_category = clear_response.split("Topic Categorization:\n- ")[1].split("\n")[0]
    # Extracting Importance/Action Categorization
    importance_category = clear_response.split("Importance/Action Categorization:\n- ")[1].split("\n")[0]
    # Extracting Summary
    summary_start = clear_response.index("Summary:") + len("Summary:")
    summary_end = clear_response[summary_start:].index("\n\n") if "\n\n" in clear_response[summary_start:] else len(clear_response)
    # summary = clear_response[summary_start:summary_start+summary_end].strip().split("\n- ")[1:]
    # summary = [line.replace("- ", "").strip() for line in clear_response[summary_start:summary_start+summary_end].strip().split("\n")]
    summary_list = clear_response[summary_start:summary_start+summary_end].strip().split("\n")
    summary_text = "\n".join(summary_list)

    return topic_category,importance_category,summary_text



######################## Read Mails ########################

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
    # Delete multiple spaces
    text = re.sub(r' +', ' ', text)
    # Convert Windows line endings to Unix line endings
    text = text.replace('\r\n', '\n')
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
        # Utiliser BeautifulSoup pour parser le HTML et extraire le texte
        soup = BeautifulSoup(decoded_data_temp, "html.parser")
        text = soup.get_text('\n') 
        # print("HTML content: ", text)
        decoded_data_temp = text
        # print("get_text_from_mail: ",decoded_data_temp)
    return decoded_data_temp

# if email is structured in "multiparts", goes through all to get the email body
def process_part(part,plaintext_var):
    mime_type = part['mimeType']
    # print("mime_type: ",mime_type,plaintext_var[0])
    decoded_data = None

    if mime_type == "text/plain":
        decoded_data = get_text_from_mail(mime_type,part,decoded_data)
        if decoded_data != None and decoded_data != "" and decoded_data != b'':
            plaintext_var[0] = 1
    elif mime_type == "text/html" and plaintext_var[0]==0:
        decoded_data = get_text_from_mail(mime_type,part,decoded_data)
    elif "multipart/" in mime_type:
        # FOr every subpart, call this function
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
def get_mail(services,int_mail):
    # \"\"\"Render the home page and interact with emails.\"\"\"
    # service = authenticate_service(GMAIL_READONLY_SCOPE)
    # service = authenticate_service()
    service = services['gmail.readonly']
    plaintext_var = [0]
    plaintext_var[0] = 0

    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me',labelIds=['INBOX']).execute()
    messages = results.get('messages', [])
    if not messages:
        print('No new messages.')
    else:
        message = messages[int_mail]
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
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
            # Utiliser BeautifulSoup pour parser le HTML et extraire le texte
            soup = BeautifulSoup(decoded_data_temp, "html.parser")
            text = soup.get_text('\n') 
            decoded_data = text
        # print("decoded_data: ",decoded_data)
        preprocessed_data = preprocess_email(decoded_data)
        # print('plaintext_var',plaintext_var)
        # pre_prompt = "You are to summarize the following as an assistant would do. No more, no less. No questions asked. No need to say 'Hello!'."
        # pre_prompt = "Provide a concise summary of this mail without providing help."
        # pre_prompt = "Donne un résumé concis de ce mail sans proposer d'aide."
        # pre_prompt = "Résumé concis du texte suivant:"
        # prompt_input = decoded_data
        # int_test = 0
        # summarized_data = llama2_replicate(pre_prompt,prompt_input,0.1,0.5,128,1)
        # print(summarized_data)
                    
    return subject,from_name,preprocessed_data

# separate multiple mails (from a single mail) to different parts
def separate_concatenated_mails(decoded_text):
    # Using the given separator to split the mails
    separator = "________________________________"
    mails = decoded_text.split(separator)
    
    # Removing any empty strings from the list
    mails = [mail.strip() for mail in mails if mail.strip()]
    
    return mails

######################## Answers to Mails ########################

# gets a template for llama 2 to answer in that form
def get_answer_template(mail_size):
    # samples for Llama 2 to get work done as intended
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

