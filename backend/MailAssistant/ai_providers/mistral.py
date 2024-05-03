"""
Handles prompt engineering requests for Mistral API.
"""

import ast
from datetime import datetime
import json
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from MailAssistant.constants import DEFAULT_CATEGORY, MISTRAL_CREDS
from colorama import Fore, init


######################## MISTRAL API SETTINGS ########################
init(autoreset=True)


######################## TEXT PROCESSING UTILITIES ########################
def get_prompt_response(formatted_prompt, model, role):
    """Returns the prompt response"""
    client = MistralClient(api_key=MISTRAL_CREDS["api_key"])
    message = ChatMessage(role=role, content=formatted_prompt)
    response = client.chat(model=model, messages=[message])
    return response


def get_language(input_body, input_subject) -> str:
    """Returns the primary language used in the email"""

    template = """Given an email with subject: '{input_subject}' and body: '{input_body}',
    IDENTIFY the primary language used (e.g: French, English, Russian), prioritizing the body over the subject.
    
    Provide ONLY the answer in JSON format with the key 'language' (STRING).
    """
    model = "mistral-small-latest"
    role = "user"
    formatted_prompt = template.format(
        input_body=input_body, input_subject=input_subject
    )
    response = get_prompt_response(formatted_prompt, model, role)
    clear_text = response.choices[0].message.content.strip()
    language = json.loads(clear_text)["language"]

    print(f"{Fore.LIGHTBLUE_EX}The language used is: {language}")

    return language


def count_corrections(
    original_subject, original_body, corrected_subject, corrected_body
):
    """Count and compare corrections in original and corrected texts"""

    # Splitting the original and corrected texts into words
    original_subject_words = original_subject.split()
    corrected_subject_words = corrected_subject.split()
    original_body_words = original_body.split()
    corrected_body_words = corrected_body.split()

    # Counting the differences in the subject
    subject_corrections = sum(
        1
        for orig, corr in zip(original_subject_words, corrected_subject_words)
        if orig != corr
    )

    # Counting the differences in the body
    body_corrections = sum(
        1
        for orig, corr in zip(original_body_words, corrected_body_words)
        if orig != corr
    )

    # Total corrections
    total_corrections = subject_corrections + body_corrections

    return total_corrections


def extract_contacts_recipients(query):
    template = """"As an intelligent email assistant, analyze the input: '{query}' to categorize email recipients into main, cc, and bcc categories based on the presence of keywords and context that suggest copying or blind copying.

    Guidelines for classification:
    - Main recipients: recipients name directly mentioned or implied to be the primary audience, without specific indicators for copying.
    - CC (carbon copy): recipients explicitly identified through the context of being copied on an email.
    - BCC (blind carbon copy): recipients explicitly identified through the context of a need for discretion or privacy in copying.
    
    ---
    Do NOT provide explanations
    Answer must ONLY be a Json format matching this template:
    {{
        main_recipients: [Python list],
        cc_recipients: [Python list],
        bcc_recipients: [Python list]
    }}
    """
    model = "mistral-small-latest"
    role = "user"
    formatted_prompt = template.format(query=query)
    response = get_prompt_response(formatted_prompt, model, role)
    response_text = response.choices[0].message.content.strip()
    recipients = json.loads(response_text)

    # Extract information based on markers
    main_recipients = recipients.get("main_recipients", [])
    cc_recipients = recipients.get("cc_recipients", [])
    bcc_recipients = recipients.get("bcc_recipients", [])

    print(f"{Fore.CYAN}Main Recipients: {main_recipients}")
    print(f"{Fore.BLUE}Carbon Copy: {cc_recipients}")
    print(f"{Fore.GREEN}Blind Carbon Copy: {bcc_recipients}")

    return main_recipients, cc_recipients, bcc_recipients


# ----------------------- PREPROCESSING REPLY EMAIL -----------------------#
def generate_response_keywords(input_email, input_subject, language) -> list:
    """Generate a list of keywords for responding to a given email."""

    template = """As an email assistant, and given the email with subject: '{input_subject}' and body: '{input_email}' written in {language}.

    IDENTIFY up to 4 different ways to respond to this email.
    USE as few verbs in {language} as possible while keeping a relevant meaning.
    KEYWORDS must look like buttons the user WILL click to reply to the email.

    Answer must be a list (Python) format:  ["...", "..."]
    """
    model = "mistral-small-latest"
    role = "user"
    formatted_prompt = template.format(
        input_subject=input_subject, input_email=input_email, language=language
    )
    response = get_prompt_response(formatted_prompt, model, role)
    keywords = response.choices[0].message.content.strip()

    print(f"{Fore.YELLOW}{keywords}")

    keywords_list = ast.literal_eval(keywords)

    return keywords_list


