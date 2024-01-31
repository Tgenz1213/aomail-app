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
    template = """As an email assistant,

    Analyze the following input: '{query}' to determine recipients for an email. Follow these rules:

    1. If no main recipients are explicitly indicated, assume all recipients are main recipients.
    2. If no CC or BCC recipients are specified, include all recipients in the main_recipients list.

    Return the results in JSON format with three keys:
    main_recipients: [Python list],
    cc_recipients: [Python list],
    bcc_recipients: [Python list]    
    """
    formatted_prompt = template.format(query=query)
    response = get_prompt_response(formatted_prompt)
    response_text = response.choices[0].message.content.strip()    
    recipients = json.loads(response_text)

    # Extract information based on markers
    main_recipients = recipients.get('main_recipients', [])
    cc_recipients = recipients.get('cc_recipients', [])
    bcc_recipients = recipients.get('bcc_recipients', [])

    print(f"{Fore.CYAN}Main Recipients: {main_recipients}")
    print(f"{Fore.BLUE}Carbon Copy: {cc_recipients}")
    print(f"{Fore.GREEN}Blind Carbon Copy: {bcc_recipients}")

    return main_recipients, cc_recipients, bcc_recipients


query = "mail à Carter,  Taylor et Isabell. En copie caché met Mitchell & Grace. En copi simple: Sophia et madison"


extract_contacts_recipients(query)