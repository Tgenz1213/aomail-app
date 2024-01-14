"""
Handles frontend requests and redirects them to the appropriate API.
"""
import base64
import re
import logging
import json
from colorama import Fore, init
import jwt
from rest_framework_simplejwt.settings import api_settings
#### FOR AUTH TO THE API
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate, logout
from django.shortcuts import redirect, get_object_or_404
####

from django.contrib.auth.models import User
import datetime
from email import message_from_string
from collections import defaultdict

# THEO IMPORT For API and test Postgres
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .models import Message, Category, SocialAPI, Email, BulletPoint, Rule, Preference, Sender
from .serializers import MessageSerializer, CategoryNameSerializer, EmailReadUpdateSerializer, EmailReplyLaterUpdateSerializer, RuleBlockUpdateSerializer, EmailDataSerializer, PreferencesSerializer, UserLoginSerializer, RuleSerializer, SenderSerializer, NewEmailAISerializer, EmailAIRecommendationsSerializer, EmailCorrectionSerializer, EmailCopyWritingSerializer, EmailProposalAnswerSerializer, EmailGenerateAnswer, NewCategorySerializer
from django.db import IntegrityError

from MailAssistant import google_api, microsoft_api
from MailAssistant import gpt_4
from MailAssistant import gpt_3_5_turbo
from django.http import JsonResponse

# OpenAI - ChatGPT
import openai

# langchain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import SystemMessagePromptTemplate,ChatPromptTemplate


# Initialize colorama with autoreset
init(autoreset=True)
# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


openai.organization = "org-YSlFvq9rM1qPzM15jewopUUt"
openai.api_key = "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"
gpt_model = "gpt-3.5-turbo"

importance_list = {
    'Important': 'Items or messages that are of high priority, do not contain offers to "unsubscribe", and require immediate attention or action.',
    'Information' : 'Details that are relevant and informative but may not require immediate action. Does not contain offers to "unsubscribe".',
    'Useless': 'Items or messages that contain offers to "unsubscribe", might not be relevant to all recipients, are redundant, or do not provide any significant value.'
}
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

api_list = [google_api,microsoft_api]
api_var = 0



######################## Read Mails ########################

# # get categories from database (no data base set)
# def get_db_categories():
#     # access database
#     category_list = {
#     'Esaip':"Ecole d'ingénieur",
#     'Entreprenariat':"Tout ce qui est en lien avec l'entreprenariat",
#     'Subscriptions': 'Pertaining to periodic payment plans for services or products.',
#     'Miscellaneous': 'Items, topics, or subjects that do not fall under any other specific category or for which a dedicated category has not been established.'
#     }
#     return category_list

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

def processed_email_to_bdd(request, services):
    subject, from_name, decoded_data, email_id = api_list[api_var].get_mail(services, 0, None) #microsoft non fonctionnel

    if not Email.objects.filter(provider_id=email_id).exists():

        # Check if data is decoded, then format it
        if decoded_data:
            decoded_data = format_mail(decoded_data)

        # Get user categories
        category_list = get_db_categories(request.user)

        # Process the email data with AI/NLP
        topic, importance, answer, summary, sentence, relevance, importance_explain = gpt_langchain_response(subject, decoded_data, category_list)

        sender_name, sender_email = separate_name_email(from_name)

        # Fetch or create the sender
        sender, created = Sender.objects.get_or_create(name=sender_name, email=sender_email)  # assuming from_name contains the sender's name

        # Get the relevant category based on topic or create a new one (for simplicity, I'm getting an existing category)
        category = Category.objects.get_or_create(name=topic, user=request.user)[0]

        provider_list = ['Gmail','Outlook']
        provider = provider_list[api_var]

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
                user=request.user
            )

            # If the email has a summary, save it in the BulletPoint table
            if summary:
                # Split summary by line breaks
                lines = summary.split("\n")
                
                # Filter lines that start with '- ' which indicates a bullet point
                bullet_points = [line[2:].strip() for line in lines if line.strip().startswith("- ")]

                for point in bullet_points:
                    BulletPoint.objects.create(content=point, email=email_entry)
        except IntegrityError:
            print(f"An error occurred when trying to create an email with provider_id {email_id}. It might already exist.")

        # Debug prints
        print('topic:', topic)
        print('importance:', importance)
        print('answer:', answer)
        print('summary:', summary)
        print('sentence:', sentence)
        print('relevance:', relevance)
        print('importance_explain:', importance_explain)
    
    else:
        print(f"Email with provider_id {email_id} already exists.")

    # return email_entry  # Return the created email object, if needed
    return


