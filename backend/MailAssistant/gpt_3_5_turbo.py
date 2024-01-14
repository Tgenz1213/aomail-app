"""
Handles prompt engineering requests for GPT-3.5-turbo API.
"""
import json
import logging
import re
from colorama import Fore, init
import openai


######################## GPT - 3.5 turbo API SETTINGS ########################
openai.organization = "org-YSlFvq9rM1qPzM15jewopUUt"
openai.api_key = "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"
init(autoreset=True)



######################## TEXT PROCESSING UTILITIES ########################
def get_prompt_response(formatted_prompt):
    """Returns the prompt response"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "assistant", "content": formatted_prompt}],
    )
    return response


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
    response_text = response.choices[0].message['content'].strip()

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


def improve_email_copywriting(email_subject, email_body):
    """Provides feedback and suggestions for improving the copywriting in the email subject and body."""

    # Simplified template for direct feedback and suggestions on copywriting
    template = """
    Évaluez en français la qualité du copywriting du sujet et du corps de cet e-mail. Fournissez un retour et des suggestions d'amélioration.

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
    response_text = response.choices[0].message['content'].strip()

    return response_text


def gpt_improve_email_writing(body, subject):
    template = """As an email assistant, enhance the subject and body of this email in both QUANTITY and QUALITY in FRENCH, while preserving key details from the original version.
    
    Answer must be a Json format with two keys: subject (STRING) AND body (HTML)

    subject: {email_subject},
    body: {mail_content}
    """
    formatted_prompt = template.format(email_subject=subject, mail_content=body)
    response = get_prompt_response(formatted_prompt)    
    clear_text = response.choices[0].message['content'].strip()
    result_json = json.loads(clear_text)

    return result_json['body'], result_json['subject']


def gpt_new_mail_recommendation(mail_content, email_subject, user_recommendation):
    template = """As an email assistant, enhance the subject and body of this email in both QUANTITY and QUALITY in FRENCH according to the user guideline: '{user_recommendation}', while preserving key details from the original version.
    
    Answer must be a Json format with two keys: subject (STRING) AND body (HTML)

    subject: {email_subject},
    body: {mail_content}
    """
    formatted_prompt = template.format(user_recommendation=user_recommendation, email_subject=email_subject, mail_content=mail_content)
    response = get_prompt_response(formatted_prompt)    
    clear_text = response.choices[0].message['content'].strip()

    result_json = json.loads(clear_text)
    subject_text = result_json['subject']
    email_body = result_json['body']
    
    print(f"{Fore.GREEN}Subject: {subject_text}")
    print(f"{Fore.LIGHTGREEN_EX}Email Body: {email_body}")

    return subject_text, email_body


def correct_mail_language_mistakes(body, subject):
    """Corrects spelling and grammar mistakes in the email subject and body based on user's request."""    
    template = """As an email assistant, check the following French text for any grammatical or spelling errors and correct them, Do not change any words unless they are misspelled or grammatically incorrect.
    
    Answer must be a Json format with two keys: subject (STRING) AND body (HTML)

    subject: {email_subject},
    body: {mail_content}
    """
    formatted_prompt = template.format(email_subject=subject, email_body=body)
    response = get_prompt_response(formatted_prompt)
    clear_text = response.choices[0].message['content'].strip()
    result_json = json.loads(clear_text)

    print(f"{Fore.GREEN}Response Text : ", result_json)

    corrected_subject = result_json['subject']
    corrected_body = result_json['body']

    # Count the number of corrections
    num_corrections = count_corrections(subject, body, corrected_subject, corrected_body)

    return corrected_subject, corrected_body, num_corrections