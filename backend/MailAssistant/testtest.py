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


def generate_email_response(
    input_subject: str, input_body: str, user_instruction: str, language: str
) -> str:
    """Generates an email response based on the given response type"""

    template = f"""{HUMAN}As a smart email assistant and Based on the email with the subject: '{input_subject}' and body: '{input_body}' craft a response strictly in {language} following the user instruction: '{user_instruction}'.
    1. Ensure the response is structured as an HTML email. Make sure to create a brief response that is straight to the point. RESPECT the tone employed in the subject and body, as well as the relationship and respectful markers between recipients.
    2. Here is a template to follow, with placeholders for the dynamic content:
    <p>[Insert greeting]</p><html>[Insert the response]</html><p>[Insert sign_off],</p>

    ---
    Answer must be above HTML without spaces
    {ASSISTANT}
    """
    response = get_prompt_response(template)
    body = response.content[0].text.strip()

    print(f"{Fore.GREEN}[REPLY] body: {body}")

    return body


def improve_email_response(
    self, chat_history: ChatMessageHistory, user_input: str
) -> str:
    """Improves the email response according to the history of conversation."""

    template = f"""{HUMAN}You are Ao, an email assistant, that helps a user to reply to an {self.importance} email he received.
    The user has already entered the recipients and the subject: '{self.subject}' of the email.    
    Improve the email response following user's guidelines.

    Current Conversation:
    {self.chat_history}
    User: {user_input}

    The response must keep the core information and incorporate the required user changes.
    If you hesitate or there are contradictory information; always prioritize the last user input.
    Keep the same email body length AND level of speech unless a change is explicitly mentioned by the user.

    ---
    Answer must includes all new changes and match the same HTML format.
    {ASSISTANT}
    """
    response = get_prompt_response(template)
    body = response.content[0].text.strip()

    print(f"{Fore.BLUE}[REPLY n°2] body: {body}")

    return body


importance = "Informative".lower()
subject = "Préparation missions été CESAME"
body = ""

user_instruction = "Accepter l'opportunité de monter en compétences"


context = f"""You are Ao, an email assistant, that helps a user to reply to an {importance} email he received.
The user has already entered the recipients and the subject: '{subject}' of the email.
Help it to write the response to the email.

According to the current conversation.
Improve the email response following user's guidelines.

The response must keep the core information and incorporate the required user changes.
If you hesitate or there are contradictory information; always prioritize the last user input.
Keep the same email body length AND level of speech unless a change is explicitly mentioned by the user.
Answer must includes all new changes and match the same HTML format as the current email body response.

"""
body_response = generate_email_response(subject, body, user_instruction, "French")

template = (
    context
    + f"""Current email body response:
{body_response}

"""
    + """Current conversation:
{history}
User: {input}
Ao:"""
)


print(template)


llm = ChatAnthropic(
    model="claude-3-haiku-20240307", anthropic_api_key=CLAUDE_CREDS["api_key"]
)


history = ChatMessageHistory()
history.add_ai_message("Does this answer satisfy you?")


user_input = """Non,
Je veux que tu rajoute ma signature: Augustin ROLET ainsi que le fait que je suis très reconnaissant d'avoir été choisi"""
new_body_response = improve_email_response(user_input)
print(new_body_response)

user_input = """Non,
toujours pas. Il faut que tu ajoute le nom de famille de Thomas qui est: 'BERGER'"""
new_body_response = improve_email_response(user_input)
print(new_body_response)