######################## WRITING ########################
def improve_email_writing(body, subject):
    """Enhance email subject and body"""

    language = get_language(body, subject).upper()

    template = f"""As an email assistant, enhance the subject and body of this email in both QUANTITY and QUALITY in {language}, while preserving key details from the original version.
    
    Answer must be a Json format with two keys: subject (STRING) AND body (HTML)

    subject: {subject},
    body: {body}
    """
    model = "mistral-small-latest"
    role = "user"
    response = get_prompt_response(template, model, role)
    clear_text = response.choices[0].message.content.strip()

    result_json = json.loads(clear_text)

    subject_text = result_json["subject"]
    email_body = result_json["body"]

    print(f"{Fore.CYAN}EMAIL DRAFT IMPROVED:")
    print(f"{Fore.GREEN}Subject: {subject_text}")
    print(f"{Fore.CYAN}Email Body: {email_body}")

    return email_body, subject_text


def new_mail_recommendation(
    mail_content, email_subject, user_recommendation, language="FRENCH"
):
    """Enhance email subject and body based on user guideline"""

    template = f"""As an email assistant, enhance the subject and body of this email in both QUANTITY and QUALITY in {language} according to the user guideline: '{user_recommendation}', while preserving key details from the original version.
    
    Answer must be a Json format with two keys: subject (STRING) AND body (HTML)

    subject: {email_subject},
    body: {mail_content}
    """
    model = "mistral-small-latest"
    role = "user"
    response = get_prompt_response(template, model, role)
    clear_text = response.choices[0].message.content.strip()

    # TODO: handle when the response is not a json format with an algorithm
    result_json = json.loads(clear_text)
    subject_text = result_json["subject"]
    email_body = result_json["body"]

    print(f"{Fore.CYAN}NEW EMAIL RECOMMENDATION:")
    print(f"{Fore.GREEN}Subject: {subject_text}")
    print(f"{Fore.LIGHTGREEN_EX}Email Body: {email_body}")

    return subject_text, email_body


def generate_email(input_data, length, formality, language="FRENCH"):
    """Generate an email, enhancing both QUANTITY and QUALITY according to user guidelines."""

    template = f"""As an email assistant, write a {length} and {formality} email in {language}.
    Improve the QUANTITY and QUALITY in {language} according to the user guideline: '{input_data}', it should strictly contain only the information present in the input.

    Answer must be a Json format with two keys: subject (STRING) AND body IN HTML FORMAT (HTML)
    """
    model = "mistral-small-latest"
    role = "user"
    response = get_prompt_response(template, model, role)

    clear_text = response.choices[0].message.content.strip()
    result_json = json.loads(clear_text)

    subject_text = result_json.get("subject")
    email_body = result_json.get("body")

    print(f"{Fore.CYAN}{length} and {formality} email suggestion:")
    print(f"{Fore.GREEN}Subject: {subject_text}")
    print(f"{Fore.CYAN}Email Body: {email_body}")

    return subject_text, email_body


def correct_mail_language_mistakes(body, subject):
    """Corrects spelling and grammar mistakes in the email subject and body based on user's request."""

    language = get_language(body, subject).upper()

    template = f"""As an email assistant, check the following {language} text for any grammatical or spelling errors and correct them, Do not change any words unless they are misspelled or grammatically incorrect.
    
    Answer must be ONLY a Json format with two keys: subject (STRING) AND body (HTML)

    subject: {subject},
    body: {body}
    """
    model = "mistral-small-latest"
    role = "user"
    response = get_prompt_response(template, model, role)
    clear_text = response.choices[0].message.content.strip()

    result_json = json.loads(clear_text)

    corrected_subject = result_json["subject"]
    corrected_body = result_json["body"]

    print(f"{Fore.CYAN}EMAIL CORRECTED:")
    print(f"{Fore.GREEN}Subject: {corrected_subject}")
    print(f"{Fore.CYAN}Email Body: {corrected_body}")

    num_corrections = count_corrections(
        subject, body, corrected_subject, corrected_body
    )

    return corrected_subject, corrected_body, num_corrections


def improve_email_copywriting(email_subject, email_body):
    """Provides feedback and suggestions for improving the copywriting in the email subject and body."""

    language = get_language(email_body, email_subject)

    template = f"""Evaluate the quality of copywriting in both the subject and body of this email in {language}. Provide feedback and improvement suggestions.

    Email Subject:
    "{email_subject}"

    Email Body:
    "{email_body}"

    ---

    <strong>Subject Feedback</strong>:
    [Your feedback on the subject]

    <strong>Suggestions for the Subject</strong>:
    [Your suggestions for the subject]

    <strong>Email Body Feedback</strong>:
    [Your feedback on the email body]

    <strong>Suggestions for the Email Body</strong>:
    [Your suggestions for the email body]
    """
    model = "mistral-small-latest"
    role = "user"
    response = get_prompt_response(template, model, role)
    feedback_ai = response.choices[0].message.content.strip()

    print(f"{Fore.CYAN}EMAIL COPYWRITING:")
    print(f"{Fore.GREEN}{feedback_ai}")

    return feedback_ai


