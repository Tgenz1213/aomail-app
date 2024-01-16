import json
from colorama import Fore, init
import openai
import time



######################## GPT - 3.5 turbo API SETTINGS ########################
ORGANIZATION = "org-YSlFvq9rM1qPzM15jewopUUt"
API_KEY = "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"
init(autoreset=True)



def get_prompt_response_gpt_4(formatted_prompt):
    """Returns the prompt response"""
    client = openai.OpenAI(organization=ORGANIZATION, api_key=API_KEY)
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{
            "role": "system",
            "content": formatted_prompt
        }]
    )
    return response

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


######################## PREPROCESSING ########################
def get_language(input_subject, input_body):
    """Returns the primary language used in the email"""
    template = """Given an email with subject: '{input_subject}' and body: '{input_body}',
    IDENTIFY the primary language used (e.g., French, English, Russian), prioritizing the body over the subject.
    
    Provide the answer in JSON format with the key 'language' (STRING).
    """
    formatted_prompt = template.format(input_body=input_body, input_subject=input_subject)
    response = get_prompt_response(formatted_prompt)
    clear_text = response.choices[0].message.content.strip()
    language = json.loads(clear_text)["language"]

    print(f'{Fore.LIGHTBLUE_EX}The language used is: {language}')

    return language


def generate_response_keywords(input_subject, input_email, language) -> list:
    template = """As an email assistant, and given the email with subject: '{input_subject}' and body: '{input_email}' written in {language}.

    IDENTIFY up to 4 different ways to respond to this email.
    USE as few verbs in {language} as possible while keeping a relevant meaning.
    KEYWORDS must look like buttons the user WILL click to reply to the email.

    Answer must be a list (Python) format: []
    """
    formatted_prompt = template.format(input_subject=input_subject, input_email=input_email, language=language)
    #response = get_prompt_response(formatted_prompt)
    response = get_prompt_response(formatted_prompt)
    keywords = response.choices[0].message.content.strip()

    print(f'{Fore.YELLOW}{keywords}')

    return keywords

def shorten_keywords(keywords):
    formatted_prompt = f"""As an email assistant,

    Givent this list of keywords '{keywords}', GENERATE a shorter version for each keyword/
    

    Answer must be a Json format with KEYS being each NEW keyword and values being each associated old keyword
    """
    response = get_prompt_response(formatted_prompt)
    keywords_dict = json.loads(response.choices[0].message.content.strip())

    print(f'{Fore.YELLOW}{keywords_dict}')

    return keywords_dict


def generate_email_response(input_subject, input_body, response_type, language):
    """Generates a French email response based on the given response type"""
    template = """As an email assistant, REPLY in {language} to the email with subject: '{input_subject}' and body: '{input_body}'.

    Based on the user indication: '{response_type}', REPLY to the email without adding any new details.
    It should STRICTLY correspond to the information present in the original email.

    Answer must ONLY be an HTML email body
    """
    formatted_prompt = template.format(input_subject=input_subject, input_body=input_body, response_type=response_type, language=language)
    #response = get_prompt_response_gpt_4(formatted_prompt)
    response = get_prompt_response_gpt_4(formatted_prompt)
    clear_text = response.choices[0].message.content.strip()
    body = clear_text

    print(f'{Fore.GREEN}body: {body}')

    return body




start = time.time()



subject =  "Coupure Internet Angers 16/01 à partir de 18h30"
body = """
<html>
Bonjour,

En raison d'une opération de maintenance visant à renforcer la sécurité de notre connexion Internet, celle-ci sera interrompue le mardi 16 janvier à partir de 18h30 jusqu'à minuit au moins.

Les impacts prévus sont les suivants :

    Aucun accès à Internet à Angers.

    Indisponibilité des ressources informatiques d'Angers depuis Aix ou Reims (partages réseaux, etc)
    Veuillez noter que l'accès Internet des sites distants ne sera pas affecté.

    Plus d'accès VPN via le Forticlient.

Merci d’avance pour votre patience et pour votre compréhension.

Excellente fin de journée et bon week-end,
</html>
"""



# REPLY in 4 steps:

# get language
language = get_language(subject, body)

# long keywords list
keywords = generate_response_keywords(subject, body, language)
# short keywords dict
keywords_dict = shorten_keywords(keywords)


"""just to test"""
keyword = list(keywords_dict.values())[0]


# HTML response
generate_email_response(subject, body, keyword, language)



total_time = time.time() - start

print(f"Elapsed time: {total_time} seconds")