def fill_lists(categories, percentages):
    base_categories = ['Important', 'Information', 'Useless']
    
    # Determine which category is in the list
    first_category = categories[0]

    # Remove the category found from the base list
    base_categories.remove(first_category)

    # Construct the new categories list based on the first category
    for i in range(1, 3):
        if not categories[i]:
            categories[i] = base_categories.pop(0)
            percentages[i] = '0%'

    return categories, percentages

# Summarize and categorize an email
def gpt_langchain_response(subject,decoded_data,category_list):
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
    )

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])
    # get a chat completion from the formatted messages
    chat = ChatOpenAI(temperature=0,openai_api_key=openai.api_key,openai_organization=openai.organization)
    response = chat(chat_prompt.format_prompt(user=user_description,category=category_list,importance=importance_list,answer=response_list,subject=subject,text=decoded_data,relevance=relevance_list).to_messages())

    clear_response = response.content.strip()
    print("full response: ",clear_response)

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
    
    importance_categories,importance_percentages = fill_lists(importance_categories,importance_percentages)

    # Extracting Response Categorization
    response_category = clear_response.split("Response Categorization: ")[1].split("\n")[0]

    # Extracting Relevance Categorization
    relevance_category = clear_response.split("Relevance Categorization: ")[1].split("\n")[0]

    # Extracting one sentence summary
    short_sentence = clear_response.split("Résumé court en français: ")[1].split("\n")[0]

    # # Extracting Summary
    # summary_start = clear_response.index("Résumé en français:") + len("Résumé en français:")
    # summary_end = clear_response[summary_start:].index("\n\n") if "\n\n" in clear_response[summary_start:] else len(clear_response)
    # summary_list = clear_response[summary_start:summary_start+summary_end].strip().split("\n- ")[1:]
    # summary_text = "\n".join(summary_list)

    # Finding start of the summary
    summary_start = clear_response.find("Résumé en français:") + len("Résumé en français:")

    # Finding the end of the summary
    summary_end = clear_response.find("\n\n", summary_start)
    if summary_end == -1:  # If there's no double newline after the start, consider till the end of the string
        summary_end = len(clear_response)

    # Extracting the summary
    summary_text = clear_response[summary_start:summary_end].strip()
    # if summary_text.startswith("- "):  # Remove any leading "- " from the extracted text
    #     summary_text = summary_text[2:].strip()

    # Output results
    # print("Topic Category:", topic_category)
    # print("Importance Categories:", importance_categories)
    # print("Importance Percentages:", importance_percentages)
    # print("Response Category:", response_category)
    # print("Relevance Category:", relevance_category)
    # print("Short Sentence:", short_sentence)
    # print("Summary Text:", summary_text)


    return topic_category,importance_categories,response_category,summary_text,short_sentence,relevance_category,importance_percentages

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



######################## Search bar ########################

# decode using 'utf-8'
def decode_email_data(data):
    byte_code = base64.urlsafe_b64decode(data)
    return byte_code.decode("utf-8")

# goes through parts
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

# Function to extract value after colon for a given field
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
    return final_text.strip()

# Function to extract value after colon for a given field
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
    return final_text.strip()

# decompose text from user to key words for API (Google)
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
    
    return from_email, to_email, starting_date_text, ending_date_text, key_words_text

# Questions asked for more details
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
    return assistant_question