def generate_email_response(input_subject, input_body, response_type, language):
    """Generates an email response based on the given response type"""
    template = f"""Based on the email with the subject: '{input_subject}' and body: '{input_body}' craft a response in {language} following the '{response_type}' instruction. Ensure the response is structured as an HTML email. Here is a template to follow, with placeholders for the dynamic content:
    <p>[Insert greeting]</p><!-- Insert response here based on the input body and the specified response type --><p>[Insert sign_off],</p><p>[Your Name]</p>

    ----

    Answer must be above HTML without spaces
    """
    # DO NOT DELETE : possible upgrade TO TEST (something like this in the template) : craft a response in {language} following the '{response_type}' instruction, do not invent new demands that the user didn't ask, ONLY IF NECESSARY you can leave blank space after ':' if you want the user to manually complete the answer
    model = "mistral-small-latest"
    role = "user"
    response = get_prompt_response(template, model, role)
    body = response.choices[0].message.content.strip()

    print(f"{Fore.GREEN}[REPLY] body: {body}")

    return body


####################################################################
######################## UNDER CONSTRUCTION ########################
####################################################################


def categorize_and_summarize_email(
    subject: str,
    decoded_data: str,
    category_dict: dict,
    user_description: str,
    language="French",
):
    """Categorizes and summarizes an email"""

    category_dict.pop(DEFAULT_CATEGORY)

    importance_list = {
        "Important": "Messages that are high priority, require immediate attention or action, and are relevant to the user.",
        "Information": "Details that are relevant and informative to the user but may not necessarily require immediate action.",
        "Useless": "Messages that are not relevant to the user, are redundant, do not provide significant value, or are unsolicited newsletters or commercial offers. If uncertain, it's preferable to categorize the message as 'Useless' because the user can correct the classification later.",
    }
    response_list = {
        "Answer Required": "Message requires an answer.",
        "Might Require Answer": "Message might require an answer.",
        "No Answer Required": "No answer is required.",
    }
    relevance_list = {
        "Highly Relevant": "Message is highly relevant to the recipient.",
        "Possibly Relevant": "Message might be relevant to the recipient.",
        "Not Relevant": "Message is not relevant to the recipient.",
    }

    template = f"""Given the following email:

    Subject:
    {subject}

    Text:
    {decoded_data}

    Description:
    {user_description}

    Using the provided categories:

    Topic Categories:
    {category_dict}

    Importance Categories:
    {importance_list}

    Response Categories:
    {response_list}

    Relevance Categories:
    {relevance_list}

    1. Please categorize the email by topic, importance, response, and relevance corresponding to the user description.
    2. In {language}: Summarize the following message
    3. In {language}: Provide a short sentence summarizing the email.

    ---
    Answer must be a Json format matching this template:
    {{
        "topic": Topic Title Category,
        "response": Response Category,
        "relevance": Relevance Category,
        "summary": {{
            "one_line": One-Sentence Summary in {language},
            "complete": [
                "Short Bullet Point 1",
                "Short Bullet Point 2",
                ...
            ]
        }},
        "importance": {{
            "Important": Percentage for Important,
            "Information": Percentage for Information,
            "Useless": Percentage for Useless
        }}
    }}
    """
    model = "mistral-small-latest"
    role = "user"
    response = get_prompt_response(template, model, role)
    clear_response = response.choices[0].message.content.strip()
    result_json = json.loads(clear_response)

    print(result_json)

    topic = result_json["topic"]
    response = result_json["response"]
    relevance = result_json["relevance"]
    short_sentence = result_json["summary"]["one_line"]
    summary_list = result_json["summary"]["complete"]
    importance_dict = result_json["importance"]

    # convert percentages to int
    for key, value in importance_dict.items():
        importance_dict[key] = int(value)

    return (
        topic,
        importance_dict,
        response,
        summary_list,
        short_sentence,
        relevance,
    )


def search_emails(query: str, language: str = "French") -> dict:
    """Searches emails based on the user query and generates structured JSON response."""

    today = datetime.now().strftime("%m-%d-%Y")

    template = f"""As a smart email assistant and based on the user query: '{query}'. Knowing today's date: {today}
    1. Analyse and create a filter to search emails content with the Gmail API and Graph API.
    2. If nothing special is specified, 'from', 'to', 'subject', 'body' MUST have the same value as the most relevant keyword. By default, search in 'read', 'unread' emails
    3. Regarding keywords, provide ONLY individual words. Sentences are not allowed unless explicitly mentioned. If you're unsure, list every relevant word separately.
    4. If and only if a date is explicitely provided by the user; add it to the output using this format: MM/DD/YYYY. Otherwise leave it as an empty string if you hesitate.
    
    ---
    Answer must ONLY be a Json format matching this template in {language} WITHOUT giving any explanation:
    {{
        closeness_percentage: int,
        max_results: int - default 100,
        from: "",
        to: [],
        subject: "",
        body: "",
        filenames: [filenames OR extensions following (a-z0-9)],
        date_from: "",
        keywords: [],
        search_in: {{
            "read": boolean,
            "unread": boolean,
            "drafts": boolean,
            "sent_emails": boolean,
            "deleted_emails": boolean,
            "spams": boolean
        }}
    }}
    """
    model = "mistral-small"
    role = "user"
    response = get_prompt_response(template, model, role)
    clear_response = response.choices[0].message.content.strip()

    print(clear_response)

    queries_dict = json.loads(clear_response)

    return queries_dict
