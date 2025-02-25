"""
Dispatches LLM requests to different providers (currently Anthropic Claude and Google Gemini).

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

from aomail.ai_providers.anthropic import client as claude
from aomail.ai_providers.google import client as gemini


def extract_contacts_recipients(
    query: str, llm_provider: str = "google", llm_model: str = None
) -> dict[str, list]:
    """
    Analyzes the input query to categorize email recipients into main, CC, and BCC categories.

    Args:
        query (str): The input string containing email recipient information.
        llm_provider (str): The language model to use for the email recipient extraction.
        llm_model (str): The language model to use for the email recipient extraction.

    Returns:
        dict[str, list]: A dictionary with three keys:
            'main_recipients': List of main recipients.
            'cc_recipients': List of CC recipients.
            'bcc_recipients': List of BCC recipients.
    """
    if llm_provider == "anthropic":
        return claude.extract_contacts_recipients(query, llm_model)
    elif llm_provider == "google":
        return gemini.extract_contacts_recipients(query, llm_model)


def generate_response_keywords(
    input_email: str,
    input_subject: str,
    llm_provider: str = "google",
    llm_model: str = None,
) -> dict:
    """
    Generates a list of detailed draft response sentences for responding to a given email.

    Args:
        input_email (str): The body of the email.
        input_subject (str): The subject of the email.
        llm_provider (str): The language model to use for the email generation.
        llm_model (str): The language model to use for the email generation.

    Returns:
        dict: A dictionary containing:
            keywords_list (list): A list of detailed draft response sentences for the email.
            tokens_input (int): The number of tokens used for the input.
            tokens_output (int): The number of tokens used for the output.
    """
    if llm_provider == "anthropic":
        return claude.generate_response_keywords(input_email, input_subject, llm_model)
    elif llm_provider == "google":
        return gemini.generate_response_keywords(input_email, input_subject, llm_model)


def generate_email(
    input_data: str,
    length: str,
    formality: str,
    language: str,
    agent_settings: dict,
    signature: str = "",
    llm_provider: str = "google",
    llm_model: str = None,
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
        llm_provider (str): The language model to use for the email generation.
        llm_model (str): The language model to use for the email generation.

    Returns:
        dict: A dictionary containing:
            subject_text (str): The subject of the generated email.
            email_body (str): The body of the generated email in HTML format.
            tokens_input (int): The number of tokens used for the input.
            tokens_output (int): The number of tokens used for the output.
    """
    if llm_provider == "anthropic":
        return claude.generate_email(
            input_data,
            length,
            formality,
            language,
            agent_settings,
            signature,
            llm_model,
        )
    elif llm_provider == "google":
        return gemini.generate_email(
            input_data,
            length,
            formality,
            language,
            agent_settings,
            signature,
            llm_model,
        )


def correct_mail_language_mistakes(
    body: str, subject: str, llm_provider: str = "google", llm_model: str = None
) -> dict:
    """
    Corrects spelling and grammar mistakes in the email subject and body based on user's request.

    Args:
        body (str): The body of the email to be corrected.
        subject (str): The subject of the email to be corrected.
        llm_provider (str): The language model to use for the email correction.
        llm_model (str): The language model to use for the email correction.

    Returns:
        dict: A dictionary containing:
            corrected_subject (str): The corrected subject of the email.
            corrected_body (str): The corrected body of the email in HTML format.
            num_corrections (int): The number of corrections made in the email subject and body.
            tokens_input (int): The number of tokens used for the input.
            tokens_output (int): The number of tokens used for the output.
    """
    if llm_provider == "anthropic":
        return claude.correct_mail_language_mistakes(body, subject, llm_model)
    elif llm_provider == "google":
        return gemini.correct_mail_language_mistakes(body, subject, llm_model)


def improve_email_copywriting(
    email_subject: str,
    email_body: str,
    llm_provider: str = "google",
    llm_model: str = None,
) -> dict:
    """
    Provides feedback and suggestions for improving the copywriting in the email subject and body.

    Args:
        email_subject (str): The subject of the email to be evaluated and improved.
        email_body (str): The body of the email to be evaluated and improved.
        llm_provider (str): The language model to use for the email copywriting improvement.
        llm_model (str): The language model to use for the email copywriting improvement.

    Returns:
        dict: A dictionary containing:
            feedback_ai (str): Feedback and suggestions for improving the copywriting in the email subject and body.
            tokens_input (int): The number of tokens used for the input.
            tokens_output (int): The number of tokens used for the output.
    """
    if llm_provider == "anthropic":
        return claude.improve_email_copywriting(email_subject, email_body, llm_model)
    elif llm_provider == "google":
        return gemini.improve_email_copywriting(email_subject, email_body, llm_model)


