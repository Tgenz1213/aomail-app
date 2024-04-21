"""
Handles prompt engineering requests for Llama 3 API.
"""

import json
import groq
from colorama import Fore, init
from MailAssistant.constants import LLAMA_CREDS

######################## Llama 3 API SETTINGS ########################
init(autoreset=True)


######################## TEXT PROCESSING UTILITIES ########################
def get_prompt_response(formatted_prompt):
    """Returns the prompt response"""
    client = groq.Groq(api_key=LLAMA_CREDS["api_key"]
    )
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "assistant", "content": formatted_prompt}],
    )
    return response


def get_language(input_body, input_subject) -> str:
    """Returns the primary language used in the email"""

    template = """Given an email with subject: '{input_subject}' and body: '{input_body}',
    IDENTIFY the primary language used (e.g: French, English, Russian), prioritizing the body over the subject.
    
    Provide the answer in JSON format with the key 'language' (STRING).
    """
    formatted_prompt = template.format(
        input_body=input_body, input_subject=input_subject
    )
    response = get_prompt_response(formatted_prompt)
    clear_text = response.choices[0].message.content.strip()
    language = json.loads(clear_text)["language"]

    print(f"{Fore.LIGHTBLUE_EX}The language used is: {language}")

    return language


get_language("ceci est un email de test llama", "ceci est juste un sujet")