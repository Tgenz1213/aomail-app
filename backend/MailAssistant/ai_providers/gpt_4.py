"""
Handles prompt engineering requests for GPT-4 API.

⚠️ Some functions are outdated ⚠️
"""

import json
import openai
from colorama import Fore, init
from . import gpt_3_5_turbo
from MailAssistant.constants import OPENAI_CREDS, DEFAULT_CATEGORY


######################## GPT - 4 API SETTINGS ########################
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


def categorize_and_summarize_email(
    subject: str,
    decoded_data: str,
    category_dict: dict,
    user_description: str,
    language="French",
):
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
    2. In {language}: Summarize the following email using description nouns or infinitive verbs structures according to the information for each bullet point.
    3. In {language}: Provide up to 5 (according to email length) short bullet points WITHOUT making any judgment or interpretation, they should be clear and as short as possible. Do NOT add any redundant information and SPEAK ONLY about the content NOT about the name of the sender or greetings or unecessary details.
    4. In {language}: Provide a VERY SHORT sentence summarizing the core content of the email without giving ANY details.
    Remember, regardless of the email's perceived relevance or importance, a summary is always required. This summary should objectively reflect the content of the email without making subjective judgments about its relevance.

    ---
    Answer must be a Json format (without ) matching this template:
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
    """
    response = get_prompt_response(template)
    clear_response = response.choices[0].message.content.strip()
    if "```json" in clear_response:
        clear_response = clear_response.removeprefix("```json")
        clear_response = clear_response.removesuffix("```")

    print("GPT 4 turbo")
    print(clear_response)

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
