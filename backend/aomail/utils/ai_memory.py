"""
Handles conversations with prompt engineering for user/AI interaction.
"""

import json
from django.contrib.auth.models import User
from langchain_community.chat_message_histories import ChatMessageHistory
from aomail.ai_providers import gemini
from aomail.ai_providers.utils import extract_json_from_response


class EmailReplyConversation:
    """Handles the conversation with the AI to reply to an email."""

    def __init__(
        self,
        user: User,
        importance: str,
        subject: str,
        body: str,
        history: ChatMessageHistory,
    ):
        """
        Initializes an instance of EmailReplyConversation.

        Args:
            user (User): The user object who is replying to the email.
            importance (str): The importance level of the email (e.g., "high", "medium", "low").
            subject (str): The subject of the email to reply to.
            body (str): The initial body of the email response.
            history (ChatMessageHistory): History of the conversation messages.
        """
        self.user = user
        self.subject = subject
        self.importance = importance.lower()
        self.body = body
        self.history = history

    def update_history(self, user_input: str, new_body: str):
        """
        Updates the conversation history and the current email body response.

        Args:
            user_input (str): The user's input message.
            new_body (str): The updated body of the email response.
        """
        self.history.add_user_message(user_input)
        self.body = new_body

    def improve_email_response(self, user_input: str, agent_settings: dict) -> dict:
        """
        Improves the email response according to the conversation history.

        Args:
            user_input (str): The user's input for improving the email response.
            agent_settings (dict): Settings for the AI agent to guide the response.

        Returns:
            dict: A dictionary containing:
                body (str): The improved email response in HTML format.
                tokens_input (int): The number of tokens used for the input.
                tokens_output (int): The number of tokens used for the output.
        """
        template = f"""You are Ao, an email assistant, following these agent guidelines: {json.dumps(agent_settings)}, who helps a user reply to an {self.importance} email they received.
        The user has already entered the recipients and the subject: '{self.subject}' of the email.    
        Improve the email response following the user's guidelines.

        Current email body response:
        {self.body}

        Current Conversation:
        {self.history}
        User: {user_input}

        The response must retain the core information and incorporate the required user changes.
        If you hesitate or there is contradictory information, always prioritize the last user input.

        ---
        Answer must ONLY be in JSON format with one key: body in HTML.
        """
        response = gemini.get_prompt_response_exp(template)
        result_json = extract_json_from_response(response.text)
        body = result_json.get("body", "")

        self.update_history(user_input, body)

        return {
            "body": body,
            "tokens_input": response.usage_metadata.prompt_token_count,
            "tokens_output": response.usage_metadata.candidates_token_count,
        }


class GenerateEmailConversation:
    """Handles the conversation with the AI to generate an email."""

    def __init__(
        self,
        user: User,
        length: str,
        formality: str,
        subject: str,
        body: str,
        history: ChatMessageHistory,
    ):
        """
        Initializes a GenerateEmailConversation object.

        Args:
            user (User): The user object who is generating the email.
            length (str): The desired length of the email (e.g., "short", "medium", "long").
            formality (str): The desired formality of the email (e.g., "formal", "informal").
            subject (str): The subject of the email to be generated.
            body (str): The initial body of the email to be generated.
            history (ChatMessageHistory): History of the conversation messages.
        """
        self.user = user
        self.subject = subject
        self.body = body
        self.length = length
        self.formality = formality
        self.history = history

    def update_history(self, user_input: str, new_subject: str, new_body: str):
        """
        Updates the conversation history and the current email subject and body.

        Args:
            user_input (str): The user's input message.
            new_subject (str): The updated subject of the email.
            new_body (str): The updated body of the email.
        """
        self.history.add_user_message(user_input)
        self.subject = new_subject
        self.body = new_body

    def improve_draft(self, user_input: str, language: str) -> dict:
        """
        Improves the email subject and body generated by the AI according to user guidelines.

        Args:
            user_input (str): The user's input for improving the email draft.
            language (str): The language used for the email content.

        Returns:
            dict: A dictionary containing:
                new_subject (str): The improved subject of the email.
                new_body (str): The improved body of the email in HTML format.
                tokens_input (int): The number of tokens used for the input.
                tokens_output (int): The number of tokens used for the output.
        """
        template = f"""You are an email assistant, who helps a user redact an email in {language}.
        The user has already entered the recipients and the subject: '{self.subject}' of the email.    
        Improve the email body and subject following the user's guidelines.

        Current email body:
        {self.body}

        Current Conversation:
        {self.history}
        User: {user_input}

        The response must retain the core information and incorporate the required user changes.
        If you hesitate or there is contradictory information, always prioritize the last user input.
        Keep the same email body length: '{self.length}' AND level of speech: '{self.formality}' unless a change is explicitly mentioned by the user.

        ---
        Answer must ONLY be in JSON format with two keys: subject (STRING) and body in HTML format without spaces and unusual line breaks.
        """
        response = gemini.get_prompt_response(template)
        clear_text = response.content[0].text.strip()

        result_json: dict[str, str] = json.loads(clear_text)
        new_subject = result_json.get("subject")
        new_body = result_json.get("body")
        self.update_history(user_input, new_subject, new_body)

        return {
            "new_subject": new_subject,
            "new_body": new_body,
            "tokens_input": response.usage.input_tokens,
            "tokens_output": response.usage.output_tokens,
        }