######################## REGISTRATION ########################
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """REGISTER USER IN mailassistandb and handles the callback of the API with Oauth2.0

    APIs taken into account:
        - Gmail API (Google)
        - Graph API (Microsoft)
    """
    # Extract user data from the request
    type_api = request.data.get('type_api')
    code = request.data.get('code')
    username = request.data.get('login')
    password = request.data.get('password')
    theme = request.data.get('theme')
    color = request.data.get('color')
    categories = request.data.get('categories')

    if not code:
        return Response({'error': 'No authorization code provided'}, status=404)    
    
    # Check if user requirements
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)
    elif " " in username:
        return Response({'error': 'Username must not contain spaces'}, status=400)
    
    # Checks passwords requirements
    if not (8 <= len(password) <= 32):
        return Response({'error': 'Password length must be between 8 and 32 characters'}, status=400)
    if " " in password:
        return Response({'error': 'Password must not contain spaces'}, status=400)
    elif not re.match(r'^[a-zA-Z0-9!@#$%^&*()-=_+]+$', password):
        return Response({'error': 'Password contains invalid characters'}, status=400)

    # Checks if the authorization code is valid
    if type_api == "google":
        # callback for Google API
        try:
            access_token, refresh_token = google_api.exchange_code_for_tokens(code)
            # print(f"{Fore.CYAN}[GOOGLE]\n{Fore.GREEN}TOKENS RETRIEVED FROM BACKEND: \n{Fore.LIGHTGREEN_EX}Access token: {Fore.YELLOW}{access_token} \n{Fore.LIGHTGREEN_EX}Refresh token: {Fore.YELLOW}{refresh_token}")            
            email = google_api.get_email(access_token, refresh_token)
        except Exception as e:
            return Response({'error': e}, status=400)
        
    elif type_api == "microsoft":
        # callback for Microsoft API
        try:
            access_token, refresh_token = microsoft_api.exchange_code_for_tokens(code)
            # print(f"{Fore.CYAN}[MICROSOFT]\n{Fore.GREEN}TOKENS RETRIEVED FROM BACKEND: \n{Fore.LIGHTGREEN_EX}Access token: {Fore.YELLOW}{access_token} \n{Fore.LIGHTGREEN_EX}Refresh token: {Fore.YELLOW}{refresh_token}")
            email = microsoft_api.get_email(access_token)
            # TODO: check if its constant
            # Access  token len: 2416
            # Refresh token len: 1530
        except Exception as e:
            return Response({'error': e}, status=400)
        
    # Check email requirements
    if email:
        if SocialAPI.objects.filter(email=email).exists():
            return Response({'error': 'Email address already used'}, status=400)
        elif " " in email:
            return Response({'error': 'Email address must not contain spaces'}, status=400)
    else:
        return Response({'error': 'Failed to get the email'}, status=400)

    # Create and save user
    user = User.objects.create_user(username, '', password)
    user_id = user.id
    refresh = RefreshToken.for_user(user)
    jwt_access_token = str(refresh.access_token)
    user.save()

    # Save socialAPI
    social_api = SocialAPI(
        user=user,
        type_api=type_api,
        email=email,
        access_token=access_token,
        refresh_token=refresh_token
    )
    social_api.save()

    # Save user preferences
    preference = Preference(
        theme=theme,
        bg_color=color,
        user=user
    )
    preference.save()

    # Save user categories
    if categories:
        try:
            categories_j = json.loads(categories)
            for category_data in categories_j:
                category_name = category_data.get('name')
                category_description = category_data.get('description')

                category = Category(
                    name=category_name,
                    description=category_description,
                    user=user
                )
                category.save()
        except json.JSONDecodeError:
            return Response({'error': 'Invalid categories data'}, status=404)

    return Response({'user_id': user_id, 'access_token': jwt_access_token, 'email': email}, status=201)



######################## CREDENTIALS AVAILABILITY ########################
@api_view(['GET'])
@permission_classes([AllowAny])
def check_username(request):
    """Verify if the username is available"""
    username = request.headers.get("username")
    
    if User.objects.filter(username=username).exists():
        return Response({'available': False}, status=200)
    else:
        return Response({'available': True}, status=200)



