######################## GPT - 3.5 turbo API SETTINGS ########################
import json
from colorama import Fore
import openai


ORGANIZATION = "org-YSlFvq9rM1qPzM15jewopUUt"
API_KEY = "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"



def get_prompt_response(formatted_prompt):
    """Returns the prompt response"""
    client = openai.OpenAI(organization=ORGANIZATION, api_key=API_KEY)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "assistant",
            "content": formatted_prompt
        }]
    )
    return response


def extract_contacts_recipients(query):
    template = """I am not able to fix this error. Provide me a valid code please

    {query}
    """
    formatted_prompt = template.format(query=query)
    response = get_prompt_response(formatted_prompt)
    response_text = response.choices[0].message.content.strip()    
    print(response_text)


query = """
tr en fr

notificationMessage = 'Votre Background a ete mis a jour';
"""


extract_contacts_recipients(query)