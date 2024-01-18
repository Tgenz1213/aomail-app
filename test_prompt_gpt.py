
######################## GPT - 3.5 turbo API SETTINGS ########################
import json
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
    
    Analyze the following input : '{query}' to determine recipients for an email:
    If the input is not valid or unreadable: Return "INCORRECT"
    If no CC or no CCI are indicate, put everything in main_recipients


    Answer must be a Json format with three keys:
    main_recipients: [Python list],
    cc_recipients: [Python list],
    bcc_recipients: [Python list]
    """
    formatted_prompt = template.format(query=query)
    response = get_prompt_response(formatted_prompt)
    response_text = response.choices[0].message.content.strip()


    if response_text == "INCORRECT":
        return "INCORRECT", "INCORRECT", "INCORRECT"

    recipients = json.loads(response_text)


    # Extract information based on markers
    main_recipients = recipients.get('main_recipients', [])
    cc_recipients = recipients.get('cc_recipients', [])
    bcc_recipients = recipients.get('bcc_recipients', [])

    print("Extracted response from ChatGPT (main): %s" % main_recipients)
    print("Extracted response from ChatGPT (CC): %s" % cc_recipients)
    print("Extracted response from ChatGPT (BCC): %s" % bcc_recipients)

    return main_recipients, cc_recipients, bcc_recipients


query = "envoi un mail a marise et a theo en copie et Jea en copie cachée"

extract_contacts_recipients(query)
