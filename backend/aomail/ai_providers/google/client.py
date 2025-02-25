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

import os
import re
import ast
import json
import logging
import google.generativeai as genai
from datetime import datetime
from aomail.ai_providers.utils import extract_json_from_response
from aomail.ai_providers.prompts import (
    CATEGORIZE_AND_SUMMARIZE_EMAIL_PROMPT,
    CHAT_HISTORY_TEXT,
    CORRECT_MAIL_LANGUAGE_MISTAKES_PROMPT,
    DETERMINE_ACTION_SCENARIO_PROMPT,
    EXTRACT_CONTACTS_RECIPIENTS_PROMPT,
    GENERATE_CATEGORIES_SCRATCH_PROMPT,
    GENERATE_EMAIL_PROMPT,
    GENERATE_EMAIL_RESPONSE_PROMPT,
    GENERATE_PRIORITIZATION_SCRATCH_PROMPT,
    GENERATE_RESPONSE_KEYWORDS_PROMPT,
    IMPROVE_EMAIL_COPYWRITING_PROMPT,
    RELEVANCE_LIST,
    RESPONSE_LIST,
    REVIEW_USER_DESCRIPTION_PROMPT,
    SEARCH_EMAILS_PROMPT,
    SIGNATURE_INSTRUCTION_WITH_CONTENT,
    SIGNATURE_INSTRUCTION_WITHOUT_CONTENT,
)


LOGGER = logging.getLogger(__name__)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


######################## TEXT PROCESSING UTILITIES ########################
def get_prompt_response(formatted_prompt: str, model: str = "gemini-1.5-flash"):
    """Returns the prompt response using Gemini 1.5 Flash model"""
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(model)
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
    formatted_prompt = EXTRACT_CONTACTS_RECIPIENTS_PROMPT.format(query=query)
    response = get_prompt_response(formatted_prompt)
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
    formatted_prompt = GENERATE_RESPONSE_KEYWORDS_PROMPT.format(
        input_subject=input_subject, input_email=input_email
    )
    response = get_prompt_response(formatted_prompt, "gemini-2.0-flash-exp")
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
        signature_instruction = SIGNATURE_INSTRUCTION_WITH_CONTENT.format(
            signature=signature
        )
    else:
        signature_instruction = SIGNATURE_INSTRUCTION_WITHOUT_CONTENT

    template = GENERATE_EMAIL_PROMPT.format(
        agent_settings=json.dumps(agent_settings),
        length=length,
        formality=formality,
        language=language,
        input_data=input_data,
        signature_instruction=signature_instruction,
    )

    response = get_prompt_response(template, "gemini-2.0-flash-exp")
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

    formatted_prompt = CORRECT_MAIL_LANGUAGE_MISTAKES_PROMPT.format(
        subject=subject, body=body
    )
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

    template = IMPROVE_EMAIL_COPYWRITING_PROMPT.format(
        email_subject=email_subject, email_body=email_body
    )
    response = get_prompt_response(template)
    feedback_ai = response.text

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
        signature_instruction = SIGNATURE_INSTRUCTION_WITH_CONTENT.format(
            signature=signature
        )
    else:
        signature_instruction = SIGNATURE_INSTRUCTION_WITHOUT_CONTENT

    template = GENERATE_EMAIL_RESPONSE_PROMPT.format(
        agent_settings=json.dumps(agent_settings),
        input_subject=input_subject,
        input_body=input_body,
        user_instruction=user_instruction,
        signature_instruction=signature_instruction,
    )
    response = get_prompt_response(template, "gemini-2.0-flash-exp")
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
        important_guidelines (str): Guidelines for important emails.
        informative_guidelines (str): Guidelines for informative emails.
        useless_guidelines (str): Guidelines for useless emails.

    Returns:
        dict: Structured JSON response with categorized and summarized email details.
    """
    template = CATEGORIZE_AND_SUMMARIZE_EMAIL_PROMPT.format(
        sender=sender,
        subject=subject,
        decoded_data=decoded_data,
        user_description=user_description,
        category_dict=category_dict,
        response_list=RESPONSE_LIST,
        relevance_list=RELEVANCE_LIST,
        important_guidelines=important_guidelines,
        informative_guidelines=informative_guidelines,
        useless_guidelines=useless_guidelines,
    )
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

    template = SEARCH_EMAILS_PROMPT.format(query=query, today=today, language=language)
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
    prompt = REVIEW_USER_DESCRIPTION_PROMPT.format(user_description=user_description)
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
        CHAT_HISTORY_TEXT.format(chat_history=chat_history) if chat_history else ""
    )
    prompt = GENERATE_CATEGORIES_SCRATCH_PROMPT.format(
        user_topics=user_topics,
        chat_history_text=chat_history_text,
    )
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
    prompt = GENERATE_PRIORITIZATION_SCRATCH_PROMPT.format(user_input=user_input)
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
        formatted_prompt = DETERMINE_ACTION_SCENARIO_PROMPT.format(
            user_request=user_request
        )
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
