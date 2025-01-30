"""
Handles prompt engineering requests for Gemini 1.5 Flash API.

Features:
- ✅ extract_contacts_recipients: Categorizes email recipients.
- ✅ generate_response_keywords: Suggests keywords for email responses.
- ✅ generate_email: Creates emails per user guidelines.
- ✅ correct_mail_language_mistakes: Fixes spelling and grammar errors.
- ✅ improve_email_copywriting: Suggests improvements for email copywriting.
- ✅ generate_email_response: Crafts responses based on input type.
- ✅ search_emails: Searches and structures email data.
- ✅ categorize_and_summarize_email: Categorizes and summarizes an email.
- ✅ review_user_description: Reviews a user-provided description and provides validation and feedback.
- ✅ generate_categories_scratch: Generates categories based on user topics for email classification.
"""

import re
import ast
import json
import logging
import google.generativeai as genai
from datetime import datetime
from aomail.constants import (
    ANSWER_REQUIRED,
    GEMINI_CREDS,
    HIGHLY_RELEVANT,
    MIGHT_REQUIRE_ANSWER,
    NO_ANSWER_REQUIRED,
    NOT_RELEVANT,
    POSSIBLY_RELEVANT,
)
from aomail.ai_providers.utils import extract_json_from_response


LOGGER = logging.getLogger(__name__)


######################## TEXT PROCESSING UTILITIES ########################
def get_prompt_response(formatted_prompt: str):
    """Returns the prompt response using Gemini 1.5 Flash model"""
    genai.configure(api_key=GEMINI_CREDS["api_key"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        formatted_prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=1000, temperature=0.0
        ),
    )
    return response


def get_prompt_response_exp(formatted_prompt: str):
    """Returns the prompt response using Gemini 2.0 Flash exp model"""
    genai.configure(api_key=GEMINI_CREDS["api_key"])
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    response = model.generate_content(
        formatted_prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=1000, temperature=0.0
        ),
    )
    return response


def count_corrections(
    original_subject: str,
    original_body: str,
    corrected_subject: str,
    corrected_body: str,
) -> int:
    """
    Counts and compares corrections in original and corrected texts.

    Args:
        original_subject (str): The original subject text.
        original_body (str): The original body text.
        corrected_subject (str): The corrected subject text.
        corrected_body (str): The corrected body text.

    Returns:
        int: The total number of corrections made in the subject and body texts.
    """
    original_subject_words = original_subject.split()
    corrected_subject_words = corrected_subject.split()
    original_body_words = original_body.split()
    corrected_body_words = corrected_body.split()

    subject_corrections = sum(
        orig != corr
        for orig, corr in zip(original_subject_words, corrected_subject_words)
    )
    body_corrections = sum(
        orig != corr for orig, corr in zip(original_body_words, corrected_body_words)
    )

    total_corrections = subject_corrections + body_corrections

    return total_corrections


def extract_contacts_recipients(query: str) -> dict[str, list]:
    """
    Analyzes the input query to categorize email recipients into main, CC, and BCC categories.

    Args:
        query (str): The input string containing email recipient information.

    Returns:
        dict[str, list]: A dictionary with three keys:
            'main_recipients': List of main recipients.
            'cc_recipients': List of CC recipients.
            'bcc_recipients': List of BCC recipients.
    """
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
    LOGGER.error(f"DEBUG ---------------------------------------> {response}")
    try:
        result_json = extract_json_from_response(response.text)
    except json.JSONDecodeError as e:
        LOGGER.error(f"JSON Decode Error: {e}")
    result_json["tokens_input"] = response.usage_metadata.prompt_token_count
    result_json["tokens_output"] = response.usage_metadata.candidates_token_count

    return result_json


# ----------------------- PREPROCESSING REPLY EMAIL -----------------------#
def generate_response_keywords(input_email: str, input_subject: str) -> dict:
    """
    Generates a list of detailed draft response sentences for responding to a given email.

    Args:
        input_email (str): The body of the email.
        input_subject (str): The subject of the email.

    Returns:
        dict: A dictionary containing:
            keywords_list (list): A list of detailed draft response sentences for the email.
            tokens_input (int): The number of tokens used for the input.
            tokens_output (int): The number of tokens used for the output.
    """
    formatted_prompt = f"""
    As an email assistant, analyze the email with the subject: '{input_subject}' and body: '{input_email}'.

    IDENTIFY exactly 5 distinct ways to respond. For each scenario:
    **Provide "keywords":** a list of short phrases (fragments) describing the approach. These should **not form complete sentences** but should contain multiple words to effectively convey the strategy. Ensure that the keywords are **in the same language** as the original email. For example:
    - "can't attend 5pm, need new schedule, request confirmation"
    - "appreciate feedback, will implement changes, thank you"

    As an answer ONLY give a Python List format: ["...", "..."]. Do not use any other characters or explanations; RETURN only the list.
    """
    response = get_prompt_response_exp(formatted_prompt)
    keywords_text = response.text.strip()

    try:
        keywords_list = ast.literal_eval(keywords_text)
    except (ValueError, SyntaxError):
        cleaned_text = keywords_text.replace("```", "").replace("python", "").strip()
        keywords_list = ast.literal_eval(cleaned_text)

    return {
        "keywords_list": keywords_list,
        "tokens_input": response.usage_metadata.prompt_token_count,
        "tokens_output": response.usage_metadata.candidates_token_count,
    }


