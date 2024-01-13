"""
Handles prompt engineering requests for GPT-3.5-turbo API.
"""
import logging
import re
import openai



######################## GPT - 3.5 turbo API SETTINGS ########################
openai.organization = "org-YSlFvq9rM1qPzM15jewopUUt"
openai.api_key = "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"



# TO UPDATE : make work with langchain
def extract_contacts_recipients(input_query):
    # Define the prompt template for ChatGPT
    template = """
    Analyze the following input to determine recipients for an email :

    {input_query}

    Format the response as (if no CC or CCI are indicate, put in main):
    1. Main recipients: [username/email, username/email, ...]
    2. CC recipients: [username/email, username/email, ...]
    3. BCC recipients: [username/email, username/email, ...]
    """

    formatted_prompt = template.format(input_query=input_query)

    # Call the OpenAI API
    '''
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=formatted_prompt,
        max_tokens=150,
        api_key=openai.api_key 
    )

    response_text = response.choices[0].text.strip()

    '''
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": formatted_prompt}],
        api_key=openai.api_key )

    response_text = response.choices[0].message['content'].strip()

    logging.info("Received response from ChatGPT: %s", response_text)

    if response_text == "INCORRECT":
        return "INCORRECT", "INCORRECT", "INCORRECT"

    # Define a function to extract items from the response
    def extract_items(response, marker):
        pattern = re.escape(marker) + r"\: \[(.*?)\]"
        match = re.search(pattern, response)
        if match:
            items = match.group(1).split(", ")
            return [item.strip() for item in items]
        else:
            return []

    # Extract information based on markers
    main_recipients = extract_items(response_text, "1. Main recipients")
    cc_recipients = extract_items(response_text, "2. CC recipients")
    bcc_recipients = extract_items(response_text, "3. BCC recipients")

    logging.info("Extracted response from ChatGPT (main): %s", main_recipients)
    logging.info("Extracted response from ChatGPT (CC): %s", cc_recipients)
    logging.info("Extracted response from ChatGPT (BCC): %s", bcc_recipients)

    return main_recipients, cc_recipients, bcc_recipients


def improve_email_copywriting(email_subject, email_body):
    """Provides feedback and suggestions for improving the copywriting in the email subject and body."""

    # Simplified template for direct feedback and suggestions on copywriting
    template = """
    Évaluez en français la qualité du copywriting du sujet et du corps de cet e-mail. Fournissez un retour et des suggestions d'amélioration.

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

    formatted_prompt = template.format(email_subject=email_subject, email_body=email_body)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": formatted_prompt}],
        api_key=openai.api_key
    )

    response_text = response.choices[0].message['content'].strip()

    return response_text