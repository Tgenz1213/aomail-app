from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, ChatMessageHistory
from langchain_core.prompts.prompt import PromptTemplate
from langchain_community.chat_models import ChatAnthropic
from constants import CLAUDE_CREDS


from langchain.memory import (
    ChatMessageHistory,
    ConversationSummaryMemory,
    ConversationBufferMemory,
)
from langchain.chains import ConversationChain
from langchain_core.prompts.prompt import PromptTemplate
import json
import anthropic
from colorama import Fore, init
from constants import CLAUDE_CREDS, HUMAN, ASSISTANT
from langchain_anthropic import ChatAnthropic

######################## Claude 3 API SETTINGS ########################
init(autoreset=True)


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


class EmailReplyConversation:
    """Handles the conversation with the AI to reply to an email."""

    def __init__(self, user: str, importance: str, subject: str, body: str) -> None:
        self.user = user
        self.subject = subject
        self.importance = importance.lower()
        self.body = body
        self.history = ChatMessageHistory()

    def prompt(self, user_input: str):
        # TODO: check claude prompt template
        template = f"""{HUMAN}You are Ao, an email assistant, who helps a user redact an email.
                The user has already entered the recipients and the subject: '{self.subject}' of the email.    
                Improve the email body and subject following the user's guidelines.

                Current Conversation:
                {self.history}
                User: {user_input}

                The response must retain the core information and incorporate the required user changes.
                If you hesitate or there is contradictory information, always prioritize the last user input.
                Keep the same email body length AND level of speech unless a change is explicitly mentioned by the user.

                ---
                The answer must include all new changes and match the same HTML format.
                {ASSISTANT}
                """


# N'hésitez pas à fournir un brouillon de l'email que vous souhaitez rédiger

# here give the length and formality

# Est-ce que ce mail vous convient ? Vous pouvez me fournir des indications pour que je l'adapte à vos besoins

# new prompt disant que non il faut faire ci

# Corrige l'orthographe => J'ai corrigé l'orthographe, est-ce que souhaitez autre chose ?
# Vérifie le copywriting => J'ai vérifié le copywriting, est-ce que souhaitez autre chose ?
# Améliore l'écriture => Est-ce que ce mail vous convient mieux ?


# il répond tjrs ça après
# Est-ce que ce mail vous convient mieux ?
