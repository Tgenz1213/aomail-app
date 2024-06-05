"""
Template to summarize an email instead of bullet points
"""

import json
import anthropic


def get_prompt_response(formatted_prompt):
    """Returns the prompt response"""
    client = anthropic.Anthropic(
        api_key="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"
    )
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0.0,
        messages=[{"role": "user", "content": formatted_prompt}],
    )
    return response


def categorize_and_summarize_email(
    subject: str,
    decoded_data: str,
    category_dict: dict,
    user_description: str,
    sender: str,
    language: str = "French",
) -> tuple[str, str, str, dict[str:str, str:list], dict[str:int]]:
    """Categorizes and summarizes an email"""

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

    template = f"""You are a smart email assistant acting as if you were a secretary, summarizing an email for the recipient orally.
    
    Given the following email:

    Sender:
    {sender}

    Subject:
    {subject}

    Text:
    {decoded_data}

    User description:
    {user_description}

    Using the provided categories:

    Topic Categories:
    {category_dict}

    Response Categories:
    {response_list}

    Relevance Categories:
    {relevance_list}

    Complete the following tasks in {language}:
    - Categorize the email according to the user description (if provided) and given categories.
    - Summarize the email without adding any greetings.
    - If the email appears to be a response or a conversation, summarize only the last email and IGNORE the previous ones.
    - The summary should objectively reflect the most important information of the email without making subjective judgments.
    - If the email is explicitely mentionning the name of the user (provided with user description), then use 'You' instead of the name of the user.
    
    ---
    Answer must always be a Json format matching this template:
    {{
        "topic": Topic Title Category,
        "response": Response Category,
        "relevance": Relevance Category,
        "summary": Summary of the email
    }}"""
    response = get_prompt_response(template)
    clear_response = response.content[0].text.strip()

    print("Claude")
    print(clear_response)

    result_json = json.loads(clear_response)

    topic_category = result_json["topic"]
    response_category = result_json["response"]
    relevance_category = result_json["relevance"]
    summary = result_json["summary"]

    return (
        topic_category,
        response_category,
        summary,
        relevance_category,
    )


decoded_data = """
Bonjour à toutes et à tous,

Dans le cadre de la préparation de votre Séjour d'études LV1
de l'année prochaine et afin de valoriser votre fidélité à
l'ESAIP, nous vous transmettons dès maintenant le Powerpoint
de présentation des destinations possibles pour votre séjour à
l'étranger en troisième année. Il s'agit d'une présentation
informative, mais contractuelle.

Nous vous invitons à regarder les sites des écoles partenaires
(indiquer le nom sur votre moteur de recherche) et notamment
le programme Bachelor de votre filière (IR ou GRE).

Si vous souhaitez « réserver » votre place pour l'une des
écoles, vous avez
jusqu'au
21/06/24

pour nous communiquer votre souhait par retour de mail.

Dans ce cas, nous vous inscrirons dès maintenant (sous réserve
d'un niveau d'anglais suffisant pour intégrer l'université
partenaire, B1 ou B2 selon les écoles).

Attention : toute inscription sera
définitive et sans possibilité de changement en septembre.

Nous vous offrons cette opportunité car chaque destination
a un nombre limité de places.

Si vous souhaitez attendre le mois de septembre pour faire vos
choix, vous n'avez pas besoin de répondre à cet e-mail.

Vous en souhaitant une bonne réception.

Cordialement,

Manon GUINEBRETIERE

Assistante des relations
internationales

Campus Ouest

02 41 96 65 13

Campus
Ouest

18,
rue du 8 mai 1945 - CS 80022 - 49180 St-Barthélemy
d'Anjou Cedex
"""
sender = "GUINEBRETIERE Manon <mguinebretiere@esaip.org>"
subject = "Préparation Séjour d'études ING3"
category_dict = {
    "Exceptionnels": "Mails rares et important parlant de business, livraison, propositions d'activités.",
    "ESAIP": "Le pilote s'appelle Moïse CROCHET. Mets TOUT les mails de notifications Teams en Inutile ainsi que les convocations de soutenances.",
    "Alternance": "Mail reliés à mon inscription pour l'année prochaine ainsi que les démarches administratives associées.",
    "Jobs": "Tout les mails reliés à Cognitive Design Systems (CDS) et Aomail, AlphaPen, SeedLab",
}
user_description = "Augustin ROLET est un étudiant en école d'ingénieurs spécialisée dans l'informatique et la cybersécurité"

categorize_and_summarize_email(
    subject, decoded_data, category_dict, user_description, sender
)
