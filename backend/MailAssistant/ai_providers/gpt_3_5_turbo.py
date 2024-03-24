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
    """Enhance email subject and body in French"""

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


def new_mail_recommendation(mail_content, email_subject, user_recommendation):
    """Enhance email subject and body in FRENCH based on user guideline"""

    template = """As an email assistant, enhance the subject and body of this email in both QUANTITY and QUALITY in FRENCH according to the user guideline: '{user_recommendation}', while preserving key details from the original version.
    
    Answer must be a Json format with two keys: subject (STRING) AND body (HTML)

    subject: {email_subject},
    body: {mail_content}
    """
    formatted_prompt = template.format(
        user_recommendation=user_recommendation,
        email_subject=email_subject,
        mail_content=mail_content,
    )
    response = get_prompt_response(formatted_prompt)
    clear_text = response.choices[0].message.content.strip()

    result_json = json.loads(clear_text)
    subject_text = result_json["subject"]
    email_body = result_json["body"]

    print(f"{Fore.CYAN}NEW EMAIL RECOMMENDATION:")
    print(f"{Fore.GREEN}Subject: {subject_text}")
    print(f"{Fore.LIGHTGREEN_EX}Email Body: {email_body}")

    return subject_text, email_body


def generate_email(input_data, length, formality):
    """Generate a French email, enhancing both QUANTITY and QUALITY according to user guidelines."""

    template = """As an email assistant, write a {length} and {formality} email in FRENCH.
    Improve the QUANTITY and QUALITY in FRENCH according to the user guideline: '{input_data}', it should strictly contain only the information present in the input.

    Answer must be a Json format with two keys: subject (STRING) AND body IN HTML FORMAT (HTML)
    """
    formatted_prompt = template.format(
        input_data=input_data, length=length, formality=formality
    )
    response = get_prompt_response(formatted_prompt)

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
    """Generates a French email response based on the given response type"""
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


# TODO: update with claude and mistral prompt engineering
def categorize_and_summarize_email(
    subject: str, decoded_data: str, category_dict: dict, user_description: str
):
    """Categorizes and summarizes an email"""

    category_dict.pop(DEFAULT_CATEGORY)

    template = """Given the following email:

    Subject:
    {subject}

    Text:
    {text}

    Description:
    {user}

    Using the provided categories:

    Topic Categories:
    {category}

    Importance Categories:
    {importance}

    Response Categories:
    {answer}

    Relevance Categories:
    {relevance}

    1. Please categorize the email by topic, importance, response, and relevance corresponding to the user description.
    2. In French: Summarize the following message
    3. In French: Provide a short sentence summarizing the email.

    ---

    Topic Categorization: [Model's Response for Topic Category]

    Importance Categorization (Taking User Description into account and only using Importance Categories):
    - Category 1: [Model's Response for Importance Category 1]
    - Percentage 1: [Model's Percentage for Importance Category 1]
    - Category 2: [Model's Response for Importance Category 2]
    - Percentage 2: [Model's Percentage for Importance Category 2]
    - Category 3: [Model's Response for Importance Category 3]
    - Percentage 3: [Model's Percentage for Importance Category 3]

    Response Categorization: [Model's Response for Response Category]

    Relevance Categorization: [Model's Response for Relevance Category]

    Résumé court en français: [Model's One-Sentence Summary en français without using response/relevance categorization]

    Résumé en français (without using importance, response or relevance categorization):
    - [Model's Bullet Point 1 en français]
    - [Model's Bullet Point 2 en français]
    ...
    """
    importance_list = {
        "Important": 'Items or messages that are of high priority, do not contain offers to "unsubscribe", and require immediate attention or action.',
        "Information": 'Details that are relevant and informative but may not require immediate action. Does not contain offers to "unsubscribe".',
        "Useless": 'Items or messages that contain offers to "unsubscribe", might not be relevant to all recipients, are redundant, or do not provide any significant value.',
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
    formatted_template = template.format(
        subject=subject,
        text=decoded_data,
        user=user_description,
        category=category_dict,
        importance=importance_list,
        answer=response_list,
        relevance=relevance_list,
    )

    response = get_prompt_response(formatted_template)
    clear_response = response.choices[0].message.content.strip()

    # Extracting Topic Categorization
    topic_category = clear_response.split("Topic Categorization: ")[1].split("\n")[0]

    # Extracting Importance/Action Categorization
    importance_categories = []
    importance_percentages = []
    for i in range(1, 4):
        cat_str = f"Category {i}: "
        perc_str = f"Percentage {i}: "
        importance_categories.append(clear_response.split(cat_str)[1].split("\n")[0])
        importance_percentages.append(clear_response.split(perc_str)[1].split("\n")[0])

    # Extracting Response Categorization
    response_category = clear_response.split("Response Categorization: ")[1].split(
        "\n"
    )[0]

    # Extracting Relevance Categorization
    relevance_category = clear_response.split("Relevance Categorization: ")[1].split(
        "\n"
    )[0]

    # Extracting one sentence summary
    short_sentence = clear_response.split("Résumé court en français: ")[1].split("\n")[
        0
    ]

    # Finding start of the summary
    match = re.search(
        r"Résumé en français(\s\(without using importance, response or relevance categorization\))?:",
        clear_response,
    )

    if match:
        # Adjusting the start index based on the match found
        summary_start = match.end()
    else:
        # Fallback or default behavior if the pattern is not found
        summary_start = -1  # Or handle this case as needed

    # Finding the end of the summary
    summary_end = clear_response.find("\n\n", summary_start)
    # If there's no double newline after the start, consider till the end of the string
    if summary_end == -1:
        summary_end = len(clear_response)

    # Extracting the summary if a valid start index was found
    if summary_start != -1:
        summary_text = clear_response[summary_start:summary_end].strip()
    else:
        summary_text = "Summary not found."

    return (
        topic_category,
        importance_categories,
        response_category,
        summary_text,
        short_sentence,
        relevance_category,
        importance_percentages,
    )
