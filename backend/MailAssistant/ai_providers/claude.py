"""
Handles prompt engineering requests for Claude 3 API.

TODO:
- Clean the code with doc + datatypes
- Remove all unecessary functions
- Write an list of all supported function in the banner of that file like
    - search emails: ✅
    - feature 2: ⚒️
"""

import ast
import json
import anthropic
from datetime import datetime
import tiktoken
from MailAssistant.constants import CLAUDE_CREDS


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


def count_tokens(text: str) -> int:
    """Calculates the number of tokens in a given text string using the provided tokenizer."""
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(text))
    return num_tokens


def get_language(input_body, input_subject) -> str:
    """Returns the primary language used in the email"""

    formatted_prompt = f"""Given an email with subject: '{input_subject}' and body: '{input_body}',
    IDENTIFY the primary language used (e.g: French, English, Russian), prioritizing the body over the subject.
    
    Provide ONLY the answer in JSON format with the key 'language' (STRING).    
    """
    response = get_prompt_response(formatted_prompt)
    language = json.loads(response.content[0].text)["language"]

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


def extract_contacts_recipients(query) -> dict[str:list]:
    formatted_prompt = f"""As an intelligent email assistant, analyze the input to categorize email recipients into main, cc, and bcc categories based on the presence of keywords and context that suggest copying or blind copying. Here's the input: '{query}'.

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
    """
    response = get_prompt_response(formatted_prompt)
    recipients: dict = json.loads(response.content[0].text)

    main_recipients = recipients.get("main_recipients", [])
    cc_recipients = recipients.get("cc_recipients", [])
    bcc_recipients = recipients.get("bcc_recipients", [])

    return main_recipients, cc_recipients, bcc_recipients


# ----------------------- PREPROCESSING REPLY EMAIL -----------------------#
def generate_response_keywords(input_email, input_subject) -> list:
    """Generate a list of keywords for responding to a given email."""

    language = get_language(input_email, input_subject)

    formatted_prompt = f"""As an email assistant, and given the email with subject: '{input_subject}' and body: '{input_email}' written in {language}.

    IDENTIFY up to 4 different ways to respond to this email. Only identify relevant way to respond if you can't find 4 different ways only give 2 or 3 ways to respond.
    USE few words in {language} while keeping a relevant meaning ONLY if you are sure that keyword is relevant, if you HESITATE do not add it.
    KEYWORDS must look like ACTIONS buttons the user WILL click to reply to the email.

    ---
    As an answer ONLY give a Python List format: ["...", "..."] dont use any other caracters otherwise it will create errors. Do not give ANY explanations, RETURN only the list.
    """
    response = get_prompt_response(formatted_prompt)
    keywords = response.content[0].text.strip()
    keywords_list = ast.literal_eval(keywords)

    return keywords_list


######################## WRITING ########################
# TODO: remove HARD CODED language
def generate_email(input_data, length, formality, language):
    """Generate an email, enhancing both QUANTITY and QUALITY according to user guidelines."""

    template = f"""As an email assistant, write a {length} and {formality} email in {language}.
    Improve the QUANTITY and QUALITY in {language} according to the user guideline: '{input_data}'.
    It must strictly contain only the information that is present in the input.
    Add a standard greeting and sign-off without a signature (unless explicitly mentioned) if nothing is specified.
    
    ---
    Answer must ONLY be in JSON format with two keys: subject (STRING) and body in HTML format without spaces and unusual line breaks.
    """
    response = get_prompt_response(template)
    clear_text = response.content[0].text.strip()

    result_json: dict = json.loads(clear_text)
    subject_text = result_json.get("subject")
    email_body = result_json.get("body")

    return subject_text, email_body


def correct_mail_language_mistakes(body, subject):
    """Corrects spelling and grammar mistakes in the email subject and body based on user's request."""

    language = get_language(body, subject).upper()

    formatted_prompt = f"""As an email assistant, check the following {language} text for any grammatical or spelling errors and correct them, Do not change any words unless they are misspelled or grammatically incorrect.
    
    Answer must be a Json format with two keys: subject (STRING) AND body (HTML)

    subject: {subject},
    body: {body}
    """
    response = get_prompt_response(formatted_prompt)
    clear_text = response.content[0].text.strip()
    result_json = json.loads(clear_text)

    corrected_subject = result_json["subject"]
    corrected_body = result_json["body"]

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
    response = get_prompt_response(template)
    feedback_ai = response.content[0].text.strip()

    return feedback_ai


def generate_email_response(
    input_subject: str, input_body: str, user_instruction: str
) -> str:
    """Generates an email response based on the given response type"""

    template = f"""As a smart email assistant and based on the email with the subject: '{input_subject}' and body: '{input_body}'.
    Craft a response strictly in the language used in the email following the user instruction: '{user_instruction}'.
    0. Pay attention if the email appears to be a conversation. You MUST only reply to the last email and do NOT summarize the conversation at all.
    1. Ensure the response is structured as an HTML email. Make sure to create a brief response that is straight to the point unless a contradictory guideline is explicitly mentioned by the user.
    2. Respect the tone employed in the subject and body, as well as the relationship and respectful markers between recipients.
    3. Here is a template to follow, with placeholders for the dynamic content:
    <p>[Insert greeting]</p><html>[Insert the response]</html><p>[Insert sign_off],</p>

    ---
    Answer must be above HTML without spaces
    """
    response = get_prompt_response(template)
    body = response.content[0].text.strip()

    return body


