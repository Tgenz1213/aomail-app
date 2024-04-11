"""
Handles prompt engineering requests for GPT-3.5-turbo API.
"""

from colorama import Fore, init
from MailAssistant.constants import DEFAULT_CATEGORY, OPENAI_CREDS
import json
import re
import openai
import ast


######################## GPT - 3.5 turbo API SETTINGS ########################
init(autoreset=True)


######################## TEXT PROCESSING UTILITIES ########################
def get_prompt_response(formatted_prompt):
    """Returns the prompt response"""
    client = openai.OpenAI(
        organization=OPENAI_CREDS["organization"], api_key=OPENAI_CREDS["api_key"]
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
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
    template = """"As an intelligent email assistant, analyze the input to categorize email recipients into main, cc, and bcc categories based on the presence of keywords and context that suggest copying or blind copying. Here's the input: '{query}'.

    Guidelines for classification:
    - Main recipients are those directly mentioned or implied to be the primary audience, without specific indicators for copying.
    - CC (carbon copy) recipients are identified through the context or subtle cues that imply they should be informed of the communication. Look for any keywords or phrases, even if indirectly stated, that traditionally associate with copying someone on an email.
    - BCC (blind carbon copy) recipients are identified similarly by context or cues suggesting a need for discretion or privacy in copying, without directly mentioning them in the conversation.

    If the input does not clearly differentiate between main, cc, and bcc recipients, use intuitive rules and a careful analysis of the text structure and any potential copying-related keywords or implications:
    1. Names appearing first or separated by phrases indicating inclusion (e.g., 'and', 'et') without clear copying context are considered as main recipients.
    2. Utilize any linguistic or structural clues to infer if a recipient is intended for CC or BCC, focusing on the broader context rather than explicit markers

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
    main_recipients = recipients.get("main_recipients", [])
    cc_recipients = recipients.get("cc_recipients", [])
    bcc_recipients = recipients.get("bcc_recipients", [])

    print(f"{Fore.CYAN}Main Recipients: {main_recipients}")
    print(f"{Fore.BLUE}Carbon Copy: {cc_recipients}")
    print(f"{Fore.GREEN}Blind Carbon Copy: {bcc_recipients}")

    return main_recipients, cc_recipients, bcc_recipients


# ----------------------- PREPROCESSING REPLY EMAIL -----------------------#
def generate_response_keywords(input_email, input_subject, language) -> list:
    """Generate a list of keywords for responding to a given email."""

    template = """As an email assistant, and given the email with subject: '{input_subject}' and body: '{input_email}' written in {language}.

    IDENTIFY up to 4 different ways to respond to this email.
    USE as few verbs in {language} as possible while keeping a relevant meaning.
    KEYWORDS must look like buttons the user WILL click to reply to the email.

    Answer must be a list (Python) format: ["....", "....."]
    """
    formatted_prompt = template.format(
        input_subject=input_subject, input_email=input_email, language=language
    )
    response = get_prompt_response(formatted_prompt)
    keywords = response.choices[0].message.content.strip()

    print(f"{Fore.YELLOW}{keywords}")

    keywords_list = ast.literal_eval(keywords)

    return keywords_list


def shorten_keywords(keywords) -> dict:
    """Shorten each keyword in the given list"""

    formatted_prompt = f"""As an email assistant,

    Given this list of keywords '{keywords}', GENERATE a shorter version for each keyword/
    

    Answer must be a Json format with KEYS being each NEW keyword and values being each associated old keyword
    """
    response = get_prompt_response(formatted_prompt)
    keywords_dict = json.loads(response.choices[0].message.content.strip())

    print(f"{Fore.YELLOW}{keywords_dict}")

    return keywords_dict


######################## WRITING ########################
def improve_email_writing(body, subject):
    """Enhance email subject and body"""

    language = get_language(body, subject).upper()

    template = f"""As an email assistant, enhance the subject and body of this email in both QUANTITY and QUALITY in {language}, while preserving key details from the original version.
    
    Answer must be a Json format with two keys: subject (STRING) AND body (HTML)

    subject: {subject},
    body: {body}
    """
    response = get_prompt_response(template)
    clear_text = response.choices[0].message.content.strip()
    result_json = json.loads(clear_text)

    subject_text = result_json["subject"]
    email_body = result_json["body"]

    print(f"{Fore.CYAN}EMAIL DRAFT IMPROVED:")
    print(f"{Fore.GREEN}Subject: {subject_text}")
    print(f"{Fore.CYAN}Email Body: {email_body}")

    return email_body, subject_text


def new_mail_recommendation(
    mail_content, email_subject, user_recommendation, language="FRENCH"
):
    """Enhance email subject and body based on user guideline"""

    template = f"""As an email assistant, enhance the subject and body of this email in both QUANTITY and QUALITY in {language} according to the user guideline: '{user_recommendation}', while preserving key details from the original version.
    
    Answer must be a Json format with two keys: subject (STRING) AND body (HTML)

    subject: {email_subject},
    body: {mail_content}
    """
    response = get_prompt_response(template)
    clear_text = response.choices[0].message.content.strip()

    result_json = json.loads(clear_text)
    subject_text = result_json["subject"]
    email_body = result_json["body"]

    print(f"{Fore.CYAN}NEW EMAIL RECOMMENDATION:")
    print(f"{Fore.GREEN}Subject: {subject_text}")
    print(f"{Fore.LIGHTGREEN_EX}Email Body: {email_body}")

    return subject_text, email_body


def generate_email(input_data, length, formality, language="FRENCH"):
    """Generate an email, enhancing both QUANTITY and QUALITY according to user guidelines."""

    template = f"""As an email assistant, write a {length} and {formality} email in {language}.
    Improve the QUANTITY and QUALITY in {language} according to the user guideline: '{input_data}', it should strictly contain only the information present in the input.

    Answer must be a Json format with two keys: subject (STRING) AND body IN HTML FORMAT (HTML)
    """
    response = get_prompt_response(template)

    clear_text = response.choices[0].message.content.strip()
    result_json = json.loads(clear_text)

    subject_text = result_json.get("subject")
    email_body = result_json.get("body")

    print(f"{Fore.CYAN}{length} and {formality} email suggestion:")
    print(f"{Fore.GREEN}Subject: {subject_text}")
    print(f"{Fore.CYAN}Email Body: {email_body}")

    return subject_text, email_body


def correct_mail_language_mistakes(body, subject):
    """Corrects spelling and grammar mistakes in the email subject and body based on user's request."""

    language = get_language(body, subject).upper()

    template = f"""As an email assistant, check the following {language} text for any grammatical or spelling errors and correct them, Do not change any words unless they are misspelled or grammatically incorrect.
    
    Answer must be a Json format with two keys: subject (STRING) AND body (HTML)

    subject: {subject},
    body: {body}
    """
    response = get_prompt_response(template)
    clear_text = response.choices[0].message.content.strip()
    result_json = json.loads(clear_text)

    corrected_subject = result_json["subject"]
    corrected_body = result_json["body"]

    print(f"{Fore.CYAN}EMAIL CORRECTED:")
    print(f"{Fore.GREEN}Subject: {corrected_subject}")
    print(f"{Fore.CYAN}Email Body: {corrected_body}")

    # Count the number of corrections
    num_corrections = count_corrections(
        subject, body, corrected_subject, corrected_body
    )

    return corrected_subject, corrected_body, num_corrections


# TODO: improve prompt engineering + get a json response from GPT
def improve_email_copywriting(email_subject, email_body):
    """Provides feedback and suggestions for improving the copywriting in the email subject and body."""

    # Simplified template for direct feedback and suggestions on copywriting
    template = """Évaluez en français la qualité du copywriting du sujet et du corps de cet e-mail. Fournissez un retour et des suggestions d'amélioration.

    Objet de l'e-mail :
    "{email_subject}"

    Corps de l'e-mail :
    "{email_body}"

    ---

    <strong>Retour sur l'objet</strong> :
    [Votre retour sur l'objet]

    <strong>Suggestions pour l'objet</strong> :
    [Vos suggestions pour l'objet]

    <strong>Retour sur le corps de l'e-mail</strong> :
    [Votre retour sur le corps de l'e-mail]

    <strong>Suggestions pour le corps de l'e-mail</strong> :
    [Vos suggestions pour le corps de l'e-mail]
    """

    formatted_prompt = template.format(
        email_subject=email_subject, email_body=email_body
    )
    response = get_prompt_response(formatted_prompt)
    response_text = response.choices[0].message.content.strip()

    print(f"{Fore.CYAN}EMAIL COPYWRITING:")
    print(f"{Fore.GREEN}{response_text}")

    return response_text


def generate_email_response(input_subject, input_body, response_type, language):
    """Generates an email response based on the given response type"""
    template = """Based on the email with the subject: '{input_subject}' and body: '{input_body}' craft a response in {language} following the '{response_type}' instruction. Ensure the response is structured as an HTML email. Here is a template to follow, with placeholders for the dynamic content:
    <p>[Insert greeting]</p><!-- Insert response here based on the input body and the specified response type --><p>[Insert sign_off],</p><p>[Your Name]</p>

    ----

    Answer must be above HTML without spaces
    """
    # DO NOT DELETE : possible upgrade TO TEST (something like this in the template) : craft a response in {language} following the '{response_type}' instruction, do not invent new demands that the user didn't ask, ONLY IF NECESSARY you can leave blank space after ':' if you want the user to manually complete the answer
    formatted_prompt = template.format(
        input_subject=input_subject,
        input_body=input_body,
        response_type=response_type,
        language=language,
    )
    response = get_prompt_response(formatted_prompt)
    body = response.choices[0].message.content.strip()

    print(f"{Fore.GREEN}[REPLY] body: {body}")

    return body


####################################################################
######################## UNDER CONSTRUCTION ########################
####################################################################


def categorize_and_summarize_email(
    subject: str,
    decoded_data: str,
    category_dict: dict,
    user_description: str,
    language="French",
):
    """Categorizes and summarizes an email"""

    category_dict.pop(DEFAULT_CATEGORY)

    importance_list = {
        "Important": "Messages that are high priority, require immediate attention or action, and are relevant to the user.",
        "Information": "Details that are relevant and informative to the user but may not necessarily require immediate action.",
        "Useless": "Messages that are not relevant to the user, are redundant, do not provide significant value, or are newsletters or commercial offers. If uncertain, it's preferable to categorize the message as 'Useless' because the user can correct the classification later.",
    }
    response_list = {
        "Answer Required": "Message requires an answer.",
        "Might Require Answer": "Message might require an answer.",
        "No Answer Required": "No answer is required.",
    }
    relevance_list = {
        "Highly Relevant": "Message is highly relevant to the recipient.",
        "Possibly Relevant": "Message might be relevant to the recipient.",
        "Not Relevant": "Message is not relevant to the recipient.",
    }

    template = f"""Given the following email:

    Subject:
    {subject}

    Text:
    {decoded_data}

    Description:
    {user_description}

    Using the provided categories:

    Topic Categories:
    {category_dict}

    Importance Categories:
    {importance_list}

    Response Categories:
    {response_list}

    Relevance Categories:
    {relevance_list}

    1. Please categorize the email by topic, importance, response, and relevance corresponding to the user description. (regarding the topic category, you need to be sure of the choice made, if you hesitate put it in the Others category)
    2. In {language}: Summarize the following email using description nouns or infinitive verbs structures according to the information for each bullet point.
    3. In {language}: Provide up to 3 short bullet points WITHOUT making any judgment or interpretation, they should be clear and as short as possible. Do NOT add any redundant information and SPEAK ONLY about the content NOT about the name of the sender or greetings or unecessary details.
    4. In {language}: Provide a VERY SHORT sentence summarizing the core content of the email without giving ANY details.
    Remember, regardless of the email's perceived relevance or importance, a summary is always required. This summary should objectively reflect the content of the email without making subjective judgments about its relevance.

    ---
    Answer must be a Json format matching this template:
    {{
        "topic": Topic Title Category,
        "response": Response Category,
        "relevance": Relevance Category,
        "summary": {{
            "one_line": One-Sentence Summary in {language},
            "complete": [
                "Short Bullet Point 1",
                "Short Bullet Point 2",
                ...
            ]
        }},
        "importance": {{
            "UrgentWorkInformation": Percentage for UrgentWorkInformation,
            "RoutineWorkUpdates": Percentage for RoutineWorkUpdates,
            "InternalCommunications": Percentage for InternalCommunications,
            "Promotional": Percentage for Promotional,
            "News": Percentage for News 
        }}
    }}
    """
    response = get_prompt_response(template)
    clear_response = response.choices[0].message.content.strip()
    result_json = json.loads(clear_response)

    print("GPT 3.5 turbo")
    print(clear_response)

    topic = result_json["topic"]
    response = result_json["response"]
    relevance = result_json["relevance"]
    short_sentence = result_json["summary"]["one_line"]
    summary_list = result_json["summary"]["complete"]
    importance_dict = result_json["importance"]

    # convert percentages to int
    for key, value in importance_dict.items():
        importance_dict[key] = int(value)

    return (
        topic,
        importance_dict,
        response,
        summary_list,
        short_sentence,
        relevance,
    )
