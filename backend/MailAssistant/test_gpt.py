import openai
import json
from colorama import Fore, init
import time

start_time = time.time()


######################## GPT - 3.5 turbo API SETTINGS ########################
init(autoreset=True)


######################## TEXT PROCESSING UTILITIES ########################
def get_prompt_response(formatted_prompt):
    """Returns the prompt response"""
    client = openai.OpenAI(organization="org-YSlFvq9rM1qPzM15jewopUUt", api_key="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")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "assistant",
            "content": formatted_prompt
        }]
    )
    return response

def gpt_langchain_redaction(input_data, length, formality):
    """Generate a French email, enhancing both QUANTITY and QUALITY according to user guidelines."""

    template = """As an email assistant, write a {length} and {formality} email in FRENCH.
    Improve the QUANTITY and QUALITY in FRENCH according to the user guideline: '{input_data}', it should strictly contain only the information present in the input.

    Answer must be a Json format with two keys: subject (STRING) AND body (HTML)
    """
    formatted_prompt = template.format(input_data=input_data, length=length, formality=formality)
    response = get_prompt_response(formatted_prompt)

    clear_text = response.choices[0].message.content.strip()
    result_json = json.loads(clear_text)

    subject_text = result_json.get('subject')
    email_body = result_json.get('body')

    print(f"{Fore.CYAN}{length} and {formality} email suggestion:")
    print(f"{Fore.GREEN}Subject: {subject_text}")
    print(f"{Fore.CYAN}Email Body: {email_body}")

gpt_langchain_redaction("Je serais absent à la réunion de vendredi", "Short", "Formal")

execution_time = time.time() - start_time

print(f"Le temps d'exécution du script est de {execution_time} secondes.")

    