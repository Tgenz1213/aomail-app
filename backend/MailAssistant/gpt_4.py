"""
Handles prompt engineering requests for GPT-4 API.
"""

import json
import os
import openai
from colorama import Fore, init
from MailAssistant import gpt_3_5_turbo


######################## GPT - 4 API SETTINGS ########################
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
OPENAI_CREDS = json.load(open(f"{BACKEND_DIR}/creds/openai_creds.json", "r"))
init(autoreset=True)


######################## TEXT PROCESSING UTILITIES ########################
def get_prompt_response(formatted_prompt):
    """Returns the prompt response"""
    client = openai.OpenAI(
        organization=OPENAI_CREDS["organization"], api_key=OPENAI_CREDS["api_key"]
    )
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "system", "content": formatted_prompt}],
    )
    return response


######################## WRITING FUNCTIONS ########################
def generate_email_response(input_subject, input_body, response_type, language):
    """Generates a French email response based on the given response type"""
    template = """As an email assistant, REPLY in {language} to the email with subject: '{input_subject}' and body: '{input_body}'.

    Based on the user indication: '{response_type}', REPLY to the email without adding any new details.
    It should STRICTLY correspond to the information present in the original email.

    Answer must ONLY be an HTML email body
    """
    formatted_prompt = template.format(
        input_subject=input_subject,
        input_body=input_body,
        response_type=response_type,
        language=language,
    )
    response = get_prompt_response(formatted_prompt)
    body = response.choices[0].message.content.strip()

    print(f"{Fore.GREEN}[REPLY] body: {body}")

    return body


######################## DEPRECATED FUNCTIONS ########################
def gpt_langchain_redaction(input_data, length, formality):
    template = """
        Given the following draft:

        "{input_data}"

        Please follow these instructions carefully:
        1. Write a short subject for the email based on the draft in French.
        2. Write an email in French that matches the length and content of the input. The email should be {length}, {formality}, and should strictly contain only the information present in the input. Do not add any new details or information.
        ---

        Subject:
        [Model's drafted subject]

        Draft:
        [Model's drafted email]
    """

    formatted_prompt = template.format(
        input_data=input_data, length=length, formality=formality
    )

    print("FORMATTED PROMPT", formatted_prompt)

    response = get_prompt_response(formatted_prompt)

    clear_text = response.choices[0].message.content.strip()

    print("clear_text: ", clear_text)

    # Extracting Subject
    subject_start = clear_text.index("Subject:") + len("Subject:")
    subject_end = (
        clear_text[subject_start:].index("\n\n")
        if "\n\n" in clear_text[subject_start:]
        else len(clear_text)
    )
    subject_list = (
        clear_text[subject_start : subject_start + subject_end].strip().split("\n")
    )
    subject_text = "\n".join(subject_list)

    # Extracting Email
    mail_start = clear_text.index("Draft:") + len("Draft:")
    mail_list = clear_text[mail_start : len(clear_text)].strip().split("\n")
    mail_text = "\n".join(mail_list)

    print("Email :", mail_text)

    return subject_text, mail_text


def gpt_new_mail_recommendation(mail_content, user_recommendation, email_subject):
    template = """
        Consider the following email subject, content, and user recommendation in French:

        Email Subject:
        "{email_subject}"

        Email Content:
        "{mail_content}"

        User Recommendation:
        "{user_recommendation}"

        Based on the user recommendation, modify the email while keeping as much of the original content and intent as possible. Please provide:
        1. An revised subject for the email, if the recommendation suggests a change.
        2. A revised body of the email that incorporates the recommendation without altering the original message unnecessarily.

        ---

        Subject:
        [Adjusted Email Subject]

        Email Body:
        [Revised Email Body]
    """

    formatted_prompt = template.format(
        mail_content=mail_content,
        user_recommendation=user_recommendation,
        email_subject=email_subject,
    )

    print("FORMATTED PROMPT", formatted_prompt)

    response = get_prompt_response(formatted_prompt)

    clear_text = response.choices[0].message.content.strip()

    # Extract the subject and body of the email
    subject_start = clear_text.index("Subject:") + len("Subject:")
    subject_end = clear_text.index("Email Body:")
    subject_text = clear_text[subject_start:subject_end].strip()
    body_start = subject_end + len("Email Body:")
    email_body = clear_text[body_start:].strip()

    # Removing quotations from subject and body
    if subject_text.startswith('"') and subject_text.endswith('"'):
        subject_text = subject_text[1:-1]
    if email_body.startswith('"') and email_body.endswith('"'):
        email_body = email_body[1:-1]

    print("Subject:", subject_text)
    print("Email Body:", email_body)

    return subject_text, email_body


def correct_mail_language_mistakes(email_subject, email_body):
    """Corrects spelling and grammar mistakes in the email subject and body based on user's request."""
    template = """
    Please check the following French text for any grammatical or spelling errors and correct them. Do not change any words unless they are misspelled or grammatically incorrect.

    Subject:
    "{email_subject}"

    Body:
    "{email_body}"

    ---

    Corrected Subject:
    [Corrected Subject]

    Corrected Body:
    [Corrected Body]
    """
    formatted_prompt = template.format(
        email_subject=email_subject, email_body=email_body
    )
    response = get_prompt_response(formatted_prompt)
    response_text = response.choices[0].message.content.strip()

    print("Response Text : ", response_text)

    # Extract the corrected subject and body
    corrected_subject = extract_between_markers(
        response_text, "Corrected Subject:", "Corrected Body:"
    )
    corrected_body = extract_after_marker(response_text, "Corrected Body:")

    # Count the number of corrections
    num_corrections = gpt_3_5_turbo.count_corrections(
        email_subject, email_body, corrected_subject, corrected_body
    )

    return corrected_subject, corrected_body, num_corrections


######################## TEXT EXTRACTION AND COMPARISON UTILITIES ########################
def extract_between_markers(text, start_marker, end_marker):
    start = text.find(start_marker) + len(start_marker)
    end = text.find(end_marker, start)
    if end > start:
        extracted_text = text[start:end].strip()
        return extracted_text.strip('"')  # Remove surrounding quotation marks
    return ""


def extract_after_marker(text, marker):
    start = text.find(marker) + len(marker)
    if start > -1:
        extracted_text = text[start:].strip()
        return extracted_text.strip('"')  # Remove surrounding quotation marks
    return ""
