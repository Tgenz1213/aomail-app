"""
Handles prompt engineering requests for GPT-3.5-turbo API.
"""
import json
import re
from django.db import IntegrityError
import openai
import ast
from colorama import Fore, init
from MailAssistant import google_api
from .models import BulletPoint, Category, Email, Sender



######################## GPT - 3.5 turbo API SETTINGS ########################
OPENAI_CREDS = json.load(open('creds/openai_creds.json', 'r'))
init(autoreset=True)



######################## TEXT PROCESSING UTILITIES ########################
def get_prompt_response(formatted_prompt):
    """Returns the prompt response"""
    client = openai.OpenAI(organization=OPENAI_CREDS['organization'], api_key=OPENAI_CREDS['api_key'])
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[{
            "role": "assistant",
            "content": formatted_prompt
        }]
    )
    return response


def get_language(input_subject, input_body):
    """Returns the primary language used in the email"""

    template = """Given an email with subject: '{input_subject}' and body: '{input_body}',
    IDENTIFY the primary language used (e.g., French, English, Russian), prioritizing the body over the subject.
    
    Provide the answer in JSON format with the key 'language' (STRING).
    """
    formatted_prompt = template.format(input_body=input_body, input_subject=input_subject)
    response = get_prompt_response(formatted_prompt)
    clear_text = response.choices[0].message.content.strip()
    language = json.loads(clear_text)["language"]

    print(f'{Fore.LIGHTBLUE_EX}The language used is: {language}')

    return language


def count_corrections(original_subject, original_body, corrected_subject, corrected_body):
    """Count and compare corrections in original and corrected texts"""

    # Splitting the original and corrected texts into words
    original_subject_words = original_subject.split()
    corrected_subject_words = corrected_subject.split()
    original_body_words = original_body.split()
    corrected_body_words = corrected_body.split()

    # Counting the differences in the subject
    subject_corrections = sum(1 for orig, corr in zip(original_subject_words, corrected_subject_words) if orig != corr)

    # Counting the differences in the body
    body_corrections = sum(1 for orig, corr in zip(original_body_words, corrected_body_words) if orig != corr)

    # Total corrections
    total_corrections = subject_corrections + body_corrections

    return total_corrections


def extract_contacts_recipients(query):
    template = """As an email assistant,

    Analyze the following input: '{query}' to determine recipients for an email. Follow these rules:

    1. If no main recipients are explicitly indicated, assume all recipients are main recipients.
    2. If no CC or BCC recipients are specified, include all recipients in the main_recipients list.

    Return the results in JSON format with three keys:
    main_recipients: [Python list],
    cc_recipients: [Python list],
    bcc_recipients: [Python list]    
    """
    formatted_prompt = template.format(query=query)
    response = get_prompt_response(formatted_prompt)
    response_text = response.choices[0].message.content.strip()    
    recipients = json.loads(response_text)

    # Extract information based on markers
    main_recipients = recipients.get('main_recipients', [])
    cc_recipients = recipients.get('cc_recipients', [])
    bcc_recipients = recipients.get('bcc_recipients', [])

    print(f"{Fore.CYAN}Main Recipients: {main_recipients}")
    print(f"{Fore.BLUE}Carbon Copy: {cc_recipients}")
    print(f"{Fore.GREEN}Blind Carbon Copy: {bcc_recipients}")

    return main_recipients, cc_recipients, bcc_recipients


#----------------------- PREPROCESSING REPLY EMAIL -----------------------#
def generate_response_keywords(input_subject, input_email, language) -> list:
    """Generate a list of keywords for responding to a given email."""

    template = """As an email assistant, and given the email with subject: '{input_subject}' and body: '{input_email}' written in {language}.

    IDENTIFY up to 4 different ways to respond to this email.
    USE as few verbs in {language} as possible while keeping a relevant meaning.
    KEYWORDS must look like buttons the user WILL click to reply to the email.

    Answer must be a list (Python) format: ["....", "....."]
    """
    formatted_prompt = template.format(input_subject=input_subject, input_email=input_email, language=language)
    response = get_prompt_response(formatted_prompt)
    keywords = response.choices[0].message.content.strip()

    print(f'{Fore.YELLOW}{keywords}')

    keywords_list = ast.literal_eval(keywords)

    return keywords_list


def shorten_keywords(keywords) -> dict:
    """Shorten each keyword in the given list"""

    formatted_prompt = f"""As an email assistant,

    Given this list of keywords '{keywords}', GENERATE a shorter version for each keyword/
    

    Answer must be a Json format with KEYS being each NEW keyword and values being each associated old keyword
    """
    response = get_prompt_response(formatted_prompt)
    keywords_dict = json.loads(response.choices[0].message.content.strip())

    print(f'{Fore.YELLOW}{keywords_dict}')

    return keywords_dict



