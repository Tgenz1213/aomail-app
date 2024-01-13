"""
Handles prompt engineering requests for GPT-4 API.
"""
import openai



######################## GPT - 4 API SETTINGS ########################
openai.organization = "org-YSlFvq9rM1qPzM15jewopUUt"
openai.api_key = "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"



######################## REDACTION ########################
# TODO: gpt-3.5-turbo => TO FIX AND TO FIND THE BEST PROMPT
def gpt_langchain_redaction(input_data, length, formality):
    template = """
        Given the following draft:

        "{input_data}"

        Please follow these instructions carefully:
        1. Write a short subject for the email based on the draft in French.
        2. Write an email in French that matches the length and content of the input. The email should be {length}, {formality}, and should strictly contain only the information present in the input. Do not add any new details or information.
        ---

        Subject:
        [Model's drafted subject]

        Draft:
        [Model's drafted email]
    """

    formatted_prompt = template.format(input_data=input_data, length=length, formality=formality)

    print("FORMATTED PROMPT", formatted_prompt)

    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview", # gpt-3.5-turbo => TO FIX AND TO FIND THE BEST PROMPT
        messages=[{"role": "system", "content": formatted_prompt}],
        api_key=openai.api_key
    )

    clear_text = response.choices[0].message['content'].strip()

    print('clear_text: ',clear_text)

    # Extracting Subject
    subject_start = clear_text.index("Subject:") + len("Subject:")
    subject_end = clear_text[subject_start:].index("\n\n") if "\n\n" in clear_text[subject_start:] else len(clear_text)
    subject_list = clear_text[subject_start:subject_start+subject_end].strip().split("\n")
    subject_text = "\n".join(subject_list)

    # Extracting Email
    mail_start = clear_text.index("Draft:") + len("Draft:")
    mail_list = clear_text[mail_start:len(clear_text)].strip().split("\n")
    mail_text = "\n".join(mail_list)

    print("Email :", mail_text)

    return subject_text, mail_text


def gpt_new_mail_recommendation(mail_content, user_recommendation, email_subject):
    template = """
        Consider the following email subject, content, and user recommendation in French:

        Email Subject:
        "{email_subject}"

        Email Content:
        "{mail_content}"

        User Recommendation:
        "{user_recommendation}"

        Based on the user recommendation, modify the email while keeping as much of the original content and intent as possible. Please provide:
        1. An revised subject for the email, if the recommendation suggests a change.
        2. A revised body of the email that incorporates the recommendation without altering the original message unnecessarily.

        ---

        Subject:
        [Adjusted Email Subject]

        Email Body:
        [Revised Email Body]
    """

    formatted_prompt = template.format(mail_content=mail_content, user_recommendation=user_recommendation, email_subject=email_subject)

    print("FORMATTED PROMPT", formatted_prompt)

    # Replace 'openai.api_key' with your actual OpenAI API key
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview", # gpt-3.5-turbo => TO FIX AND TO FIND THE BEST PROMPT
        messages=[{"role": "system", "content": formatted_prompt}],
        api_key=openai.api_key
    )

    clear_text = response.choices[0].message['content'].strip()

    print('clear_text: ', clear_text)

    # Extract the subject and body of the email
    subject_start = clear_text.index("Subject:") + len("Subject:")
    subject_end = clear_text.index("Email Body:")
    subject_text = clear_text[subject_start:subject_end].strip()

    body_start = subject_end + len("Email Body:")
    email_body = clear_text[body_start:].strip()

    print("Subject:", subject_text)
    print("Email Body:", email_body)

    return subject_text, email_body


# TODO: V1 template to upgrade to make work with GPT3
def correct_mail_language_mistakes(email_subject, email_body):
    """Corrects spelling and grammar mistakes in the email subject and body based on user's request."""    
    template = """
    Please check the following French text for any grammatical or spelling errors and correct them. Do not change any words unless they are misspelled or grammatically incorrect.

    Subject:
    "{email_subject}"

    Body:
    "{email_body}"

    ---

    Corrected Subject:
    [Corrected Subject]

    Corrected Body:
    [Corrected Body]
    """

    formatted_prompt = template.format(email_subject=email_subject, email_body=email_body)

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "system", "content": formatted_prompt}],
        api_key=openai.api_key
    )

    response_text = response.choices[0].message['content'].strip()

    print("Response Text : ", response_text)

    # Extract the corrected subject and body
    corrected_subject = extract_between_markers(response_text, "Corrected Subject:", "Corrected Body:")
    corrected_body = extract_after_marker(response_text, "Corrected Body:")

    # Count the number of corrections
    num_corrections = count_corrections(email_subject, email_body, corrected_subject, corrected_body)

    return corrected_subject, corrected_body, num_corrections



# Answer possibilities generation
'''
Given the following email content in French, identify different ways to respond to this email (maximum 4 NOT MORE). Only output in as less keywords as possible the ways to respond in French, do not output the mail answer

    Email Content:
    "{input_email}"

    ---

    French ways to respond :'''
