"""
Handles prompt engineering requests for Claude 3 API.
"""

import json
import time
import anthropic
from colorama import Fore, init


######################## Claude 3 API SETTINGS ########################
CLAUDE_CREDS = json.load(open("backend/creds/claude_creds.json", "r"))
init(autoreset=True)


######################## TEXT PROCESSING UTILITIES ########################
def get_prompt_response(formatted_prompt):
    """Returns the prompt response"""
    client = anthropic.Anthropic(api_key=CLAUDE_CREDS["api_key"])
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0.0,
        messages=[{"role": "user", "content": formatted_prompt}],
    )
    return response


def get_language(input_subject, input_body):
    """Returns the primary language used in the email"""

    template = """\n\nHuman: Given an email with subject: '{input_subject}' and body: '{input_body}',
    IDENTIFY the primary language used (e.g: French, English, Russian), prioritizing the body over the subject.
    
    Provide ONLY the answer in JSON format with the key 'language' (STRING).
    
    Assistant:"""
    formatted_prompt = template.format(
        input_body=input_body, input_subject=input_subject
    )
    response = get_prompt_response(formatted_prompt)
    language = json.loads(response.content[0].text)["language"]

    print(f"{Fore.LIGHTBLUE_EX}The language used is: {language}")

    return language


def count_corrections(
    original_subject, original_body, corrected_subject, corrected_body
):
    """Count and compare corrections in original and corrected texts"""

    # Splitting the original and corrected texts into words
    original_subject_words = original_subject.split()
    corrected_subject_words = corrected_subject.split()
    original_body_words = original_body.split()
    corrected_body_words = corrected_body.split()

    # Counting the differences in the subject
    subject_corrections = sum(
        1
        for orig, corr in zip(original_subject_words, corrected_subject_words)
        if orig != corr
    )

    # Counting the differences in the body
    body_corrections = sum(
        1
        for orig, corr in zip(original_body_words, corrected_body_words)
        if orig != corr
    )

    # Total corrections
    total_corrections = subject_corrections + body_corrections

    return total_corrections


def extract_contacts_recipients(query):
    template = """"\n\nHuman: As an intelligent email assistant, analyze the input to categorize email recipients into main, cc, and bcc categories based on the presence of keywords and context that suggest copying or blind copying. Here's the input: '{query}'.

    Guidelines for classification:
    - Main recipients are those directly mentioned or implied to be the primary audience, without specific indicators for copying.
    - CC (carbon copy) recipients are identified through the context or subtle cues that imply they should be informed of the communication. Look for any keywords or phrases, even if indirectly stated, that traditionally associate with copying someone on an email.
    - BCC (blind carbon copy) recipients are identified similarly by context or cues suggesting a need for discretion or privacy in copying, without directly mentioning them in the conversation.

    If the input does not clearly differentiate between main, cc, and bcc recipients, use intuitive rules and a careful analysis of the text structure and any potential copying-related keywords or implications:
    1. Names appearing first or separated by phrases indicating inclusion (e.g., 'and', 'et') without clear copying context are considered as main recipients.
    2. Utilize any linguistic or structural clues to infer if a recipient is intended for CC or BCC, focusing on the broader context rather than explicit markers

    Return ONLY the results in JSON format with three keys:
    main_recipients: [Python list],
    cc_recipients: [Python list],
    bcc_recipients: [Python list]
    
    Assistant:"""
    formatted_prompt = template.format(query=query)
    response = get_prompt_response(formatted_prompt)
    recipients = json.loads(response.content[0].text)

    # Extract information based on markers
    main_recipients = recipients.get("main_recipients", [])
    cc_recipients = recipients.get("cc_recipients", [])
    bcc_recipients = recipients.get("bcc_recipients", [])

    print(f"{Fore.CYAN}Main Recipients: {main_recipients}")
    print(f"{Fore.BLUE}Carbon Copy: {cc_recipients}")
    print(f"{Fore.GREEN}Blind Carbon Copy: {bcc_recipients}")

    return main_recipients, cc_recipients, bcc_recipients


'''start_time = time.time()
get_language(
    "Yaxshimiziz",
    "Assalomu Aleykum, Meining ismi Augustin. Men Uzbek tilini organypman",
)
get_language("test d'email", "Salut, la team, cava? c'est juste un test")
get_language("Achtung bitte", "Hallo, ich habe nur ein Frage, Warum bist du langsamer als mistral?")

execution_time = time.time() - start_time

print(f"{Fore.GREEN}Le temps d'exécution du script n°2 est de {execution_time} secondes.")'''



'''start_time = time.time()
extract_contacts_recipients("envoie à jean et à claude")
execution_time = time.time() - start_time

print(
    f"{Fore.GREEN}Le temps d'exécution du script n°2 est de {execution_time} secondes."
)'''