# TODO: finish to implement by merging with the old function
# categorize_and_summarize_email
def new_function_(
    subject: str,
    decoded_data: str,
    category_dict: dict,
    user_description: str,
    sender: str,
    language: str,
) -> tuple[str, str, str, dict[str:str, str:list], dict[str:int]]:
    """Categorizes and summarizes an email"""

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

    template = f"""You are a smart email assistant acting as if you were a secretary, summarizing an email for the recipient orally.
    
    Given the following email:

    Sender:
    {sender}

    Subject:
    {subject}

    Text:
    {decoded_data}

    User description:
    {user_description}

    Using the provided categories:

    Topic Categories:
    {category_dict}

    Response Categories:
    {response_list}

    Relevance Categories:
    {relevance_list}

    Complete the following tasks in {language}:
    - Categorize the email according to the user description (if provided) and given categories.
    - Summarize the email without adding any greetings.
    - If the email appears to be a response or a conversation, summarize only the last email and IGNORE the previous ones.
    - The summary should objectively reflect the most important information of the email without making subjective judgments.
    - If the email is explicitely mentionning the name of the user (provided with user description), then use 'You' instead of the name of the user.
    
    ---
    Answer must always be a Json format matching this template:
    {{
        "topic": Topic Title Category,
        "response": Response Category,
        "relevance": Relevance Category,
        "summary": Summary of the email
    }}"""
    response = get_prompt_response(template)

    print("=====================NUMBER OF TOKENS INPUT=========================")
    print(count_tokens(template))

    clear_response = response.content[0].text.strip()

    print("=====================NUMBER OF TOKENS OUTPUT =========================")
    print(count_tokens(clear_response))

    print("Claude categorize_and_summarize_email")
    print(clear_response)

    result_json = json.loads(clear_response)

    topic_category = result_json["topic"]
    response_category = result_json["response"]
    relevance_category = result_json["relevance"]
    summary = result_json["summary"]

    return (
        topic_category,
        response_category,
        summary,
        relevance_category,
    )


# TODO: remove HARD CODED language
def search_emails(query: str, language: str) -> dict:
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
        from: [],
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
    }}"""
    response = get_prompt_response(template)
    clear_response = response.content[0].text.strip()
    queries_dict = json.loads(clear_response)

    return queries_dict


###########################################################
######################## TO DELETE ########################
###########################################################


# TO DELETE
def categorize_and_summarize_email(
    subject: str,
    decoded_data: str,
    category_dict: dict,
    user_description: str,
    language: str = "French",
) -> tuple[str, str, str, dict[str:str, str:list], dict[str:int]]:
    """Categorizes and summarizes an email"""

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

    template = f"""Given the following email:

    Subject:
    {subject}

    Text:
    {decoded_data}

    User description:
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

    Complete the following tasks in {language}:
    - Categorize the email according to the user description (if provided) and given categories.
    - If the email appears to be a response or a conversation, summarize only the last email and IGNORE the previous ones. There is no need to summarize the topic as it is given in the short sentence.
    - Provide a short sentence (up to 10 words) summarizing the core content of the email.
    - The summary should objectively reflect the most important information of the email without making subjective judgments.
    - Bullet points MUST strictly be different from the short sentence summary.
    - If the email is explicitely mentionning the name of the user (provided with user description), then use 'You' instead of the name of the user.
    - Provide up to 5 (according to email length and relevance) short bullet points WITHOUT making any judgment or interpretation. They should be clear and concise (max 10 words).
    - Every bullet point MUST be unique and useful for the user to help him save time. If several bullet points express the same idea, keep only the best one.

    ---
    Answer must always be a Json format matching this template:
    {{
        "topic": Topic Title Category,
        "response": Response Category,
        "relevance": Relevance Category,
        "summary": {{
            "one_line": Short sentence summary,
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
    }}"""

    print("=====================NUMBER OF TOKENS INPUT=========================")
    print(count_tokens(template))
    response = get_prompt_response(template)
    clear_response = response.content[0].text.strip()

    # print("Claude")
    # print(clear_response)

    print("=====================NUMBER OF TOKENS OUTPUT =========================")
    print(count_tokens(clear_response))

    result_json = json.loads(clear_response)

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

    template = f"""As an email assistant, write a {formality} email in {language} with a length of {word_count_range}.
    Improve the QUANTITY and QUALITY in {language} according to the user guideline: '{input_data}', it should strictly contain only the information present in the input.

    Answer must be ONLY a Json format with two keys: subject (STRING) AND body IN HTML FORMAT (HTML)
    """
    response = get_prompt_response(template)
    clear_text = response.content[0].text.strip()

    result_json = json.loads(clear_text)

    subject_text = result_json.get("subject")
    email_body = result_json.get("body")

    print(f"{Fore.CYAN}{length} and {formality} email suggestion:")
    print(f"{Fore.GREEN}Subject: {subject_text}")
    print(f"{Fore.CYAN}Email Body: {email_body}")

    return subject_text, email_body'''
