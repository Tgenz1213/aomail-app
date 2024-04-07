"""
Handles prompt engineering requests for Claude 3 API.
"""

import ast
import json
import anthropic
from colorama import Fore, init
from MailAssistant.constants import CLAUDE_CREDS, DEFAULT_CATEGORY, HUMAN, ASSISTANT


######################## Claude 3 API SETTINGS ########################
init(autoreset=True)


######################## TEXT PROCESSING UTILITIES ########################
def get_prompt_response(formatted_prompt):
    """Returns the prompt response"""
    client = anthropic.Anthropic(api_key=CLAUDE_CREDS["api_key"])
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0.0,
        messages=[{"role": "user", "content": formatted_prompt}],
    )
    return response


def get_language(input_body, input_subject) -> str:
    """Returns the primary language used in the email"""

    formatted_prompt = f"""{HUMAN}Given an email with subject: '{input_subject}' and body: '{input_body}',
    IDENTIFY the primary language used (e.g: French, English, Russian), prioritizing the body over the subject.
    
    Provide ONLY the answer in JSON format with the key 'language' (STRING).    
    {ASSISTANT}"""
    response = get_prompt_response(formatted_prompt)
    language = json.loads(response.content[0].text)["language"]

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
    formatted_prompt = f"""{HUMAN}As an intelligent email assistant, analyze the input to categorize email recipients into main, cc, and bcc categories based on the presence of keywords and context that suggest copying or blind copying. Here's the input: '{query}'.

    Guidelines for classification:
    - Main recipients are those directly mentioned or implied to be the primary audience, without specific indicators for copying.
    - CC (carbon copy) recipients are identified through the context or subtle cues that imply they should be informed of the communication. Look for any keywords or phrases, even if indirectly stated, that traditionally associate with copying someone on an email.
    - BCC (blind carbon copy) recipients are identified similarly by context or cues suggesting a need for discretion or privacy in copying, without directly mentioning them in the conversation.

    If the input does not clearly differentiate between main, cc, and bcc recipients, use intuitive rules and a careful analysis of the text structure and any potential copying-related keywords or implications:
    1. Names appearing first or separated by phrases indicating inclusion (e.g., 'and', 'et') without clear copying context are considered as main recipients.
    2. Utilize any linguistic or structural clues to infer if a recipient is intended for CC or BCC, focusing on the broader context rather than explicit markers

    Return ONLY the results in JSON format with three keys:
    main_recipients: [Python list],
    cc_recipients: [Python list],
    bcc_recipients: [Python list]    
    {ASSISTANT}"""
    response = get_prompt_response(formatted_prompt)
    recipients = json.loads(response.content[0].text)

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

    formatted_prompt = f"""{HUMAN}As an email assistant, and given the email with subject: '{input_subject}' and body: '{input_email}' written in {language}.

    IDENTIFY up to 4 different ways to respond to this email. Only identify relevant way to respond if you can't find 4 different ways only give 2 or 3 ways to respond.
    USE few words in {language} while keeping a relevant meaning.
    KEYWORDS must look like buttons the user WILL click to reply to the email.

    ---

    As an answer ONLY give a Python List format: ["...", "..."] dont use any other caracters otherwise it will create errors
    {ASSISTANT}"""
    response = get_prompt_response(formatted_prompt)
    keywords = response.content[0].text.strip()

    print(f"{Fore.YELLOW}{keywords}")

    keywords_list = ast.literal_eval(keywords)

    return keywords_list


######################## WRITING ########################
def improve_email_writing(body, subject):
    """Enhance email subject and body"""

    language = get_language(body, subject).upper()

    formatted_prompt = f"""{HUMAN}As an email assistant, enhance the subject and body of this email in both QUANTITY and QUALITY in {language}, while preserving key details from the original version.
    
    Answer must be a Json format with two keys: subject (STRING) AND body (HTML)

    subject: {subject},
    body: {body}
    {ASSISTANT}"""
    response = get_prompt_response(formatted_prompt)
    result_json = json.loads(response.content[0].text.strip())

    subject_text = result_json["subject"]
    email_body = result_json["body"]

    print(f"{Fore.CYAN}EMAIL DRAFT IMPROVED:")
    print(f"{Fore.GREEN}Subject: {subject_text}")
    print(f"{Fore.CYAN}Email Body: {email_body}")

    return email_body, subject_text

