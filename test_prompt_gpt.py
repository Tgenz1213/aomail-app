
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

main_list, cc_list, bcc_list = extract_contacts_recipients(query)

if not main_list:
    print(f"{Fore.RED}Invalid input or query not about email recipients")
else:
    pass













contacts_dict = {
    'Liam Turner': 'liam.turner@example.com',
    'Olivia Nelson': 'olivia.nelson@gmail.com',
    'Noah Taylor': 'noah.taylor@example.com',
    'Emma Davis': 'emma.davis@gmail.com',
    'Isabella Carter': 'isabella.carter@example.com',
    'Sophia Ward': 'sophia.ward@gmail.com',
    'Jackson Fisher': 'jackson.fisher@example.com',
    'Aiden Parker': 'aiden.parker@gmail.com',
    'Lucas Howard': 'lucas.howard@example.com',
    'Madison Mitchell': 'madison.mitchell@gmail.com',
    'Elijah Adams': 'elijah.adams@example.com',
    'Grace Taylor': 'grace.taylor@gmail.com',
    'Avery Foster': 'avery.foster@example.com',
    'Carter Cook': 'carter.cook@gmail.com',
    'Scarlett Turner': 'scarlett.turner@example.com',
    'Chloe Davis': 'chloe.davis@gmail.com',
    'Lily Carter': 'lily.carter@example.com',
    'Landon Ward': 'landon.ward@gmail.com',
    'Ethan Howard': 'ethan.howard@example.com',
    'Zoey Nelson': 'zoey.nelson@gmail.com',
    'Mia Fisher': 'mia.fisher@example.com',
    'Harper Parker': 'harper.parker@example.com',
    'Evelyn Mitchell': 'evelyn.mitchell@gmail.com',
    'Lincoln Taylor': 'lincoln.taylor@example.com',
    'Nora Foster': 'nora.foster@example.com',
    'Caleb Cook': 'caleb.cook@gmail.com',
    'Aria Turner': 'aria.turner@example.com',
    'Ella Davis': 'ella.davis@example.com',
    'Amelia Carter': 'amelia.carter@example.com',
    'Benjamin Ward': 'benjamin.ward@gmail.com',
    'Aubrey Howard': 'aubrey.howard@example.com',
    'Hudson Nelson': 'hudson.nelson@example.com',
    'Grayson Taylor': 'grayson.taylor@gmail.com',
    'Lillian Foster': 'lillian.foster@example.com',
    'Matthew Cook': 'matthew.cook@gmail.com',
    'Addison Turner': 'addison.turner@example.com',
    'David Davis': 'david.davis@example.com',
    'Zoe Carter': 'zoe.carter@gmail.com',
    'Penelope Ward': 'penelope.ward@example.com',
    'Hazel Howard': 'hazel.howard@gmail.com',
    'Mila Mitchell': 'mila.mitchell@example.com',
    'Gabriel Taylor': 'gabriel.taylor@example.com',
    'Sofia Foster': 'sofia.foster@gmail.com',
    'Harley Cook': 'harley.cook@example.com',
    'Joseph Turner': 'joseph.turner@example.com',
    'Aaliyah Davis': 'aaliyah.davis@example.com',
    'Eli Ward': 'eli.ward@example.com',
    'Paisley Nelson': 'paisley.nelson@gmail.com',
    'Brooklyn Taylor': 'brooklyn.taylor@example.com',
    'James Mitchell': 'james.mitchell@example.com',
    'Emma Foster': 'emma.foster@gmail.com',
    'Zachary Cook': 'zachary.cook@example.com',
    'Penelope Turner': 'penelope.turner@gmail.com',
    'Lucy Davis': 'lucy.davis@example.com',
    'Oliver Carter': 'oliver.carter@example.com',
    'Mackenzie Ward': 'mackenzie.ward@example.com',
    'William Howard': 'william.howard@gmail.com',
    'Stella Nelson': 'stella.nelson@example.com',
    'Axel Taylor': 'axel.taylor@example.com',
    'Kylie Foster': 'kylie.foster@example.com',
    'Michael Cook': 'michael.cook@gmail.com',
    'Audrey Turner': 'audrey.turner@example.com',
    'Samuel Davis': 'samuel.davis@example.com',
    'Leah Carter': 'leah.carter@example.com',
    'Nathan Ward': 'nathan.ward@example.com',
    'Aria Howard': 'aria.howard@example.com',
    'Harrison Nelson': 'harrison.nelson@gmail.com',
    'Sophie Taylor': 'sophie.taylor@example.com',
    'Daniel Foster': 'daniel.foster@gmail.com',
    'Ellie Cook': 'ellie.cook@example.com',
    'Grayson Turner': 'grayson.turner@gmail.com',
    'Anna Davis': 'anna.davis@example.com',
    'Nolan Carter': 'nolan.carter@gmail.com',
    'Avery Ward': 'avery.ward@example.com',
    'Sophia Howard': 'sophia.howard@example.com',
    'Levi Nelson': 'levi.nelson@example.com',
    'Mia Taylor': 'mia.taylor@gmail.com',
    'Matthew Foster': 'matthew.foster@example.com',
    'Ella Cook': 'ella.cook@gmail.com',
    'Caleb Turner': 'caleb.turner@example.com',
    'Gianna Davis': 'gianna.davis@example.com',
    'Andrew Carter': 'andrew.carter@gmail.com',
    'Zoe Ward': 'zoe.ward@example.com',
    'Logan Howard': 'logan.howard@gmail.com',
    'Piper Nelson': 'piper.nelson@example.com',
    'Jack Taylor': 'jack.taylor@example.com',
    'Lily Foster': 'lily.foster@example.com',
    'Owen Cook': 'owen.cook@example.com',
    'Sophia Turner': 'sophia.turner@gmail.com',
    'Ethan Davis': 'ethan.davis@example.com',
    'Addison Carter': 'addison.carter@gmail.com',
    'Aiden Ward': 'aiden.ward@example.com',
    'Aria Howard': 'aria.howard@example.com',
    'Hudson Nelson': 'hudson.nelson@example.com',
    'Scarlett Taylor': 'scarlett.taylor@gmail.com',
    'Chase Foster': 'chase.foster@example.com',
    'Natalie Cook': 'natalie.cook@example.com',
    'Wyatt Turner': 'wyatt.turner@gmail.com',
    'Aurora Davis': 'aurora.davis@example.com',
    'Oliver Carter': 'oliver.carter@gmail.com',
    'Luna Ward': 'luna.ward@example.com',
    'Isaac Howard': 'isaac.howard@example.com',
    'Violet Nelson': 'violet.nelson@gmail.com',
    'Ezra Taylor': 'ezra.taylor@example.com',
    'Madison Foster': 'madison.foster@gmail.com',
    'Aiden Cook': 'aiden.cook@example.com',
    'Zoe Turner': 'zoe.turner@gmail.com',
    'Leo Davis': 'leo.davis@example.com',
    'Stella Carter': 'stella.carter@example.com',
    'Levi Ward': 'levi.ward@gmail.com',
}


