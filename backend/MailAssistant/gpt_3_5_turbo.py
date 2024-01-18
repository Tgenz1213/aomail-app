"""
Handles prompt engineering requests for GPT-3.5-turbo API.
"""
import json
import logging
import re
import openai
from colorama import Fore, init



######################## GPT - 3.5 turbo API SETTINGS ########################
OPENAI_CREDS = json.load(open('creds/openai_creds.json', 'r'))
init(autoreset=True)



######################## TEXT PROCESSING UTILITIES ########################
def get_prompt_response(formatted_prompt):
    """Returns the prompt response"""
    client = openai.OpenAI(organization=OPENAI_CREDS['organization'], api_key=OPENAI_CREDS['api_key'])
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
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


# TO UPDATE : make work with langchain
def extract_contacts_recipients(input_query):
    # Define the prompt template for ChatGPT
    template = """Analyze the following input to determine recipients for an email:

    {input_query}

    Format the response as (if no CC or CCI are indicate, put in main):
    1. Main recipients: [username/email, username/email, ...]
    2. CC recipients: [username/email, username/email, ...]
    3. BCC recipients: [username/email, username/email, ...]
    """
    formatted_prompt = template.format(input_query=input_query)
    response = get_prompt_response(formatted_prompt)
    response_text = response.choices[0].message.content.strip()

    logging.info("Received response from ChatGPT: %s", response_text)


    if response_text == "INCORRECT":
        return "INCORRECT", "INCORRECT", "INCORRECT"

    # Define a function to extract items from the response
    def extract_items(response, marker):
        pattern = re.escape(marker) + r"\: \[(.*?)\]"
        match = re.search(pattern, response)
        if match:
            items = match.group(1).split(", ")
            return [item.strip() for item in items]
        else:
            return []

    # Extract information based on markers
    main_recipients = extract_items(response_text, "1. Main recipients")
    cc_recipients = extract_items(response_text, "2. CC recipients")
    bcc_recipients = extract_items(response_text, "3. BCC recipients")

    logging.info("Extracted response from ChatGPT (main): %s", main_recipients)
    logging.info("Extracted response from ChatGPT (CC): %s", cc_recipients)
    logging.info("Extracted response from ChatGPT (BCC): %s", bcc_recipients)

    return main_recipients, cc_recipients, bcc_recipients



#----------------------- PREPROCESSING REPLY EMAIL -----------------------#
def generate_response_keywords(input_subject, input_email, language) -> list:
    """Generate a list of keywords for responding to a given email."""

    template = """As an email assistant, and given the email with subject: '{input_subject}' and body: '{input_email}' written in {language}.

    IDENTIFY up to 4 different ways to respond to this email.
    USE as few verbs in {language} as possible while keeping a relevant meaning.
    KEYWORDS must look like buttons the user WILL click to reply to the email.

    Answer must be a list (Python) format: []
    """
    formatted_prompt = template.format(input_subject=input_subject, input_email=input_email, language=language)
    response = get_prompt_response(formatted_prompt)
    keywords = response.choices[0].message.content.strip()

    print(f'{Fore.YELLOW}{keywords}')

    return keywords


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

    Answer must be a Json format with two keys: subject (STRING) AND body (HTML)
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