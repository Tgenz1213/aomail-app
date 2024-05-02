"""
Handles conversations with prompt engineering for user/AI interaction.
"""

import claude
from langchain.memory import ChatMessageHistory
from constants import HUMAN, ASSISTANT


class EmailReplyConversation:
    """Handles the conversation with the AI to reply to an email."""

    def __init__(self, user: str, importance: str, subject: str, body: str) -> None:
        self.user = user
        self.subject = subject
        self.importance = importance.lower()
        self.body = body
        self.history = ChatMessageHistory()
        self.history.add_ai_message("Does this answer satisfy you?")

    def update_history(self, user_input: str, new_body: str) -> None:
        """Updates the conversation history and the current email body response."""

        self.history.add_user_message(user_input)
        self.body = new_body

    def improve_email_response(self, user_input: str) -> str:
        """Improves the email response according to the conversation history."""

        template = f"""{HUMAN}You are Ao, an email assistant, who helps a user reply to an {self.importance} email they received.
        The user has already entered the recipients and the subject: '{self.subject}' of the email.    
        Improve the email response following the user's guidelines.

        Current email body response:
        {self.body}

        Current Conversation:
        {self.history}
        User: {user_input}

        The response must retain the core information and incorporate the required user changes.
        If you hesitate or there is contradictory information, always prioritize the last user input.
        Keep the same email body length AND level of speech unless a change is explicitly mentioned by the user.

        ---
        The answer must include all new changes and match the same HTML format.
        {ASSISTANT}"""
        # TODO: use the model chosen by the user in its settings
        response = claude.get_prompt_response(template)
        body = response.content[0].text.strip()

        self.update_history(user_input, body)

        return body
