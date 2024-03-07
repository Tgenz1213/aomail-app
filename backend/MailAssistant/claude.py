"""
Handles prompt engineering requests for Claude 3 API.
"""

import json
import anthropic
from colorama import Fore, init


######################## Claude 3 API SETTINGS ########################
CLAUDE_CREDS = json.load(open("backend/creds/claude_creds.json", "r"))
init(autoreset=True)


######################## TEXT PROCESSING UTILITIES ########################
def get_prompt_response(formatted_prompt):
    """Returns the prompt response"""
    client = anthropic.Anthropic(api_key=CLAUDE_CREDS["api_key"])
    response = client.completions.create(
        model="claude-3-opus-20240229",
        messages=[{"role": "assistant", "content": formatted_prompt}],
    )
    return response


def get_language(input_subject, input_body):
    """Returns the primary language used in the email"""

    template = """Given an email with subject: '{input_subject}' and body: '{input_body}',
    IDENTIFY the primary language used (e.g., French, English, Russian), prioritizing the body over the subject.
    
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