######################## WRITING ########################
def gpt_improve_email_writing(body, subject):
    """Enhance email subject and body in French"""

    template = """As an email assistant, enhance the subject and body of this email in both QUANTITY and QUALITY in FRENCH, while preserving key details from the original version.
    
    Answer must be a Json format with two keys: subject (STRING) AND body (HTML)

    subject: {email_subject},
    body: {mail_content}
    """
    formatted_prompt = template.format(email_subject=subject, mail_content=body)
    response = get_prompt_response(formatted_prompt)    
    clear_text = response.choices[0].message.content.strip()
    result_json = json.loads(clear_text)

    subject_text = result_json['subject']
    email_body = result_json['body']

    print(f"{Fore.CYAN}EMAIL DRAFT IMPROVED:")
    print(f"{Fore.GREEN}Subject: {subject_text}")
    print(f"{Fore.CYAN}Email Body: {email_body}")

    return email_body, subject_text


def gpt_new_mail_recommendation(mail_content, email_subject, user_recommendation):
    """Enhance email subject and body in FRENCH based on user guideline"""

    template = """As an email assistant, enhance the subject and body of this email in both QUANTITY and QUALITY in FRENCH according to the user guideline: '{user_recommendation}', while preserving key details from the original version.
    
    Answer must be a Json format with two keys: subject (STRING) AND body (HTML)

    subject: {email_subject},
    body: {mail_content}
    """
    formatted_prompt = template.format(user_recommendation=user_recommendation, email_subject=email_subject, mail_content=mail_content)
    response = get_prompt_response(formatted_prompt)    
    clear_text = response.choices[0].message.content.strip()

    result_json = json.loads(clear_text)
    subject_text = result_json['subject']
    email_body = result_json['body']
    
    print(f"{Fore.CYAN}NEW EMAIL RECOMMENDATION:")
    print(f"{Fore.GREEN}Subject: {subject_text}")
    print(f"{Fore.LIGHTGREEN_EX}Email Body: {email_body}")

    return subject_text, email_body


def gpt_langchain_redaction(input_data, length, formality):
    """Generate a French email, enhancing both QUANTITY and QUALITY according to user guidelines."""

    template = """As an email assistant, write a {length} and {formality} email in FRENCH.
    Improve the QUANTITY and QUALITY in FRENCH according to the user guideline: '{input_data}', it should strictly contain only the information present in the input.

    Answer must be a Json format with two keys: subject (STRING) AND body IN HTML FORMAT (HTML)
    """
    formatted_prompt = template.format(input_data=input_data, length=length, formality=formality)
    response = get_prompt_response(formatted_prompt)

    clear_text = response.choices[0].message.content.strip()
    result_json = json.loads(clear_text)

    subject_text = result_json.get('subject')
    email_body = result_json.get('body')

    print(f"{Fore.CYAN}{length} and {formality} email suggestion:")
    print(f"{Fore.GREEN}Subject: {subject_text}")
    print(f"{Fore.CYAN}Email Body: {email_body}")

    return subject_text, email_body


def correct_mail_language_mistakes(body, subject):
    """Corrects spelling and grammar mistakes in the email subject and body based on user's request."""

    template = """As an email assistant, check the following FRENCH text for any grammatical or spelling errors and correct them, Do not change any words unless they are misspelled or grammatically incorrect.
    
    Answer must be a Json format with two keys: subject (STRING) AND body (HTML)

    subject: {email_subject},
    body: {mail_content}
    """
    formatted_prompt = template.format(email_subject=subject, email_body=body)
    response = get_prompt_response(formatted_prompt)
    clear_text = response.choices[0].message.content.strip()
    result_json = json.loads(clear_text)

    corrected_subject = result_json['subject']
    corrected_body = result_json['body']

    print(f"{Fore.CYAN}EMAIL CORRECTED:")
    print(f"{Fore.GREEN}Subject: {corrected_subject}")
    print(f"{Fore.CYAN}Email Body: {corrected_body}")

    # Count the number of corrections
    num_corrections = count_corrections(subject, body, corrected_subject, corrected_body)

    return corrected_subject, corrected_body, num_corrections


# TODO: improve prompt engineering + get a json response from GPT
def improve_email_copywriting(email_subject, email_body):
    """Provides feedback and suggestions for improving the copywriting in the email subject and body."""

    # Simplified template for direct feedback and suggestions on copywriting
    template = """Évaluez en français la qualité du copywriting du sujet et du corps de cet e-mail. Fournissez un retour et des suggestions d'amélioration.

    Objet de l'e-mail :
    "{email_subject}"

    Corps de l'e-mail :
    "{email_body}"

    ---

    <strong>Retour sur l'objet</strong> :
    [Votre retour sur l'objet]

    <strong>Suggestions pour l'objet</strong> :
    [Vos suggestions pour l'objet]

    <strong>Retour sur le corps de l'e-mail</strong> :
    [Votre retour sur le corps de l'e-mail]

    <strong>Suggestions pour le corps de l'e-mail</strong> :
    [Vos suggestions pour le corps de l'e-mail]
    """

    formatted_prompt = template.format(email_subject=email_subject, email_body=email_body)
    response = get_prompt_response(formatted_prompt)
    response_text = response.choices[0].message.content.strip()

    print(f"{Fore.CYAN}EMAIL COPYWRITING:")
    print(f"{Fore.GREEN}{response_text}")

    return response_text