def generate_email_response(
    input_subject: str,
    input_body: str,
    user_instruction: str,
    agent_settings: dict,
    signature: str = "",
    llm_provider: str = "google",
    llm_model: str = None,
) -> dict:
    """
    Generates an email response based on the given response type and agent settings.

    Args:
        input_subject (str): The subject of the email to respond to.
        input_body (str): The body of the email to respond to.
        user_instruction (str): Instructions or guidelines provided by the user for crafting the response.
        agent_settings (dict): The agent's guidelines and settings to guide AI responses.
        signature (str): Optional HTML signature to append to the email.
        llm_provider (str): The language model to use for the email response generation.
        llm_model (str): The language model to use for the email response generation.

    Returns:
        dict: A dictionary containing:
            body (str): The generated email response in HTML format.
            tokens_input (int): The number of tokens used for the input.
            tokens_output (int): The number of tokens used for the output.
    """
    if llm_provider == "anthropic":
        return claude.generate_email_response(
            input_subject,
            input_body,
            user_instruction,
            agent_settings,
            signature,
            llm_model,
        )
    elif llm_provider == "google":
        return gemini.generate_email_response(
            input_subject,
            input_body,
            user_instruction,
            agent_settings,
            signature,
            llm_model,
        )


def categorize_and_summarize_email(
    subject: str,
    decoded_data: str,
    category_dict: dict,
    user_description: str,
    sender: str,
    important_guidelines: str,
    informative_guidelines: str,
    useless_guidelines: str,
    llm_provider: str = "google",
    llm_model: str = None,
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
        llm_provider (str): The language model to use for the email categorization and summarization.
        llm_model (str): The language model to use for the email categorization and summarization.

    Returns:
        dict: Structured JSON response with categorized and summarized email details.
    """
    if llm_provider == "anthropic":
        return claude.categorize_and_summarize_email(
            subject,
            decoded_data,
            category_dict,
            user_description,
            sender,
            important_guidelines,
            informative_guidelines,
            useless_guidelines,
            llm_model,
        )
    elif llm_provider == "google":
        return gemini.categorize_and_summarize_email(
            subject,
            decoded_data,
            category_dict,
            user_description,
            sender,
            important_guidelines,
            informative_guidelines,
            useless_guidelines,
            llm_model,
        )


def search_emails(
    query: str, language: str, llm_provider: str = "google", llm_model: str = None
) -> dict:
    """
    Searches emails based on the user query and generates structured JSON response.

    Args:
        query (str): User's query for searching emails.
        language (str): Language for the response JSON format.
        llm_provider (str): The language model to use for the email search.
        llm_model (str): The language model to use for the email search.

    Returns:
        dict: Structured JSON response with search results and parameters.
    """
    if llm_provider == "anthropic":
        return claude.search_emails(query, language, llm_model)
    elif llm_provider == "google":
        return gemini.search_emails(query, language, llm_model)


def review_user_description(
    user_description: str, llm_provider: str = "google", llm_model: str = None
) -> dict:
    """
    Reviews a user-provided description and provides validation and feedback.

    Args:
        user_description (str): User's description for categorizing emails.
        llm_provider (str): The language model to use for the email categorization and summarization.
        llm_model (str): The language model to use for the email categorization and summarization.

    Returns:
        dict: JSON response with 'valid' status and 'feedback' message.
    """
    if llm_provider == "anthropic":
        return claude.review_user_description(user_description, llm_model)
    elif llm_provider == "google":
        return gemini.review_user_description(user_description, llm_model)


def generate_categories_scratch(
    user_topics: list | str,
    chat_history: list = None,
    llm_provider: str = "google",
    llm_model: str = None,
) -> dict:
    """
    Generates categories based on user topics for email classification.

    Args:
        user_topics (list | str): List or string of topics provided by the user.
        chat_history (list | None): List of messages between user and AI.
        llm_provider (str): The language model to use for the email categorization and summarization.
        llm_model (str): The language model to use for the email categorization and summarization.

    Returns:
        dict: JSON response with category names, descriptions, and feedback.
    """
    if llm_provider == "anthropic":
        return claude.generate_categories_scratch(user_topics, chat_history, llm_model)
    elif llm_provider == "google":
        return gemini.generate_categories_scratch(user_topics, chat_history, llm_model)


def generate_prioritization_scratch(
    user_input: dict | str, llm_provider: str = "google", llm_model: str = None
) -> dict:
    """
    Generates email prioritization guidelines based on user-provided input.

    Args:
        user_input (dict | str): The user's guidance for prioritizing emails.
        llm_provider (str): The language model to use for the email prioritization.
        llm_model (str): The language model to use for the email prioritization.

    Returns:
        dict: A JSON object with descriptions for:
              - important emails
              - informative emails
              - useless emails
    """
    if llm_provider == "anthropic":
        return claude.generate_prioritization_scratch(user_input, llm_model)
    elif llm_provider == "google":
        return gemini.generate_prioritization_scratch(user_input, llm_model)


def determine_action_scenario(
    destinary: bool,
    subject: bool,
    email_content: bool,
    user_request: str,
    is_only_signature: bool,
    llm_provider: str = "google",
    llm_model: str = None,
) -> dict:
    """
    Determines the scenario based on input flags and user request.

    Args:
        destinary (bool): Whether the sender is selected manually.
        subject (bool): Whether the subject is specified.
        email_content (bool): Whether the email content is provided.
        user_request (str): The user's request.
        is_only_signature (bool): Whether the email content is only a signature.
        llm_provider (str): The language model to use for the email categorization and summarization.
        llm_model (str): The language model to use for the email categorization and summarization.

    Returns:
        dict: A dictionary containing:
            scenario (int): Scenario number (1-5).
            1 = "The user wants the AI to fetch a sender's email using name or directly email or part of the email"
            2 = "The user wants to send an email and has specified the sender or senders"
            3 = "The user wants to send an email and has not specified any senders"
            4 = "The user wants feedback on already existing email content"
            5 = "I didn't understand the user request"
            tokens_input (int): The number of tokens used for the input.
            tokens_output (int): The number of tokens used for the output.
    """
    if llm_provider == "anthropic":
        return claude.determine_action_scenario(
            destinary,
            subject,
            email_content,
            user_request,
            is_only_signature,
            llm_model,
        )
    elif llm_provider == "google":
        return gemini.determine_action_scenario(
            destinary,
            subject,
            email_content,
            user_request,
            is_only_signature,
            llm_model,
        )


# -----------------------  AI MEMORY PROMPTS (ai_memory.py) -----------------------#
def improve_email_response(
    importance: str,
    subject: str,
    body: str,
    history: dict,
    user_input: str,
    agent_settings: dict,
    llm_provider: str = "google",
    llm_model: str = None,
) -> dict:
    if llm_provider == "anthropic":
        return claude.improve_email_response(
            importance,
            subject,
            body,
            history,
            user_input,
            agent_settings,
            llm_model,
        )
    elif llm_provider == "google":
        return gemini.improve_email_response(
            importance,
            subject,
            body,
            history,
            user_input,
            agent_settings,
            llm_model,
        )


def improve_draft(
    language: str,
    agent_settings: dict,
    subject: str,
    body: str,
    history: dict,
    user_input: str,
    length: str,
    formality: str,
    llm_provider: str = "google",
    llm_model: str = None,
) -> dict:
    if llm_provider == "anthropic":
        return claude.improve_draft(
            language,
            agent_settings,
            subject,
            body,
            history,
            user_input,
            length,
            formality,
            llm_model,
        )
    elif llm_provider == "google":
        return gemini.improve_draft(
            language,
            agent_settings,
            subject,
            body,
            history,
            user_input,
            length,
            formality,
            llm_model,
        )


# -----------------------  TREE KNOWLEDGE PROMPTS (tree_knowledge.py) -----------------------#
def select_categories(
    categories: str, question: str, llm_provider: str = "google", llm_model: str = None
) -> dict:
    if llm_provider == "anthropic":
        return claude.select_categories(categories, question, llm_model)
    elif llm_provider == "google":
        return gemini.select_categories(categories, question, llm_model)


def get_answer(
    keypoints: dict,
    question: str,
    language: str,
    llm_provider: str = "google",
    llm_model: str = None,
) -> dict:
    if llm_provider == "anthropic":
        return claude.get_answer(keypoints, question, language, llm_model)
    elif llm_provider == "google":
        return gemini.get_answer(keypoints, question, language, llm_model)


def summarize_conversation(
    subject: str,
    body: str,
    user_description: str,
    categories: dict,
    language: str,
    llm_provider: str = "google",
    llm_model: str = None,
) -> dict:
    if llm_provider == "anthropic":
        return claude.summarize_conversation(
            subject, body, user_description, categories, language, llm_model
        )
    elif llm_provider == "google":
        return gemini.summarize_conversation(
            subject, body, user_description, categories, language, llm_model
        )


def summarize_email(
    subject: str,
    body: str,
    user_description: str,
    categories: dict,
    language: str,
    llm_provider: str = "google",
    llm_model: str = None,
) -> dict:
    if llm_provider == "anthropic":
        return claude.summarize_email(
            subject, body, user_description, categories, language, llm_model
        )
    elif llm_provider == "google":
        return gemini.summarize_email(
            subject, body, user_description, categories, language, llm_model
        )