######################## ENDPOINTS HANDLING GMAIL & OUTLOOK ########################
#----------------------- GET REQUESTS -----------------------#
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_mails(request):
    """Returns the number of unread emails"""
    return forward_request(request._request, 'unread_mails')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_image(request):
    """Returns the profile image of the user"""
    return forward_request(request._request, 'get_profile_image')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_parsed_contacts(request):
    """Returns a list of parsed unique contacts"""
    return forward_request(request._request, 'get_parsed_contacts')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unique_email_senders_view(request):
    """Fetches unique email senders' information, combining data from user's contacts and email senders."""
    return forward_request(request._request, 'get_unique_email_senders')


#----------------------- POST REQUESTS -----------------------#
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_email(request):
    return forward_request(request._request, 'send_email')  


def forward_request(request, api_method):
    """Forwards the request to the appropriate API method based on type_api"""
    user = request.user
    email = request.headers.get('email')

    try:
        social_api = get_object_or_404(SocialAPI, user=user, email=email)
        type_api = social_api.type_api
    except SocialAPI.DoesNotExist:
        return JsonResponse({'error': 'SocialAPI entry not found for the user and email'}, status=404)

    api_module = None
    if type_api == 'google':
        api_module = google_api
    elif type_api == 'microsoft':
        api_module = microsoft_api

    if api_module and hasattr(api_module, api_method):
        # Call the specified API method dynamically
        api_function = getattr(api_module, api_method)
        # Forward the request and return the response
        return api_function(request)
    else:
        return JsonResponse({'error': 'Unsupported API type or method'}, status=400)



######################## ACCOUNT ########################
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    """Removes the user from the database"""
    user = request.user 

    try:
        user.delete()
        logging.info(f"{Fore.YELLOW}The user {user} has been removed from the database")
        # TODO: Success message for user
        return Response({'message': 'User successfully deleted'}, status=200)

    except Exception as e:
        logging.error(f"{Fore.RED}Error occurred while deleting user: {e}")
        # TODO: Handle deletion failure
        return Response({'error': 'Failed to delete user'}, status=500)



# THEO API TEST
@api_view(['GET'])
@permission_classes([AllowAny])
def get_message(request):
    message = Message.objects.first()  # Just getting the first message for simplicity.
    serializer = MessageSerializer(message)
    return Response(serializer.data)


def logout_user(request):
    # \"\"\"Handle user logout.\"\"\"
    logout(request)
    return redirect('MailAssistant:login')