######################## WRITING ########################
def generate_email(
    input_data: str,
    length: str,
    formality: str,
    language: str,
    agent_settings: dict,
    signature: str = "",
) -> dict:
    """
    Generates an email, enhancing both quantity and quality according to user guidelines and agent settings.

    Args:
        input_data (str): The user's input data or guidelines for the email content.
        length (str): The desired length of the email (e.g., "short", "medium", "long").
        formality (str): The desired level of formality for the email (e.g., "informal", "formal").
        language (str): The language in which the email should be written.
        agent_settings (dict): The agent's guidelines and settings to guide AI responses.
        signature (str): Optional HTML signature to append to the email.

    Returns:
        dict: A dictionary containing:
            subject_text (str): The subject of the generated email.
            email_body (str): The body of the generated email in HTML format.
            tokens_input (int): The number of tokens used for the input.
            tokens_output (int): The number of tokens used for the output.
    """
    has_content = bool(signature) and bool(re.sub(r"<[^>]+>", "", signature).strip())
    if has_content:
        signature_instruction = f"\n3. DO NOT modify, remove or create a new signature. Keep this EXACT SAME signature at the end of the email:\n{signature}"
    else:
        signature_instruction = "Add a standard greeting and sign-off without a signature (unless explicitly mentioned).\nSignature: <br>"

    template = f"""As an email assistant, following these agent guidelines: {json.dumps(agent_settings)}, write a {length} and {formality} email in {language}.
    Improve the QUANTITY and QUALITY in {language} according to the user guideline: '{input_data}'.
    It must strictly contain only the information that is present in the input.
    {signature_instruction}

    ---
    Answer must ONLY be in JSON format with two keys: subject (STRING) and body in HTML format without spaces and unusual line breaks.
    """

    response = get_prompt_response_exp(template)
    result_json: dict = extract_json_from_response(response.text)
    subject_text = result_json.get("subject")
    email_body = result_json.get("body")

    return {
        "subject_text": subject_text,
        "email_body": email_body,
        "tokens_input": response.usage_metadata.prompt_token_count,
        "tokens_output": response.usage_metadata.candidates_token_count,
    }


def correct_mail_language_mistakes(body: str, subject: str) -> dict:
    """
    Corrects spelling and grammar mistakes in the email subject and body based on user's request.

    Args:
        body (str): The body of the email to be corrected.
        subject (str): The subject of the email to be corrected.

    Returns:
        dict: A dictionary containing:
            corrected_subject (str): The corrected subject of the email.
            corrected_body (str): The corrected body of the email in HTML format.
            num_corrections (int): The number of corrections made in the email subject and body.
            tokens_input (int): The number of tokens used for the input.
            tokens_output (int): The number of tokens used for the output.
    """

    formatted_prompt = f"""As an email assistant, check the following text for any grammatical or spelling errors and correct them, Do not change any words unless they are misspelled or grammatically incorrect.
    
    Answer must be a Json format with two keys: subject (STRING) AND body (HTML)

    subject: {subject},
    body: {body}
    """
    response = get_prompt_response(formatted_prompt)
    result_json: dict = extract_json_from_response(response.text)

    corrected_subject = result_json["subject"]
    corrected_body = result_json["body"]

    num_corrections = count_corrections(
        subject, body, corrected_subject, corrected_body
    )

    return {
        "correctedSubject": corrected_subject,
        "correctedBody": corrected_body,
        "numCorrections": num_corrections,
        "tokens_input": response.usage_metadata.prompt_token_count,
        "tokens_output": response.usage_metadata.candidates_token_count,
    }