def new_mail_recommendation(mail_content, email_subject, user_recommendation, language="FRENCH"):
    """Enhance email subject and body based on user guideline"""

    template = f"""{HUMAN}As an email assistant, enhance the subject and body of this email in both QUANTITY and QUALITY in {language} according to the user guideline: '{user_recommendation}', while preserving key details from the original version.
    
    Answer must be a Json format with two keys: subject (STRING) AND body (HTML)

    subject: {email_subject},
    body: {mail_content}
    {ASSISTANT}"""
    response = get_prompt_response(template)
    clear_text = response.content[0].text.strip()

    # TODO: handle when the response is not a json format with an algorithm
    result_json = json.loads(clear_text)
    subject_text = result_json["subject"]
    email_body = result_json["body"]

    print(f"{Fore.CYAN}NEW EMAIL RECOMMENDATION:")
    print(f"{Fore.GREEN}Subject: {subject_text}")
    print(f"{Fore.LIGHTGREEN_EX}Email Body: {email_body}")

    return subject_text, email_body


''' OLD Ask Theo Before Delete'''
def generate_email(input_data, length, formality, language="FRENCH"):
    """Generate an email, enhancing both QUANTITY and QUALITY according to user guidelines."""

    template = f"""{HUMAN}As an email assistant, write a {length} and {formality} email in {language}.
    Improve the QUANTITY and QUALITY in {language} according to the user guideline: '{input_data}', it should strictly contain only the information present in the input.

    Answer must be ONLY a Json format with two keys: subject (STRING) AND body IN HTML FORMAT
    {ASSISTANT}"""
    response = get_prompt_response(template)
    clear_text = response.content[0].text.strip()

    print(clear_text)
    
    result_json = json.loads(clear_text)

    subject_text = result_json.get("subject")
    email_body = result_json.get("body")

    print(f"{Fore.CYAN}{length} and {formality} email suggestion:")
    print(f"{Fore.GREEN}Subject: {subject_text}")
    print(f"{Fore.CYAN}Email Body: {email_body}")

    return subject_text, email_body

''' IN DEV => DO NOT DELETE OR IMPLEMENT => Reserved for Theo => Ask Theo if you want to delete
def generate_email(input_data, length, formality, language="FRENCH"):
    """Generate an email, enhancing both QUANTITY and QUALITY according to user guidelines."""

    input_word_count = len(input_data.split())

    if length == "very short":
        word_count_factor = 1.0
    elif length == "short":
        word_count_factor = 1.5
    else:  # "long"
        word_count_factor = 3.0

    word_count = int(input_word_count * word_count_factor)
    word_count_range = f"{word_count - 20}-{word_count + 20} words"

    template = f"""{HUMAN}As an email assistant, write a {formality} email in {language} with a length of {word_count_range}.
    Improve the QUANTITY and QUALITY in {language} according to the user guideline: '{input_data}', it should strictly contain only the information present in the input.

    Answer must be ONLY a Json format with two keys: subject (STRING) AND body IN HTML FORMAT (HTML)
    {ASSISTANT}"""
    response = get_prompt_response(template)
    clear_text = response.content[0].text.strip()

    result_json = json.loads(clear_text)

    subject_text = result_json.get("subject")
    email_body = result_json.get("body")

    print(f"{Fore.CYAN}{length} and {formality} email suggestion:")
    print(f"{Fore.GREEN}Subject: {subject_text}")
    print(f"{Fore.CYAN}Email Body: {email_body}")

    return subject_text, email_body'''


def correct_mail_language_mistakes(body, subject):
    """Corrects spelling and grammar mistakes in the email subject and body based on user's request."""

    language = get_language(body, subject).upper()

    formatted_prompt = f"""{HUMAN}As an email assistant, check the following {language} text for any grammatical or spelling errors and correct them, Do not change any words unless they are misspelled or grammatically incorrect.
    
    Answer must be a Json format with two keys: subject (STRING) AND body (HTML)

    subject: {subject},
    body: {body}
    """
    response = get_prompt_response(formatted_prompt)
    clear_text = response.content[0].text.strip()
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

    template = f"""{HUMAN}Evaluate the quality of copywriting in both the subject and body of this email in {language}. Provide feedback and improvement suggestions.

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
    {ASSISTANT}
    """
    response = get_prompt_response(template)
    feedback_ai = response.content[0].text.strip()

    print(f"{Fore.CYAN}EMAIL COPYWRITING:")
    print(f"{Fore.GREEN}{feedback_ai}")

    return feedback_ai


def generate_email_response(input_subject, input_body, response_type, language):
    """Generates an email response based on the given response type"""
    template = f"""{HUMAN}Based on the email with the subject: '{input_subject}' and body: '{input_body}' craft a response in {language} following the '{response_type}' instruction. Ensure the response is structured as an HTML email. Here is a template to follow, with placeholders for the dynamic content:
    <p>[Insert greeting]</p><!-- Insert response here based on the input body and the specified response type --><p>[Insert sign_off],</p><p>[Your Name]</p>

    ----

    Answer must be above HTML without spaces
    {ASSISTANT}
    """
    # DO NOT DELETE : possible upgrade TO TEST (something like this in the template) : craft a response in {language} following the '{response_type}' instruction, do not invent new demands that the user didn't ask, ONLY IF NECESSARY you can leave blank space after ':' if you want the user to manually complete the answer
    response = get_prompt_response(template)
    body = response.content[0].text.strip()

    print(f"{Fore.GREEN}[REPLY] body: {body}")

    return body


