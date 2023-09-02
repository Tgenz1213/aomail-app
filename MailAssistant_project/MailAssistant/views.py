# Refactoring the entire code based on the changes discussed

import base64
import re
import time

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
import datetime
from googleapiclient.errors import HttpError
import random
from email import message_from_string

# from .google_api import * 
from . import google_api

# OpenAI - ChatGPT
import openai

# langchain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import SystemMessagePromptTemplate,ChatPromptTemplate

openai.organization = "org-YSlFvq9rM1qPzM15jewopUUt"
openai.api_key = "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"
gpt_model = "gpt-3.5-turbo"

configuration = {
    'organization': "org-YSlFvq9rM1qPzM15jewopUUt",
    'api_key' : "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"
}

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

api_list = [google_api]
api_var = 0

# loading landing page
def home_page(request):
    # connection to google
    services = api_list[api_var].authenticate_service()
    subject, from_name, decoded_data = api_list[api_var].get_mail(services,0,None)

    # subject, from_name, decoded_data = extract_body_from_email(services,0,None) #doesn't work
    
    if decoded_data: decoded_data = format_mail(decoded_data)
    # print("decoded_data: ",decoded_data)

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
        # print('draft: ',draft)
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

    query,query_list = api_list[api_var].email_query(*gpt_langchain_decompose_search([input_ai,input_text]),0)
    print('query: ',query)
    question = search_chat_reply(query_list)
    print('question:',question)

    input_ai = "Que recherchez-vous ?"
    # input_text = "pôle emploi"
    input_text = 'offres_du_bassin'

    # query_attachement = 'offres_du_bassin'
    query_attachement,query_list = api_list[api_var].email_query(*gpt_langchain_decompose_search([input_ai,input_text]),1)
    print('query_attachement: ',query_attachement)
    # attachements = api_list[api_var].search_attachments(query_attachement)
    attachements = api_list[api_var].search_emails(query_attachement)

    print('attachements: ',attachements)

    # email_list_from, email_list_to, starting_date, ending_date, key_words = gpt_langchain_decompose_search([input_ai,input_text])
    # query = email_query(email_list_from,email_list_to,starting_date,ending_date,key_words)
    # emails_id = api_list[api_var].search_emails(query)
    
    # print('from_who: ',from_who)
    # print('to_who: ',to_who)
    # print('key_words: ',key_words)
    # print('starting_date: ',starting_date)
    # print('ending_date: ',ending_date)
    # print("query: ",query)
    # emails_id = search_emails(query)
    # print('emails_id: ',emails_id)

    # if emails_id:
    #     for email_id in emails_id:
    #         # print('email found: ',google_api.get_mail(services,None,email_id))
    #         subject, from_name, decoded_data = api_list[api_var].get_mail(services,None,email_id)
    #         if decoded_data: decoded_data = format_mail(decoded_data)
            # print('email found: ',decoded_data)
            # print('email found: ',get_email_by_id(email_id)) #doesn't work


    # emailist = 'gmail'
    # full_emailist = get_contacts(emailist,'contacts','connections')
    # print('full_emailist: ',full_emailist)
    # full_emailist = get_contacts(emailist,'other.contacts','otherContacts')
    # print('full_emailist: ',full_emailist)

    
    return render(request, 'home_page.html', {'subject': subject,'sender': from_name, 'content': decoded_data})


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

    # Extracting Summary
    summary_start = clear_response.index("Résumé en français:") + len("Résumé en français:")
    summary_end = clear_response[summary_start:].index("\n\n") if "\n\n" in clear_response[summary_start:] else len(clear_response)
    summary_list = clear_response[summary_start:summary_start+summary_end].strip().split("\n- ")[1:]
    summary_text = "\n".join(summary_list)

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


######################## Other ########################

def send_mail(request):
    api_list[api_var].send_mail(request)

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