def improve_email_copywriting(email_subject: str, email_body: str) -> dict:
    """
    Provides feedback and suggestions for improving the copywriting in the email subject and body.

    Args:
        email_subject (str): The subject of the email to be evaluated and improved.
        email_body (str): The body of the email to be evaluated and improved.

    Returns:
        dict: A dictionary containing:
            feedback_ai (str): Feedback and suggestions for improving the copywriting in the email subject and body.
            tokens_input (int): The number of tokens used for the input.
            tokens_output (int): The number of tokens used for the output.
    """

    template = f"""Evaluate the quality of copywriting in both the subject and body of this email. Provide feedback and improvement suggestions.

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
    feedback_ai = extract_json_from_response(response.text)

    return {
        "feedback_ai": feedback_ai,
        "tokens_input": response.usage_metadata.prompt_token_count,
        "tokens_output": response.usage_metadata.candidates_token_count,
    }


def generate_email_response(
    input_subject: str,
    input_body: str,
    user_instruction: str,
    agent_settings: dict,
    signature: str = "",
) -> dict:
    """
    Generates an email response based on the given response type and agent settings.

    Args:
        input_subject (str): The subject of the email to respond to.
        input_body (str): The body of the email to respond to.
        user_instruction (str): Instructions or guidelines provided by the user for crafting the response.
        agent_settings (dict): The agent's guidelines and settings to guide AI responses.
        signature (str): Optional HTML signature to append to the email.

    Returns:
        dict: A dictionary containing:
            body (str): The generated email response in HTML format.
            tokens_input (int): The number of tokens used for the input.
            tokens_output (int): The number of tokens used for the output.
    """
    has_content = bool(signature) and bool(re.sub(r"<[^>]+>", "", signature).strip())
    if has_content:
        signature_instruction = f"\n3. DO NOT modify, remove or create a new signature. Keep this EXACT SAME signature at the end of the email:\n{signature}"
    else:
        signature_instruction = "Add a standard greeting and sign-off without a signature (unless explicitly mentioned).\nSignature: <br>"

    template = f"""As a smart email assistant, following these agent guidelines: {json.dumps(agent_settings)}, and based on the email with the subject: '{input_subject}' and body: '{input_body}'.
    Craft a response strictly in the language used in the email following the user instruction: '{user_instruction}'.
    0. Pay attention if the email appears to be a conversation. You MUST only reply to the last email and do NOT summarize the conversation at all.
    1. Ensure the response is structured as an HTML email. Make sure to create a brief response that is straight to the point unless a contradictory guideline is explicitly mentioned by the user.
    2. Respect the tone employed in the subject and body, as well as the relationship and respectful markers between recipients.
    {signature_instruction}

    ---
    Answer must ONLY be in JSON format with one key: body in HTML.
    """
    response = get_prompt_response_exp(template)
    result_json = extract_json_from_response(response.text)
    body = result_json.get("body", "")

    if signature and signature not in body:
        body = f"{body}\n{signature}"

    return {
        "body": body,
        "tokens_input": response.usage_metadata.prompt_token_count,
        "tokens_output": response.usage_metadata.candidates_token_count,
    }


def categorize_and_summarize_email(
    subject: str,
    decoded_data: str,
    category_dict: dict,
    user_description: str,
    sender: str,
    important_guidelines: str,
    informative_guidelines: str,
    useless_guidelines: str,
) -> dict:
    """
    Categorizes and summarizes an email.

    Args:
        subject (str): The subject of the email.
        decoded_data (str): The decoded content of the email body.
        category_dict (dict): A dictionary of topic categories to be used for classification.
        user_description (str): A description provided by the user to assist with categorization.
        sender (str): The sender of the email.

    Returns:
        dict: Structured JSON response with categorized and summarized email details.
    """
    response_list = {
        ANSWER_REQUIRED: "Message requires an answer.",
        MIGHT_REQUIRE_ANSWER: "Message might require an answer.",
        NO_ANSWER_REQUIRED: "No answer is required.",
    }
    relevance_list = {
        HIGHLY_RELEVANT: "Message is highly relevant to the recipient.",
        POSSIBLY_RELEVANT: "Message might be relevant to the recipient.",
        NOT_RELEVANT: "Message is not relevant to the recipient.",
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

    Follow those rules:
    "important" emails: {important_guidelines}
    "informative" emails: {informative_guidelines}
    "useless" emails: {useless_guidelines}
    
    Complete the following tasks in same language used in the email:
    - Categorize the email according to the user description (if provided) and given categories.
    - Summarize the email without adding any greetings.
    - If the email explicitly mentions the name of the user (provided with user description), then use 'You' instead of the name of the user.
    - Provide a short sentence (up to 10 words) summarizing the core content of the email.
    - Define the importance level of the email with one keyword: "important", "informative" or "useless".
    - If the email appears to be a response or a conversation, summarize only the last email and IGNORE the previous ones.
    - The summary should objectively reflect the most important information of the email without making subjective judgments.    
    
    ---
    Return this JSON object completed with the requested information:
    {{
        "topic": Selected Category,
        "response": Response,
        "relevance": Relevance,
        "importance": Importance of the email,
        "flags": {{
            "spam": bool,
            "scam": bool,
            "newsletter": bool,
            "notification": bool,
            "meeting": bool
        }},
        "summary": {{
            "one_line": One sentence summary,
            "short": Short summary of the email
        }}
    }}"""
    response = get_prompt_response(template)
    result_json = extract_json_from_response(response.text)
    result_json["tokens_input"] = response.usage_metadata.prompt_token_count
    result_json["tokens_output"] = response.usage_metadata.candidates_token_count

    return result_json


