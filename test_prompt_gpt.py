
import json
from colorama import Fore, init
import openai
import time
import statistics



######################## GPT - 3.5 turbo API SETTINGS ########################
openai.organization = "org-YSlFvq9rM1qPzM15jewopUUt"
openai.api_key = "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"
init(autoreset=True)


def get_prompt_response(formatted_prompt):
    """Returns the prompt response"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "assistant", "content": formatted_prompt}],
    )
    return response

def gpt_new_mail_recommendation(mail_content, email_subject, user_recommendation):
    template = """As an email assistant, enhance the subject and body of this email in both QUANTITY and QUALITY in FRENCH according to the user guideline: '{user_recommendation}', while preserving key details from the original version.
    
    Answer must be a Json format with two keys: subject (STRING) AND body (HTML)

    subject: {email_subject},
    body: {mail_content}
    """
    formatted_prompt = template.format(user_recommendation=user_recommendation, email_subject=email_subject, mail_content=mail_content)
    response = get_prompt_response(formatted_prompt)    
    clear_text = response.choices[0].message['content'].strip()

    result_json = json.loads(clear_text)
    subject_text = result_json['subject']
    email_body = result_json['body']
    
    print(f"{Fore.GREEN}Subject: {subject_text}")
    print(f"{Fore.LIGHTGREEN_EX}Email Body: {email_body}")

    return subject_text, email_body

examples = [
    ("<p>slt cv jsp koi dir. si tu voi ca c que test a march ✌️😊</p>", "msg de test ala tem", "fais un messge poli et long"),
    ("<p>Salut <strong>papi</strong> cv ? nous on séclate en Espagne!!! on ador la piscine. Claude et la fam</p>", "NEws des vacs", "étoffe les expérience en embelissant et inventant un peu"),
]




for example in examples:
    mail_content, email_subject, user_recommendation = example

    # Record the start time
    start_time = time.time()

    # Call the function with different roles
    result = gpt_new_mail_recommendation(mail_content, email_subject, user_recommendation)

    elapsed_time = time.time() - start_time
    # Print the output
    # print(f'{Fore.LIGHTBLUE_EX}{result}')
    print(f"Elapsed Time: {elapsed_time} seconds\n")