######################## AUTHENTICATION API ########################
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Authentication Django Rest API"""
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Return the access token directly in the response
        return Response({'access_token': access_token, 'message': 'Login successful'})
    
    return Response({'error': 'Invalid Credentials'}, status=400) 


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    """Refreshes the JWT access token"""
    raw_token = request.data.get('access_token')
    if not raw_token:
        return Response({'error': 'Access token is missing'}, status=400)

    try:
        # Decode the token without checking for expiration
        decoded_data = jwt.decode(
            raw_token, 
            api_settings.SIGNING_KEY, 
            algorithms=[api_settings.ALGORITHM],
            options={"verify_exp": False}
        )
        user = User.objects.get(id=decoded_data['user_id'])

        # Issue a new access token
        new_access_token = str(RefreshToken.for_user(user).access_token)

        return Response({'access_token': new_access_token})

    except Exception as e:
        # Handle exceptions
        print(f'{Fore.RED}Error while refreshing the JWT token: {e}')
        return Response({'error': e}, status=400)



######################## CATEGORIES ########################
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_categories(request):
    username = request.user.username
    
    try:
        current_user = User.objects.get(username=username)
        categories = Category.objects.filter(user=current_user)
        serializer = CategoryNameSerializer(categories, many=True)
        print("DATA --------------->", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_category(request, currentName):
    try:
        category = Category.objects.get(name=currentName, user=request.user)
    except Category.DoesNotExist:
        return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CategoryNameSerializer(category, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_category(request, currentName):
    try:
        # Retrieve the category to be deleted
        category = Category.objects.get(name=currentName, user=request.user)
    except Category.DoesNotExist:
        # Return a 404 response if the category is not found
        return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    # Delete the category
    category.delete()
    return Response({"detail": "Category deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_category(request):
    data = request.data.copy()
    data['user'] = request.user.id

    # Check if the category already exists for the user
    existing_category = Category.objects.filter(user=request.user, name=data['name']).exists()


    if existing_category:
        return Response({'error': 'Category already exists for the user'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = NewCategorySerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print("Data:", request.data)
        print("Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_category_id(request, category_name):
    user = request.user
    category = get_object_or_404(Category, name=category_name, user=user)
    return Response({'id': category.id})



######################## Home Page ########################

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])  
# def get_user_emails(request):
#     user = request.user
#     emails = Email.objects.filter(id_user=user)
#     serializer = UserEmailSerializer(emails, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])  
# def get_email_bullet_points(request, email_id):
#     user = request.user

#     # Check if the email belongs to the authenticated user
#     email = get_object_or_404(Email, id_user=user, id=email_id)

#     bullet_points = BulletPoint.objects.filter(id_email=email)
#     serializer = BulletPointSerializer(bullet_points, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_emails(request):
    print("get_user_emails")
    user = request.user
    emails = Email.objects.filter(user=user).prefetch_related('category', 'bulletpoint_set')

    # A set of all possible priorities. Adjust according to your needs.
    all_priorities = {'Important', 'Information', 'Useless'}

    formatted_data = defaultdict(lambda: defaultdict(list))

    for email in emails:
        email_data = {
            "id": email.id,
            "id_provider": email.provider_id,
            "email": email.sender.email,
            "name": email.sender.name,
            "description": email.email_short_summary,
            "details": [{"id": bp.id, "text": bp.content} for bp in email.bulletpoint_set.all()]
        }
        formatted_data[email.category.name][email.priority].append(email_data)
    
    # Ensuring all priorities are present for each category
    for category in formatted_data:
        for priority in all_priorities:
            formatted_data[category].setdefault(priority, [])

    logger.info(formatted_data)
    return Response(formatted_data, status=status.HTTP_200_OK)


# POST

@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def set_email_read(request, email_id):
    user = request.user

    # Check if the email belongs to the authenticated user
    email = get_object_or_404(Email, user=user, id=email_id)

    # Update the read field
    email.read = True
    email.save()

    # Serialize the data to return
    serializer = EmailReadUpdateSerializer(email)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def set_email_reply_later(request, email_id):
    user = request.user

    # Check if the email belongs to the authenticated user
    email = get_object_or_404(Email, user=user, id=email_id)

    # Update the reply_later field
    email.reply_later = True
    email.save()

    # Serialize the data to return
    serializer = EmailReplyLaterUpdateSerializer(email)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def set_rule_block_for_sender(request, email_id):
    user = request.user

    # Check if the email belongs to the authenticated user
    email = get_object_or_404(Email, user=user, id=email_id)
    
    # Check if there's a rule for this sender and user
    rule, _ = Rule.objects.get_or_create(id_sender=email.id_sender, id_user=user)

    # Update the block field
    rule.block = True
    rule.save()

    # Serialize the data to return
    serializer = RuleBlockUpdateSerializer(rule)
    return Response(serializer.data, status=status.HTTP_200_OK)






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
        return Response({"error": "Failed to authenticate or no search query provided"}, status=400)



######################## PROMPT ENGINEERING ########################
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def find_user_view_ai(request):
    """Searches for emails in the user's mailbox based on the provided search query in both the subject and body."""
    user = request.user
    email = request.headers.get("email")
    search_query = request.GET.get('query')

    if search_query:
        main_list, cc_list, bcc_list = gpt_3_5_turbo.extract_contacts_recipients(search_query)

        if main_list == "INCORRECT":
            return Response({"error": "Invalid input or query not about email recipients"}, status=400)

        # Function to find emails for a list of recipients
        def find_emails_for_recipients(recipient_list):
            social_api = get_object_or_404(SocialAPI, user=user, email=email)
            type_api = social_api.type_api
            
            if type_api == 'google':
                services = google_api.authenticate_service(user, email)
                return {recipient: google_api.find_user_in_emails(services, recipient) for recipient in recipient_list}
            elif type_api == 'microsoft':
                access_token = microsoft_api.refresh_access_token(microsoft_api.get_social_api(user, email))
                return {recipient: microsoft_api.find_user_in_emails(access_token, recipient) for recipient in recipient_list}

        # Find emails for main recipients, CC, and BCC
        main_recipients_with_emails = find_emails_for_recipients(main_list)
        cc_recipients_with_emails = find_emails_for_recipients(cc_list)
        bcc_recipients_with_emails = find_emails_for_recipients(bcc_list)

        logging.info(f"{Fore.GREEN}Email recipients (main): {main_recipients_with_emails}")

        return Response({
            "main_recipients": main_recipients_with_emails,
            "cc_recipients": cc_recipients_with_emails,
            "bcc_recipients": bcc_recipients_with_emails
        }, status=200)
    else:
        return Response({"error": "Failed to authenticate or no search query provided"}, status=400)


