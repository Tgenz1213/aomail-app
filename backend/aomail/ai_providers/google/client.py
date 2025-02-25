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
from aomail.ai_providers.utils import count_corrections, extract_json_from_response
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
def get_prompt_response(
    formatted_prompt: str, model: str = "gemini-1.5-flash"
) -> genai.types.GenerateContentResponse:
    """Returns the prompt response using Gemini 1.5 Flash model"""
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel(model)
    response = gemini_model.generate_content(
        formatted_prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=1000, temperature=0.0
        ),
    )
    return response


def extract_contacts_recipients(query: str) -> dict[str, list]:
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
    has_content = bool(signature) and bool(re.sub(r"<[^>]+>", "", signature).strip())
    if has_content:
        signature_instruction = SIGNATURE_INSTRUCTION_WITH_CONTENT.format(
            signature=signature
        )
    else:
        signature_instruction = SIGNATURE_INSTRUCTION_WITHOUT_CONTENT

    formatted_prompt = GENERATE_EMAIL_PROMPT.format(
        agent_settings=json.dumps(agent_settings),
        length=length,
        formality=formality,
        language=language,
        input_data=input_data,
        signature_instruction=signature_instruction,
    )

    response = get_prompt_response(formatted_prompt, "gemini-2.0-flash-exp")
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
    formatted_prompt = IMPROVE_EMAIL_COPYWRITING_PROMPT.format(
        email_subject=email_subject, email_body=email_body
    )
    response = get_prompt_response(formatted_prompt)
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
    has_content = bool(signature) and bool(re.sub(r"<[^>]+>", "", signature).strip())
    if has_content:
        signature_instruction = SIGNATURE_INSTRUCTION_WITH_CONTENT.format(
            signature=signature
        )
    else:
        signature_instruction = SIGNATURE_INSTRUCTION_WITHOUT_CONTENT

    formatted_prompt = GENERATE_EMAIL_RESPONSE_PROMPT.format(
        agent_settings=json.dumps(agent_settings),
        input_subject=input_subject,
        input_body=input_body,
        user_instruction=user_instruction,
        signature_instruction=signature_instruction,
    )
    response = get_prompt_response(formatted_prompt, "gemini-2.0-flash-exp")
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
    formatted_prompt = CATEGORIZE_AND_SUMMARIZE_EMAIL_PROMPT.format(
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
    response = get_prompt_response(formatted_prompt)
    result_json = extract_json_from_response(response.text)
    result_json["tokens_input"] = response.usage_metadata.prompt_token_count
    result_json["tokens_output"] = response.usage_metadata.candidates_token_count

    return result_json


def search_emails(query: str, language: str) -> dict:
    today = datetime.now().strftime("%m-%d-%Y")

    formatted_prompt = SEARCH_EMAILS_PROMPT.format(
        query=query, today=today, language=language
    )
    response = get_prompt_response(formatted_prompt)
    result_json = extract_json_from_response(response.text)
    result_json["tokens_input"] = response.usage_metadata.prompt_token_count
    result_json["tokens_output"] = response.usage_metadata.candidates_token_count

    return result_json


def review_user_description(user_description: str) -> dict:
    prompt = REVIEW_USER_DESCRIPTION_PROMPT.format(user_description=user_description)
    response = get_prompt_response(prompt)
    result_json = extract_json_from_response(response.text)
    result_json["tokens_input"] = response.usage_metadata.prompt_token_count
    result_json["tokens_output"] = response.usage_metadata.candidates_token_count

    return result_json


def generate_categories_scratch(
    user_topics: list | str, chat_history: list = None
) -> dict:
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