def generate_email_response(input_subject, input_body, response_type, language):
    """Generates a French email response based on the given response type"""
    template = """Based on the email with the subject: '{input_subject}' and body: '{input_body}' craft a response in {language} following the '{response_type}' instruction. Ensure the response is structured as an HTML email. Here is a template to follow, with placeholders for the dynamic content:
    <p>[Insert greeting]</p><!-- Insert response here based on the input body and the specified response type --><p>[Insert sign_off],</p><p>[Your Name]</p>

    ----

    Answer must be HTML : <p></p>
    """
    # DO NOT DELETE : possible upgrade TO TEST (something like this in the template) : craft a response in {language} following the '{response_type}' instruction, do not invent new demands that the user didn't ask, ONLY IF NECESSARY you can leave blank space after ':' if you want the user to manually complete the answer
    formatted_prompt = template.format(input_subject=input_subject, input_body=input_body, response_type=response_type, language=language)
    response = get_prompt_response(formatted_prompt)
    body = response.choices[0].message.content.strip()

    print(f'{Fore.GREEN}[REPLY] body: {body}')

    return body





####################################################################
######################## UNDER CONSTRUCTION ########################
####################################################################
    

importance_list = {
    'Important': 'Items or messages that are of high priority, do not contain offers to "unsubscribe", and require immediate attention or action.',
    'Information' : 'Details that are relevant and informative but may not require immediate action. Does not contain offers to "unsubscribe".',
    'Useless': 'Items or messages that contain offers to "unsubscribe", might not be relevant to all recipients, are redundant, or do not provide any significant value.'
}
user_description = "Enseignant chercheur au sein d'une école d'ingénieur ESAIP."

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


def processed_email_to_bdd(request, services):
    subject, from_name, decoded_data, cc, bcc, email_id = google_api.get_mail(services, 0, None)

    print(f'{Fore.YELLOW}{subject, from_name, decoded_data, cc, bcc, email_id}')

    if not Email.objects.filter(provider_id=email_id).exists():

        # Check if data is decoded, then format it
        if decoded_data:
            decoded_data = format_mail(decoded_data)

        # Get user categories
        category_list = get_db_categories(request.user)

        #print("DEBUG -------------> category", category_list)

        # Process the email data with AI/NLP
        topic, importance, answer, summary, sentence, relevance, importance_explain = gpt_langchain_response(subject, decoded_data, category_list)

        #print("TEST -------------->", from_name, "TYPE ------------>", type(from_name))
        #sender_name, sender_email = separate_name_email(from_name) => OLD USELESS
        sender_name, sender_email = from_name[0], from_name[1]

        # Fetch or create the sender
        sender, created = Sender.objects.get_or_create(name=sender_name, email=sender_email)  # assuming from_name contains the sender's name

        print("DEBUG ----------------> topic", topic)
        # Get the relevant category based on topic or create a new one (for simplicity, I'm getting an existing category)
        category = Category.objects.get_or_create(name=topic, user=request.user)[0]

        provider = 'Gmail'

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


# TODO: Put in gpt_3_5_turbo.py AFTER testing
# REMOVE hardcoded variables

# Summarize and categorize an email
def gpt_langchain_response(subject, decoded_data, category_list):
    template = (
        """Given the following email:

        Subject:
        {subject}

        Text:
        {text}

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
    formatted_template = template.format(
        subject=subject,
        text=decoded_data,
        user=user_description,
        category=category_list,
        importance=importance_list,
        answer=response_list,
        relevance=relevance_list
    )
    
    response = get_prompt_response(formatted_template)  
    clear_response = response.choices[0].message.content.strip()

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

    # Finding start of the summary
    match = re.search(r"Résumé en français(\s\(without using importance, response or relevance categorization\))?:", clear_response)

    if match:
        # Adjusting the start index based on the match found
        summary_start = match.end()
    else:
        # Fallback or default behavior if the pattern is not found
        summary_start = -1  # Or handle this case as needed

    # Finding the end of the summary
    summary_end = clear_response.find("\n\n", summary_start)
    if summary_end == -1:  # If there's no double newline after the start, consider till the end of the string
        summary_end = len(clear_response)

    # Extracting the summary if a valid start index was found
    if summary_start != -1:
        summary_text = clear_response[summary_start:summary_end].strip()
    else:
        summary_text = "Summary not found."

    return topic_category, importance_categories, response_category, summary_text, short_sentence, relevance_category, importance_percentages