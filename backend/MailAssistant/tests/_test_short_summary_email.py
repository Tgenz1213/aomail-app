"""
Template to summarize an email instead of bullet points
"""


import json
import anthropic
from backend.MailAssistant.ai_providers.claude import count_tokens
from backend.MailAssistant.constants import CLAUDE_CREDS


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