def search_emails(query: str, language: str) -> dict:
    """
    Searches emails based on the user query and generates structured JSON response.

    Args:
        query (str): User's query for searching emails.
        language (str): Language for the response JSON format.

    Returns:
        dict: Structured JSON response with search results and parameters.
    """
    today = datetime.now().strftime("%m-%d-%Y")

    template = f"""As a smart email assistant and based on the user query: '{query}'. Knowing today's date: {today}
    1. Analyse and create a filter to search emails content with the Gmail API and Graph API.
    2. If nothing special is specified, 'from', 'to', 'subject', 'body' MUST have the same value as the most relevant keyword. By default, search in 'read', 'unread' emails
    3. Regarding keywords, provide ONLY individual words. Sentences are not allowed unless explicitly mentioned. If you're unsure, list every relevant word separately.
    4. If and only if a date is explicitely provided by the user; add it to the output using this format: MM/DD/YYYY. Otherwise leave it as an empty string if you hesitate.
    
    ---
    Answer must ONLY be a Json format matching this template in {language} WITHOUT giving any explanation:
    {{
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
    result_json = extract_json_from_response(response.text)
    result_json["tokens_input"] = response.usage_metadata.prompt_token_count
    result_json["tokens_output"] = response.usage_metadata.candidates_token_count

    return result_json


def review_user_description(user_description: str) -> dict:
    """
    Reviews a user-provided description and provides validation and feedback.

    Args:
        user_description (str): User's description for categorizing emails.

    Returns:
        dict: JSON response with 'valid' status and 'feedback' message.
    """
    prompt = f"""You are an assistant helping a user to create categories to automatically classify emails. The user has provided the following description for a category: {user_description}
    
    The category should be clear and precise with enough details to classify incoming emails. The description should be in the third person and provide a clear understanding of the category.
    Here are some good examples:
                'Augustin ROLET is a student at ESAIP (Engineering School specialized in Computer Science),
                Augustin ROLET is an Integration Development Intern at CDS (Cognitive Design Systems is a company that creates software for 3D printing).'

    Tasks:
    - Review the description provided by the user.
    - Provide feedback on the quality of the description.
    - Indicate whether the description is valid. As long as the description is clear and provides enough details, it should be considered valid.
    - Do not be strict about the details: as long as the description is a short sentence and contains a few relevant keywords, it should be considered valid.

    The response MUST be a JSON formatted as follows:
    {{
        "valid": boolean,
        "feedback": "short sentence describing the quality of the description"
    }}
    """
    response = get_prompt_response(prompt)
    result_json = extract_json_from_response(response.text)
    result_json["tokens_input"] = response.usage_metadata.prompt_token_count
    result_json["tokens_output"] = response.usage_metadata.candidates_token_count

    return result_json


def generate_categories_scratch(
    user_topics: list | str, chat_history: list = None
) -> dict:
    """
    Generates categories based on user topics for email classification.

    Args:
        user_topics (list | str): List or string of topics provided by the user.
        chat_history (list | None): List of messages between user and AI.

    Returns:
        dict: JSON response with category names, descriptions, and feedback.
    """
    chat_history_text = (
        f"- Take into account the chat history, but prioritize the latest guidelines from the user:\n  {chat_history}"
        if chat_history
        else ""
    )
    prompt = f"""You are an assistant helping a user to create categories to automatically classify emails. The user has provided the following list of topics: {user_topics}
    
    Tasks:
    - The topics will be used to classify incoming emails.
    - If you see an obvious mistake in the name or the desctiption you can correct it.
    - The description should be clear and precise with enough details to classify incoming emails.
    - Avoid creating categories that are too similar to each other the categories MUST have no links between them or very little if not possible.
    - Stay as minimal as possible with the numers of created categories, DO NOT TRY to add additional categories that might fit the user.
    - Provide feedback on the quality of the name and description for each category. It MUST be short and will only be visible by the user if he dislikes the name or description.
    {chat_history_text}

    The response MUST be a JSON formatted as follows:
    {{
        "categories": [
            {{
                "name": "Category 1",
                "description": "Description of the category",
                "feedback": "short sentence describing the quality of the name and description"
            }},
            {{
                "name": "Category 2",
                "description": "Description of the category",
                "feedback": "short sentence describing the quality of the name and description"
            }}
        ]
    }}
    """
    response = get_prompt_response(prompt)
    result_json = extract_json_from_response(response.text)
    result_json["tokens_input"] = response.usage_metadata.prompt_token_count
    result_json["tokens_output"] = response.usage_metadata.candidates_token_count

    return result_json


def generate_prioritization_scratch(user_input: dict | str) -> dict:
    """
    Generates email prioritization guidelines based on user-provided input.

    Args:
        user_input (dict | str): The user's guidance for prioritizing emails.

    Returns:
        dict: A JSON object with descriptions for:
              - important emails
              - informative emails
              - useless emails
    """
    prompt = f"""You are an intelligent email assistant tasked with helping a user create detailed and effective email prioritization guidelines.
    
    The user has provided the following input: {user_input}
    This input will be used to guide an AI system in automatically categorizing and prioritizing emails based on the user's preferences.

    Your tasks are:
    1. Review the user's guidance for accuracy, completeness, and clarity.
    2. Correct any inconsistencies or errors in descriptions.
    3. Improve the descriptions to ensure they are:
       - Clear and concise
       - Specific and actionable
       - Aligned with the user's input
    4. Adapt the descriptions while taking inspiration from the example provided below, ensuring the response remains user-specific.

    Example of effective prioritization guidance:
    {{
        "important": "Emails requiring immediate attention, such as meetings and deadlines.",
        "informative": "General updates or communications that don't need urgent action.",
        "useless": "Spam, marketing emails, and newsletters that are not useful."
    }}

    Your response MUST strictly follow this JSON format:
    {{
        "important": "Description of what important emails are for the user.",
        "informative": "Description of what informative emails are for the user.",
        "useless": "Description of what useless emails are for the user."
    }}
    """
    response = get_prompt_response(prompt)
    result_json = extract_json_from_response(response.text)
    result_json["tokens_input"] = response.usage_metadata.prompt_token_count
    result_json["tokens_output"] = response.usage_metadata.candidates_token_count

    return result_json


def determine_action_scenario(
    destinary: bool,
    subject: bool,
    email_content: bool,
    user_request: str,
    is_only_signature: bool,
) -> int:
    """
    Determines the scenario based on input flags and user request.

    Args:
        destinary (bool): Whether the sender is selected manually.
        subject (bool): Whether the subject is specified.
        email_content (bool): Whether the email content is provided.
        user_request (str): The user's request.

    Returns:
        int: Scenario number (1-5).
            1 = "The user wants the AI to fetch a sender's email using name or directly email or part of the email"
            2 = "The user wants to send an email and has specified the sender or senders"
            3 = "The user wants to send an email and has not specified any senders"
            4 = "The user wants feedback on already existing email content"
            5 = "I didn't understand the user request"
    """
    if not destinary and not subject and (not email_content or is_only_signature):
        formatted_prompt = f"""
        Determine the appropriate scenario based on the following user request:
        "{user_request}"

        Scenarios:
        1. The user wants the AI to fetch a sender's email using name or directly email or part of the email. Or the user ask to send an email to someone without specifying any email instructions or draft.
        2. The user wants to ask the AI to generate an email and has specified the sender or senders.
        3. The user wants to ask the AI to generate an email and has not specified any senders.

        Please respond with the scenario number (1, 2, or 3) that best fits the user request.
        """
        response = get_prompt_response(formatted_prompt)
        try:
            scenario = int(response.text.strip())
            if scenario in [1, 2, 3]:
                return scenario
            else:
                LOGGER.error(f"Invalid scenario number received from AI: {scenario}")
                return 5
        except (ValueError, AttributeError) as e:
            LOGGER.error(f"Error parsing AI response: {e}")
            return 5

    if destinary and not subject and (not email_content or is_only_signature):
        return 3

    if destinary and subject and (not email_content or is_only_signature):
        return 3

    if email_content and not is_only_signature:
        return 4

    return 5
