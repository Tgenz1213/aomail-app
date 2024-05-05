"""
Test file to handle chat bot conv

UNDER DEV everything is hard coded

TODO: store the conversation in sessionStorage and find a way to always clean when user refreshes the page, 
close it or send email or there is a network issue
"""

import anthropic
from langchain.memory import ChatMessageHistory
from colorama import Fore, init
from constants import CLAUDE_CREDS, HUMAN, ASSISTANT

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


class EmailReplyConversation:
    """Handles the conv with the AI to reply to an email."""

    def __init__(self, user, importance: str, subject: str, body: str) -> None:
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
        """Improves the email response according to the history of conversation."""

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
        Do not justify neither explain your reasoning only give the HTML response.

        ---
        Answer must include all new changes and match the same HTML format
        {ASSISTANT}
        """
        response = get_prompt_response(template)
        body = response.content[0].text.strip()

        print(f"{Fore.BLUE}[REPLY modified] body: {body}")

        self.update_history(user_input, body)

        return body


subject = "Préparation missions été CESAME"
importance = "Informative"
body = """Bonjour Augustin,

 

Pierre m'a fait part d'un besoin pour cet été d'avoir un renfort dans l'équipe pour l'aider au Cesame sur la partie déploiement du wifi et déploiement des postes de travail dans les services.

Nous avons pensé à toi au vu de ton passage dans le service en début d'année lors de ton stage qui a été satisfaisant de notre côté, tant pour ta bonne humeur que ton autonomie dans le travail.

 

Je te propose donc un poste en CDD d'un mois, du 31 juillet 2023 jusqu'au 1 septembre 2023.

Le poste est proposé sur un grade d'agent de catégorie C.

 

Si tu es intéressé, merci de me recontacter dans les prochains jours, afin que l'on puisse organiser le contrat avec le service RH.

 

Cordialement,

 

Monsieur Martin,

Responsable des Systèmes d'Information

Service Informatique"""

# this simulates the button
user_instruction = "Accepter l'opportunité de monter en compétences"
# this simulates the first response
body_response = generate_email_response(subject, body, user_instruction, "French")

# create an EmailReplyConversation ONLY if the user replied to the question of the AI
email_reply_conv = EmailReplyConversation(
    "augustin", importance, subject, body_response
)

# TODO: display new_body_response in FE
user_input = """Non,
Je veux que tu rajoute ma signature: Augustin ROLET ainsi que le fait que je suis très reconnaissant d'avoir été choisi"""
new_body_response = email_reply_conv.improve_email_response(user_input)
user_input = "Fais plus court et simplifie les phrases"
new_body_response = email_reply_conv.improve_email_response(user_input)
print(email_reply_conv.history)