def find_emails(input_str, contacts_dict):
    # Split input_str into substrings if it contains spaces
    input_substrings = input_str.split() if ' ' in input_str else [input_str]

    # Convert input substrings to lowercase for case-insensitive matching
    input_substrings_lower = [sub_str.lower() for sub_str in input_substrings]

    # List comprehension to find matching emails
    matching_emails = [
        email
        for name, email in contacts_dict.items()
        if all(sub_str in name.lower() for sub_str in input_substrings_lower)
    ]

    # Return the list of matching emails
    return matching_emails


def find_emails_for_recipients(recipient_list, contacts_dict) -> dict:
    """Find matching emails for a list of recipients."""
    recipients_with_emails = []

    # Iterate through recipient_list to find matches
    for recipient_name in recipient_list:
        matching_emails = find_emails(recipient_name, contacts_dict)

        # Append the result as a dictionary
        recipients_with_emails.append({'name': recipient_name, 'email': matching_emails})

    # Print the result using Fore for color
    print(f"{Fore.YELLOW}Matching emails for '{', '.join(recipient_list)}':")
    for recipient in recipients_with_emails:
        print(f"{Fore.GREEN}{recipient['name']}:{Fore.RESET} {recipient['email']}")

    # Return the list of matching emails
    return recipients_with_emails

# Find matching emails for each list of recipients
main_recipients_with_emails = find_emails_for_recipients(main_list, contacts_dict)
cc_recipients_with_emails = find_emails_for_recipients(cc_list, contacts_dict)
bcc_recipients_with_emails = find_emails_for_recipients(bcc_list, contacts_dict)