def generate_response_keywords(input_email):
    template = """
    Given the following email content in French, identify different ways to respond to this email (maximum 4 NOT MORE). Only output as less keywords as possible in French with verbs, do not output the mail answer

    Email Content:
    "{input_email}"

    ---

    French ways to respond :
    """

    formatted_prompt = template.format(input_email=input_email)

    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",  # Replace with the correct model name
        messages=[{"role": "system", "content": formatted_prompt}],
        api_key=openai.api_key
    )

    response_text = response.choices[0].message['content'].strip()

    # Split the response text by line breaks and remove surrounding quotes
    keywords = [line.strip().strip('"') for line in response_text.split('\n') if line.strip()]

    return keywords


def generate_email_response(input_email, response_type):
    """Answer mail generation."""

    ''' WORK WITH GPT4
    template = """
    Given the following email content in French generate a mail response in French based on the response type. The response should not add any new information that is not asked by the user.

    Email Content:
    "{input_email}"

    Response Type:
    "{response_type}"

    ---

    French Response:
    """'''

    ''' NOT PERFECT BUT WORK EXCEPT WITH BUTTONS 
    Given an email written in French, generate a reply to this email also in French. The reply should be based on the indicated response type below and should strictly adhere to the information given in the email without adding any new details.

    Email Content:
    "{input_email}"

    Desired Response Type:
    "{response_type}"

    Please write a response that aligns with the given response type:

    Response:''' 

    template = """
    Given an email written in French, generate a reply to this email also in French. The reply should be based on the indicated response type below and should strictly adhere to the information given in the email without adding any new details.

    Email Content:
    "{input_email}"

    Desired Response Type:
    "{response_type}"

    Please write a response as that aligns with the given response type:

    Response:
    """

    formatted_prompt = template.format(input_email=input_email, response_type=response_type)

    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview", #gpt-4-1106-previewgpt-3.5-turbo
        messages=[{"role": "system", "content": formatted_prompt}],
        api_key=openai.api_key
    )

    return response.choices[0].message['content'].strip()



######################## TEXT EXTRACTION AND COMPARISON UTILITIES ########################
def extract_between_markers(text, start_marker, end_marker):
    start = text.find(start_marker) + len(start_marker)
    end = text.find(end_marker, start)
    if end > start:
        extracted_text = text[start:end].strip()
        return extracted_text.strip('"')  # Remove surrounding quotation marks
    return ""


def extract_after_marker(text, marker):
    start = text.find(marker) + len(marker)
    if start > -1:
        extracted_text = text[start:].strip()
        return extracted_text.strip('"')  # Remove surrounding quotation marks
    return ""


def count_corrections(original_subject, original_body, corrected_subject, corrected_body):
    # Splitting the original and corrected texts into words
    original_subject_words = original_subject.split()
    corrected_subject_words = corrected_subject.split()
    original_body_words = original_body.split()
    corrected_body_words = corrected_body.split()

    # Counting the differences in the subject
    subject_corrections = sum(1 for orig, corr in zip(original_subject_words, corrected_subject_words) if orig != corr)

    # Counting the differences in the body
    body_corrections = sum(1 for orig, corr in zip(original_body_words, corrected_body_words) if orig != corr)

    # Total corrections
    total_corrections = subject_corrections + body_corrections

    return total_corrections










######################## OLD CODE ########################


# Writes a email based on a draft
# def gpt_langchain_redaction(subject, input_data, parameters):
# OLD USE LANGCHAIN BUT DOES NOT WORK CORRECTLY
'''
def gpt_langchain_redaction(input_data, length, formality):
    # if (subject!=None):
    template = (
        """Given the following draft:

            {input}

            Please follow these instructions carefully:
            1. Write a subject for the email based on the draft in French.
            2. Write an email in French that matches the length and content of the input. The email should be very short, informal, and should strictly contain only the information present in the input. Do not add any new details or information.

            ---

            Subject:
            [Model's drafted subject]

            Draft:
            [Model's drafted email]
        """
    )
    #length = 'really short'
    #formality = 'formal'
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])
    # get a chat completion from the formatted messages
    chat = ChatOpenAI(temperature=0,openai_api_key=openai.api_key,openai_organization=openai.organization)
    text = chat(chat_prompt.format_prompt(input=input_data,length=length,formality=formality).to_messages())

    clear_text = text.content.strip()
    print('clear_text: ',clear_text)
    # if subject==None:
    # Extracting Subject
    subject_start = clear_text.index("Subject:") + len("Subject:")
    subject_end = clear_text[subject_start:].index("\n\n") if "\n\n" in clear_text[subject_start:] else len(clear_text)
    subject_list = clear_text[subject_start:subject_start+subject_end].strip().split("\n")
    subject_text = "\n".join(subject_list)
    # Extracting Email
    mail_start = clear_text.index("Draft:") + len("Draft:")
    # mail_end = clear_text[mail_start:].index("\n\n") if "\n\n" in clear_text[mail_start:] else len(clear_text)
    mail_list = clear_text[mail_start:len(clear_text)].strip().split("\n")
    mail_text = "\n".join(mail_list)
    # else:
    #     subject_text=subject
    #     mail_text=clear_text
    # return clear_text
    return subject_text, mail_text'''