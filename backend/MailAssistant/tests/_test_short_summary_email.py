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
    - If the email explicitly mentions the name of the user (provided with user description), then use 'You' instead of the name of the user.
    - Provide a short sentence (up to 10 words) summarizing the core content of the email.
    - Define the importance level of the email with one keyword: "important", "informative" or "useless".
    - If the email appears to be a response or a conversation, summarize only the last email and IGNORE the previous ones.
    - The summary should objectively reflect the most important information of the email without making subjective judgments.    
    
    ---
    Answer must always be a JSON format matching this template:
    {{
        "topic": Selected Category,
        "response": Response Category,
        "relevance": Relevance Category,
        "importance": Importance of the email,
        "flags": {{
            "spam": bool,
            "scam": bool,
            "newsletter": bool,
            "notification": bool,
            "meeting": bool
        }},
        "summary": {{
            "one_line": One sentence summary,
            "short": Short summary of the email
        }}
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
Subject:
RE: Aide cessation micro entreprise
From:
Raphael PAILLE <raphael.paille@greffe-tc-angers.fr>
Date:
6/17/2024, 10:34 AM
To:
Augustin ROLET <augustin.rolet.pro@gmail.com>

Monsieur,

 

Je vous invite à vous rapprocher de votre expert-comptable ou conseiller habituel pour procéder à la radiation de l’activité via le guichet unique.

 

Respectueusement,

 

Raphaël Paillé

Greffier associé

 

 

 

De : Augustin ROLET <augustin.rolet.pro@gmail.com>
Envoyé : samedi 15 juin 2024 16:44
À : Raphael PAILLE <raphael.paille@greffe-tc-angers.fr>
Objet : Aide cessation micro entreprise

 

Bonjour Monsieur,

Je me permet de vous contacter suite à 3 refus pour un motif inconnu. J'ai contacté cette addresse e-mail: <bertrand.paille@greffe-tc.net> sans réponse le 1 avril 2024.

Je souhaite simplement cesser mon activité, cela fait plusieurs mois que j'ai arrêté mais je n'ai pas pu finaliser la démarche.

SIRET: 921517397

J'ai déjà tenté depuis le guichet unique mais je suis refusé pour le motif: Pièce invalide, manquante ou incomplète

Je suis actuellement en Lituanie jusqu'à fin juin, j'ai tenté avec mon passeport, ma signature, une mention d'attestation sur l'honneur ainsi que la date du jour: sans succès

 

De plus, j'ai payé une facture: "Décision de refus d'inscription" et souhaite juste fermer ma micro entreprise rien de plus.

Merci de votre réponse et de votre aide,

Augustin ROLET


"""
sender = "raphael.paille@greffe-tc-angers.fr"
subject = "Re: Les grandes vacances s'approchent"
category_dict = {
    "Exceptionnels": "Mails rares et important parlant de business, livraison, propositions d'activités.",
    "ESAIP": "Le pilote s'appelle Moïse CROCHET. Mets TOUT les mails de notifications Teams en Inutile ainsi que les convocations de soutenances.",
    "Alternance": "Mail reliés à mon inscription pour l'année prochaine ainsi que les démarches administratives associées.",
    "Jobs": "Tout les mails reliés à Cognitive Design Systems (CDS) et Aomail, AlphaPen, SeedLab",
    "Others": "All emails that can not be classify in any of the given categories",
}
user_description = "Augustin ROLET est un étudiant en école d'ingénieurs spécialisée dans l'informatique et la cybersécurité"

categorize_and_summarize_email(
    subject, decoded_data, category_dict, user_description, sender
)