####################################################################
######################## UNDER CONSTRUCTION ########################
####################################################################


def categorize_and_summarize_email(
    subject: str, decoded_data: str, category_dict: dict, user_description: str, language="French"
):
    """Categorizes and summarizes an email"""

    category_dict.pop(DEFAULT_CATEGORY)

    ''' OLD v1 Ask Theo before DELETE
    importance_list = {
        "Important": 'Items or messages that are of high priority, do not contain offers to "unsubscribe", and require immediate attention or action.',
        "Information": 'Details that are relevant and informative but may not require immediate action. Does not contain offers to "unsubscribe".',
        "Useless": 'Items or messages that contain offers to "unsubscribe", might not be relevant to all recipients, are redundant, or do not provide any significant value.',
    }'''
    ''' OLD v2 Ask Theo before DELETE
    importance_list = {
        "Important": "Messages that are high priority, require immediate attention or action, and are relevant to the user.",
        "Information": "Details that are relevant and informative to the user but may not necessarily require immediate action.",
        "Useless": "Messages that are not relevant to the user, are redundant, do not provide significant value, or are newsletters or commercial offers. If uncertain, it's preferable to categorize the message as 'Useless' because the user can correct the classification later.",
    }'''
    ''' OLD v3 Ask Theo before DELETE
    importance_list = {
        "Important": "Messages that are high priority, require immediate attention or action, and are relevant to the user.",
        "Information": "Details relevant to the user's work interests or needs, such as professional updates, professional news, or professional content.",
        "Promotional": "Messages that contain offers, deals, or advertisements from services, stores, or subscriptions the user has interacted with.",
        "News": "Messages that contain information not related to work, insights, news, often with options to subscribe or unsubscribe",
    }'''
    ''' OLD v4 Ask Theo before DELETE
    importance_list = {
        "Important": "Messages that are high priority and require immediate attention or action (truly relevant to the user).",
        "WorkInformation": "Messages relevant to the user's work interests or needs, such as professional updates, professional news, or professional content.",
        "Promotional": "Messages that contain offers, deals, or advertisements from services, stores, or subscriptions the user has interacted with.",
        "News": "Messages that contain information not related to work, insights, news, often with options to subscribe or unsubscribe",
    }'''
    importance_list = {
        "UrgentWorkInformation": "Critical updates or information requiring immediate attention related to projects, deadlines, or time-sensitive matters.",
        "RoutineWorkUpdates": "Regular updates or communications important for work but not requiring immediate action, such as team updates or general announcements.",
        "InternalCommunications": "Internal company matters including policy updates, HR announcements, or events.",
        "Promotional": "Messages that contain offers, deals, or advertisements from services, stores, or subscriptions the user has interacted with.",
        "News": "Messages that contain information not related to work, insights, news, often with options to subscribe or unsubscribe",
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

    template = f"""{HUMAN}Given the following email:

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

    1. Please categorize the email by topic, importance, response, and relevance corresponding to the user description. (regarding the topic category, you need to be sure of the choice made, if you hesitate put it in the Others category)
    2. In {language}: Summarize the following message
    3. In {language}: Provide a short sentence summarizing the email.
    Remember, regardless of the email's perceived relevance or importance, a summary is always required. This summary should objectively reflect the content of the email without making subjective judgments about its relevance.

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
            "UrgentWorkInformation": Percentage for UrgentWorkInformation,
            "RoutineWorkUpdates": Percentage for RoutineWorkUpdates,
            "InternalCommunications": Percentage for InternalCommunications,
            "Promotional": Percentage for Promotional,
            "News": Percentage for News 
        }}
    }}
    {ASSISTANT}
    """
    response = get_prompt_response(template)
    clear_response = response.content[0].text.strip()
    result_json = json.loads(clear_response)

    print(result_json)

    topic_category = result_json["topic"]
    response_category = result_json["response"]
    relevance_category = result_json["relevance"]
    short_sentence = result_json["summary"]["one_line"]
    summary_list = result_json["summary"]["complete"]
    importance_dict = result_json["importance"]

    # convert percentages to int
    for key, value in importance_dict.items():
        importance_dict[key] = int(value)

    return (
        topic_category,
        importance_dict,
        response_category,
        summary_list,
        short_sentence,
        relevance_category,
    )