#----------------------- REDACTION -----------------------#
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_email_ai(request):
    serializer = NewEmailAISerializer(data=request.data)

    if serializer.is_valid():
        input_data = serializer.validated_data['input_data']
        length = serializer.validated_data['length']
        formality = serializer.validated_data['formality']

        subject_text, mail_text = gpt_4.gpt_langchain_redaction(input_data, length, formality)

        print("LOG MAIL", mail_text)

        # Return the response
        return Response({'subject': subject_text, 'mail': mail_text})
    else:
        return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_email_recommendations(request):    
    serializer = EmailAIRecommendationsSerializer(data=request.data)

    if serializer.is_valid():
        mail_content = serializer.validated_data['mail_content']
        user_recommendation = serializer.validated_data['user_recommendation']
        email_subject = serializer.validated_data['email_subject']
        
        print(f'{Fore.CYAN}mail_content: {mail_content}')
        print(f'{Fore.CYAN}user_recommendation: {user_recommendation}')
        print(f'{Fore.CYAN}email_subject: {email_subject}')

        subject_text, email_body = gpt_3_5_turbo.gpt_new_mail_recommendation(mail_content, user_recommendation, email_subject)

        return Response({'subject': subject_text, 'email_body': email_body})
    else:
        logging.error(f'{Fore.RED}Error: {serializer.errors}')
        return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def gpt_improve_email_writing(request):
    """Enhance the subject and body of an email in both quantity and quality in French, while preserving key details from the original version."""
    serializer = EmailCorrectionSerializer(data=request.data)

    if serializer.is_valid():
        email_body = serializer.validated_data['email_body']
        email_subject = serializer.validated_data['email_subject']

        email_body, subject_text = gpt_3_5_turbo.gpt_improve_email_writing(email_body, email_subject)
        
        return Response({'subject': subject_text, 'email_body': email_body})        
    else:
        logging.error(f'{Fore.RED}Error: {serializer.errors}')
        return Response(serializer.errors, status=400)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def correct_email_language(request):
    """Corrects spelling and grammar mistakes in the email subject and body based on user's request."""
    serializer = EmailCorrectionSerializer(data=request.data)

    if serializer.is_valid():
        email_subject = serializer.validated_data['email_subject']
        email_body = serializer.validated_data['email_body']

        corrected_subject, corrected_body, num_corrections = gpt_3_5_turbo.correct_mail_language_mistakes(email_subject, email_body)

        return Response({
            'corrected_subject': corrected_subject,
            'corrected_body': corrected_body,
            'num_corrections': num_corrections
        })
    else:
        return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_email_copywriting(request):
    serializer = EmailCopyWritingSerializer(data=request.data)
    print("Serializer :", serializer)

    if serializer.is_valid():
        email_subject = serializer.validated_data['email_subject']
        email_body = serializer.validated_data['email_body']

        feedback_copywriting = gpt_3_5_turbo.improve_email_copywriting(email_subject, email_body)

        return Response({'feedback_copywriting': feedback_copywriting})
    else:
        return Response(serializer.errors, status=400)


