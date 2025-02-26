"""
Handles prompt engineering requests for Claude 3 API.

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
- ✅ determine_action_scenario: Determines the scenario based on input flags and user request.
- ✅ improve_email_response: Improves an email response based on user feedback.
- ✅ improve_draft: Improves a draft email based on user feedback.
- ✅ select_categories: Selects categories based on user input.
- ✅ get_answer: Gets an answer based on user input.
- ✅ summarize_conversation: Summarizes a conversation.
- ✅ summarize_email: Summarizes an email.
"""

import json
import logging
import os
import re
import anthropic
from datetime import datetime
from aomail.ai_providers.utils import count_corrections
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
    GET_ANSWER_PROMPT,
    IMPROVE_EMAIL_COPYWRITING_PROMPT,
    IMPROVE_EMAIL_DRAFT_PROMPT,
    IMPROVE_EMAIL_RESPONSE_PROMPT,
    RELEVANCE_LIST,
    RESPONSE_LIST,
    REVIEW_USER_DESCRIPTION_PROMPT,
    SEARCH_EMAILS_PROMPT,
    SELECT_CATEGORIES_PROMPT,
    SIGNATURE_INSTRUCTION_WITH_CONTENT,
    SIGNATURE_INSTRUCTION_WITHOUT_CONTENT,
    SUMMARIZE_CONVERSATION_PROMPT,
    SUMMARIZE_EMAIL_PROMPT,
)


LOGGER = logging.getLogger(__name__)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


######################## TEXT PROCESSING UTILITIES ########################
def get_prompt_response(
    formatted_prompt: str, model: str = "claude-3-5-haiku-latest"
) -> anthropic.types.message.Message:
    """Returns the prompt response"""
    if not model:
        model = "claude-3-5-haiku-latest"
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        temperature=0.0,
        messages=[{"role": "user", "content": formatted_prompt}],
    )
    return response


def get_prompt_response_with_tokens(
    formatted_prompt: str, model: str = "claude-3-5-haiku-latest"
) -> dict:
    response = get_prompt_response(formatted_prompt, model)
    result_json = json.loads(response.content[0].text)
    result_json["tokens_input"] = response.usage.input_tokens
    result_json["tokens_output"] = response.usage.output_tokens

    return result_json


def extract_contacts_recipients(query: str, llm_model: str = None) -> dict:
    formatted_prompt = EXTRACT_CONTACTS_RECIPIENTS_PROMPT.format(query=query)
    return get_prompt_response_with_tokens(formatted_prompt, llm_model)


# ----------------------- PREPROCESSING REPLY EMAIL -----------------------#
def generate_response_keywords(
    input_email: str, input_subject: str, llm_model: str = None
) -> dict:
    formatted_prompt = GENERATE_RESPONSE_KEYWORDS_PROMPT.format(
        input_subject=input_subject, input_email=input_email
    )

    return get_prompt_response_with_tokens(formatted_prompt, llm_model)