#----------------------- ANSWER -----------------------#
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_email_response_keywords(request):
    serializer = EmailProposalAnswerSerializer(data=request.data)

    if serializer.is_valid():
        email_content = serializer.validated_data['email_content']
        response_keywords = gpt_4.generate_response_keywords(email_content)

        return Response({
            'response_keywords': response_keywords,
        })
    else:
        return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_email_answer(request):
    serializer = EmailGenerateAnswer(data=request.data)

    if serializer.is_valid():
        email_content = serializer.validated_data['email_content']
        response_type = serializer.validated_data['response_type']
        email_answer = gpt_4.generate_email_response(email_content, response_type)

        return Response({
            'email_answer': email_answer,
        })
    else:
        return Response(serializer.errors, status=400)


#----------------------- REPLY LATER -----------------------#
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_answer_later_emails(request):
    try:
        user = request.user
        emails = Email.objects.filter(user=user, answer_later=True).prefetch_related('bulletpoint_set', 'sender', 'category')

        all_priorities = {'Important', 'Information', 'Useless'}

        formatted_data = defaultdict(lambda: defaultdict(list))

        for email in emails:
            email_data = {
                "id": email.id,
                "id_provider": email.provider_id,
                "email": email.sender.email,
                "name": email.sender.name,
                "description": email.email_short_summary,
                "details": [{"id": bp.id, "text": bp.content} for bp in email.bulletpoint_set.all()]
            }
            formatted_data[email.category.name][email.priority].append(email_data)
        
        # Ensuring all priorities are present for each category
        for category in formatted_data:
            for priority in all_priorities:
                formatted_data[category].setdefault(priority, [])

        logger.info(formatted_data)
        return Response(formatted_data, status=status.HTTP_200_OK)

    except Exception as e:
        logging.error(f"Error fetching emails: {e}")
        return Response({"error": "An error occurred while fetching emails."}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)



######################## Settings ########################
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_bg_color(request):
    try:
        preferences = Preference.objects.get(user=request.user)
        serializer = PreferencesSerializer(preferences)
        return Response(serializer.data)

    except Preference.DoesNotExist:
        return Response({"error": "Preferences not found for the user."}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_details(request):
    return Response({'username': request.user.username})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_username(request):
    user = request.user
    new_username = request.data.get('username')

    if not new_username:
        return Response({'error': 'No new username provided.'}, status=400)

    # Check if user requirements
    if User.objects.filter(username=new_username).exists():
        return Response({'error': 'Username already exists'}, status=400)
    elif " " in new_username:
        return Response({'error': 'Username must not contain spaces'}, status=400)

    user.username = new_username
    user.save()
    
    logging.info(f"{Fore.CYAN}User: {user} changed its name in {new_username}")
    return Response({'success': 'Username updated successfully.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_password(request):
    user = request.user
    new_password = request.data.get('password')

    if not new_password:
        return Response({'error': 'No new password provided.'}, status=400)

    # Checks passwords requirements
    if not (8 <= len(new_password) <= 32):
        return Response({'error': 'Password length must be between 8 and 32 characters'}, status=400)
    if " " in new_password:
        return Response({'error': 'Password must not contain spaces'}, status=400)
    elif not re.match(r'^[a-zA-Z0-9!@#$%^&*()-=_+]+$', new_password):
        return Response({'error': 'Password contains invalid characters'}, status=400)

    user.set_password(new_password)
    user.save()

    return Response({'success': 'Password updated successfully.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_first_email(request):
    """Returns the first email associated with the user in mailassistantdb"""
    user = request.user
    social_api_instance = get_object_or_404(SocialAPI, user=user)
    
    # TODO: update the code to handle when the user has several emails
    email = social_api_instance.email
    
    if email:
        return Response({'email': email}, status=200)
    else:
        return Response({'error': 'No emails associated with the user'}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_user_bg_color(request):
    try:
        # Retrieve the user's Preference object
        preferences = Preference.objects.get(user=request.user)
    except Preference.DoesNotExist:
        # Create a new Preference object if it doesn't exist
        preferences = Preference(user=request.user)

    # Update the bg_color field from the request data
    serializer = PreferencesSerializer(preferences, data=request.data)
    if serializer.is_valid():
        serializer.save()  # Save the updated Preference object
        return Response(serializer.data)
    else:
        # Return validation errors if the data is not valid
        return Response(serializer.errors, status=400)



######################## RULES ########################
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_rules(request):
    user_rules = Rule.objects.filter(user=request.user)
    rules_data = []

    for rule in user_rules:
        # Serialize the basic rule data
        rule_serializer = RuleSerializer(rule)
        rule_data = rule_serializer.data

        # Manually add category name and sender details
        category_name = rule.category.name if rule.category else None
        sender_name = rule.sender.name if rule.sender else None
        sender_email = rule.sender.email if rule.sender else None

        rule_data['category_name'] = category_name
        rule_data['sender_name'] = sender_name
        rule_data['sender_email'] = sender_email

        rules_data.append(rule_data)

    return Response(rules_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_sender(request):
    serializer = SenderSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user_rule(request):
    serializer = RuleSerializer(data=request.data, context={'user': request.user})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    else:
        print("Data:", request.data)
        print("Errors:", serializer.errors)
        return Response(serializer.errors, status=400)



######################## TESTING ########################
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_authenticated(request):
    return Response(status=200)




# TO TEST Gmail GET the Mail from id
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mail_view(request):
    user = request.user
    email = request.headers.get('email')
    service = google_api.authenticate_service(user, email)
    
    if service is not None:
        subject, from_name, decoded_data, email_id = google_api.get_mail(service, 0, None)
        # Return a success response, along with any necessary information
        return Response({
            "message": "Authentication successful",
            "email": {
                "subject": subject,
                "from_name": from_name,
                "decoded_data": decoded_data,
                "email_id": email_id
            }
        }, status=200)
    else:
        # Return an error response
        return Response({"error": "Failed to authenticate"}, status=400)

# TO TEST Gmail GET Last Email
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mail_by_id_view(request):
    user = request.user
    email = request.headers.get('email')
    service = google_api.authenticate_service(user, email)
    mail_id = request.GET.get('email_id')
    
    if service is not None and mail_id is not None:
        
        subject, from_name, decoded_data, cc, bcc, email_id = google_api.get_mail(service, None, mail_id)
        #print("DEBUG OUTPUT -------------------------> ", from_name, cc, bcc)
        return Response({
            "message": "Authentication successful",
            "email": {
                "subject": subject,
                "from_name": from_name,
                "decoded_data": decoded_data,
                "cc": cc,  
                "bcc": bcc,
                "email_id": email_id
            }
        }, status=200)
    else:
        # Return an error response
        return Response({"error": "Failed to authenticate"}, status=400)

# TO TEST Gmail Save in BDD Last Email
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def save_last_mail_view(request):
    user = request.user
    email = request.headers.get('email')
    service = google_api.authenticate_service(user, email)
    
    if service is not None:
        processed_email_to_bdd(request,service)
        # Return a success response, along with any necessary information
        return Response({
            "message": "Save successful"
        }, status=200)
    else:
        # Return an error response
        return Response({"error": "Failed to authenticate"}, status=400)

# TO TEST AUTH API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def authenticate_service_view(request):
    user = request.user
    email = request.headers.get('email')
    service = google_api.authenticate_service(user, email)
    
    if service is not None:
        # Return a success response, along with any necessary information
        return Response({"message": "Authentication successful"}, status=200)
    else:
        # Return an error response
        return Response({"error": "Failed to authenticate"}, status=400)



######################## OLD ########################

# TO UPDATE
'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_login(request):
    try:
        user = Users.objects.get(id_user=request.user.id)
        serializer = UserLoginSerializer(user)
        return Response(serializer.data)
    except Users.DoesNotExist:
        return Response({"error": "User not found."}, status=404)'''