######################## WRITING ########################
def generate_email(
    input_data: str,
    length: str,
    formality: str,
    language: str,
    agent_settings: dict,
    signature: str = "",
    llm_model: str = None,
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

    return get_prompt_response_with_tokens(formatted_prompt, llm_model)


def correct_mail_language_mistakes(
    body: str,
    subject: str,
    llm_model: str = None,
) -> dict:
    formatted_prompt = CORRECT_MAIL_LANGUAGE_MISTAKES_PROMPT.format(
        subject=subject, body=body
    )
    response = get_prompt_response(formatted_prompt, llm_model)
    clear_text = response.content[0].text.strip()
    result_json = json.loads(clear_text)

    corrected_subject = result_json["subject"]
    corrected_body = result_json["body"]

    num_corrections = count_corrections(
        subject, body, corrected_subject, corrected_body
    )

    return {
        "correctedSubject": corrected_subject,
        "correctedBody": corrected_body,
        "numCorrections": num_corrections,
        "tokens_input": response.usage.input_tokens,
        "tokens_output": response.usage.output_tokens,
    }


def improve_email_copywriting(
    email_subject: str, email_body: str, llm_model: str = None
) -> dict:
    formatted_prompt = IMPROVE_EMAIL_COPYWRITING_PROMPT.format(
        email_subject=email_subject, email_body=email_body
    )
    response = get_prompt_response(formatted_prompt, llm_model)
    feedback_ai = response.content[0].text.strip()

    return {
        "feedback_ai": feedback_ai,
        "tokens_input": response.usage.input_tokens,
        "tokens_output": response.usage.output_tokens,
    }


def generate_email_response(
    input_subject: str,
    input_body: str,
    user_instruction: str,
    agent_settings: dict,
    signature: str = "",
    llm_model: str = None,
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
    response = get_prompt_response(formatted_prompt, llm_model)
    body = response.content[0].text.strip()

    return {
        "body": body,
        "tokens_input": response.usage.input_tokens,
        "tokens_output": response.usage.output_tokens,
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
    llm_model: str = None,
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
    return get_prompt_response_with_tokens(formatted_prompt, llm_model)


def search_emails(query: str, language: str, llm_model: str = None) -> dict:
    today = datetime.now().strftime("%m-%d-%Y")
    formatted_prompt = SEARCH_EMAILS_PROMPT.format(
        query=query, today=today, language=language
    )
    return get_prompt_response_with_tokens(formatted_prompt, llm_model)


def review_user_description(user_description: str, llm_model: str = None) -> dict:
    formatted_prompt = REVIEW_USER_DESCRIPTION_PROMPT.format(
        user_description=user_description
    )
    return get_prompt_response_with_tokens(formatted_prompt, llm_model)


def generate_categories_scratch(
    user_topics: list | str, chat_history: list = None, llm_model: str = None
) -> dict:
    chat_history_text = (
        CHAT_HISTORY_TEXT.format(chat_history=chat_history) if chat_history else ""
    )
    formatted_prompt = GENERATE_CATEGORIES_SCRATCH_PROMPT.format(
        user_topics=user_topics,
        chat_history_text=chat_history_text,
    )
    return get_prompt_response_with_tokens(formatted_prompt, llm_model)


def generate_prioritization_scratch(
    user_input: dict | str, llm_model: str = None
) -> dict:
    formatted_prompt = GENERATE_PRIORITIZATION_SCRATCH_PROMPT.format(
        user_input=user_input
    )
    return get_prompt_response_with_tokens(formatted_prompt, llm_model)


def determine_action_scenario(
    destinary: bool,
    subject: bool,
    email_content: bool,
    user_request: str,
    is_only_signature: bool,
    llm_model: str = None,
) -> dict:
    result_json = {"tokens_input": 0, "tokens_output": 0, "scenario": 5}
    if not destinary and not subject and (not email_content or is_only_signature):
        formatted_prompt = DETERMINE_ACTION_SCENARIO_PROMPT.format(
            user_request=user_request
        )
        response = get_prompt_response_with_tokens(formatted_prompt, llm_model)
        try:
            scenario = response.get("scenario", 5)
            if scenario in [1, 2, 3]:
                return result_json
            else:
                LOGGER.error(f"Invalid scenario number received from AI: {scenario}")
                result_json["scenario"] = 5
                return result_json
        except (ValueError, AttributeError) as e:
            LOGGER.error(f"Error parsing AI response: {e}")
            result_json["scenario"] = 5
            return result_json

    if destinary and not subject and (not email_content or is_only_signature):
        result_json["scenario"] = 3
        return result_json

    if destinary and subject and (not email_content or is_only_signature):
        result_json["scenario"] = 3
        return result_json

    if email_content and not is_only_signature:
        result_json["scenario"] = 4
        return result_json

    result_json["scenario"] = 5
    return result_json


def improve_email_response(
    importance: str,
    subject: str,
    body: str,
    history: dict,
    user_input: str,
    agent_settings: dict,
    llm_model: str = None,
) -> dict:
    formatted_prompt = IMPROVE_EMAIL_RESPONSE_PROMPT.format(
        importance=importance,
        subject=subject,
        body=body,
        history=history,
        user_input=user_input,
        agent_settings=agent_settings,
    )
    return get_prompt_response_with_tokens(formatted_prompt, llm_model)


def improve_draft(
    language: str,
    agent_settings: dict,
    subject: str,
    body: str,
    history: dict,
    user_input: str,
    length: str,
    formality: str,
    llm_model: str = None,
) -> dict:
    formatted_prompt = IMPROVE_EMAIL_DRAFT_PROMPT.format(
        language=language,
        agent_settings=agent_settings,
        subject=subject,
        body=body,
        history=history,
        user_input=user_input,
        length=length,
        formality=formality,
    )
    return get_prompt_response_with_tokens(formatted_prompt, llm_model)


def select_categories(categories: str, question: str, llm_model: str = None) -> dict:
    formatted_prompt = SELECT_CATEGORIES_PROMPT.format(
        categories=categories, question=question
    )
    return get_prompt_response_with_tokens(formatted_prompt, llm_model)


def get_answer(
    keypoints: dict, question: str, language: str, llm_model: str = None
) -> dict:
    formatted_prompt = GET_ANSWER_PROMPT.format(
        keypoints=keypoints, question=question, language=language
    )
    return get_prompt_response_with_tokens(formatted_prompt, llm_model)


def summarize_conversation(
    subject: str,
    body: str,
    user_description: str,
    categories: dict,
    language: str,
    llm_model: str = None,
) -> dict:
    formatted_prompt = SUMMARIZE_CONVERSATION_PROMPT.format(
        subject=subject,
        body=body,
        categories=categories,
        user_description=user_description,
        language=language,
    )
    return get_prompt_response_with_tokens(formatted_prompt, llm_model)


def summarize_email(
    subject: str,
    body: str,
    user_description: str,
    categories: dict,
    language: str,
    llm_model: str = None,
) -> dict:
    formatted_prompt = SUMMARIZE_EMAIL_PROMPT.format(
        subject=subject,
        body=body,
        categories=categories,
        user_description=user_description,
        language=language,
    )
    return get_prompt_response_with_tokens(formatted_prompt, llm_model)
