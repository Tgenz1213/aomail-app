"""
TODO: implement integration with Search

TEST FILE TO IMPLEMENT A GRPAH TO SEARCH DATA about a user question
"""

import json
import os
import re
import threading


def preprocess_email(email_content: str) -> str:
    """Removes links from the email content and strips text of unnecessary spacings"""
    # Remove links enclosed in <http...> or http... followed by a space
    email_content = re.sub(r"<http(.*?)>", "", email_content)
    email_content = re.sub(r"http(.*?)\ ", "", email_content)
    email_content = re.sub(r"http\S+", "", email_content)

    # rmv email addresses
    email_content = re.sub(r"<mailto:(.*?)>", "", email_content)
    email_content = re.sub(r"mailto:(.*?)\ ", "", email_content)
    # Remove email addresses containing "@"
    email_content = re.sub(
        r"<\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b>", "", email_content
    )
    email_content = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "", email_content
    )

    # Delete patterns like "[image: ...]"
    email_content = re.sub(r"\[image:[^\]]+\]", "", email_content)
    # Convert Windows line endings to Unix line endings
    email_content = email_content.replace("\r\n", "\n")
    # Remove spaces at the start and end of each line
    email_content = "\n".join(line.strip() for line in email_content.split("\n"))
    # Delete multiple spaces
    email_content = re.sub(r" +", " ", email_content)
    # Reduce multiple consecutive newlines to two newlines
    email_content = re.sub(r"\n{3,}", "\n\n", email_content)

    return email_content.strip()


# Sample data structure as described
data = {
    "Sport": {
        "organizations": {
            "Angers Métropole Cyclisme": {
                "topics": {
                    "New season": {
                        "keypoints": [
                            "commence 01/09/2024",
                            "quentin revient en France",
                        ],
                        "emails": ["id_email23", "id_email4"],
                    }
                }
            }
        }
    },
    "Études": {
        "organizations": {
            "ESAIP": {
                "topics": {
                    "Semestre 4": {
                        "keypoints": [
                            "fin vers mi juin",
                            "erasmus",
                            "évaluer le dortoir",
                        ],
                        "emails": ["id_email1", "id_email2"],
                    }
                }
            }
        }
    },
}


import json
import anthropic
from colorama import Fore, init

######################## Claude 3 API SETTINGS ########################
init(autoreset=True)


######################## TEXT PROCESSING UTILITIES ########################
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


class Search:
    """
    Class for searching through categorized email data within a knowledge tree.

    Example of a knowledge tree of a user:
    {
        "Studies": {
            "organizations": {
                "ESAIP": {
                    "topics": {
                        "Semester 4": {
                            "keypoints": [
                                "ends around mid-June",
                                "erasmus",
                                "evaluate the dormitory"
                            ],
                            "emails": ["id_email1", "id_email2"]
                        }
                    }
                }
            }
        }
    }
    """

    def __init__(
        self, user_id: int, question: str = None, knowledge_tree: dict = None
    ) -> None:
        self.user_id = user_id

        # TODO: change the path when we will move this file
        self.file_path = f"backend/MailAssistant/tests/{user_id}.json"

        self.question = question
        if knowledge_tree:
            self.knowledge_tree = knowledge_tree
            threading.Thread(target=self.save_user_data, args=(knowledge_tree,)).start()
        elif not os.path.exists(self.file_path):
            self.knowledge_tree = {}
        else:
            self.knowledge_tree = self.load_user_data()
        self.categories = self.get_categories()

    def get_categories(self) -> dict[str, list[str]]:
        """
        Extracts and returns categories and their associated organizations from the knowledge tree.
        """
        if not self.knowledge_tree:
            return []

        categories = {}
        for category in self.knowledge_tree:
            categories[category] = [
                organization
                for organization in self.knowledge_tree[category]["organizations"]
            ]
        return categories

    def get_keypoints(self, selected_categories: dict[str, list[str]]) -> dict:
        """
        Retrieves keypoints for the selected categories and organizations.
        """
        if not self.knowledge_tree:
            return []

        keypoints = {}
        for category in selected_categories:
            keypoints[category] = {}
            for organization in selected_categories[category]:
                keypoints[category][organization] = {}
                for topic in self.knowledge_tree[category]["organizations"][
                    organization
                ]["topics"]:
                    keypoints[category][organization][topic] = {}
                    keypoints[category][organization][topic]["keypoints"] = [
                        keypoint
                        for keypoint in self.knowledge_tree[category]["organizations"][
                            organization
                        ]["topics"][topic]["keypoints"]
                    ]

        return keypoints

    def get_selected_categories(self) -> dict[str : list[str]]:
        """
        Returns the highly relevant categories and organizations to answer the user's question.

        Returns:
            dict: A dictionary mapping highly relevant category names to their corresponding organizations.
        """
        template = f"""You are an email assistant that helps a user to answer its question.
        
        Email categories and organizations:
        {self.categories}

        User question:
        {self.question}
        
        Choose categories and organizations that have high probability to help the user to find its answer.
        The chosen categories and organizations must be highly relevant. If you hesitate do not add it.
        Do not add any comments nor explain your thinking process.

        ---
        Answer must always be a Json format matching this template:
        {{
            "category1": [selected organizations],
            ...
            "categoryN": [selected organizations]
        }}
        """
        response = get_prompt_response(template)
        clear_response = response.content[0].text.strip()
        result_json = json.loads(clear_response)

        return result_json

    def get_answer(self, keypoints: dict, language: str = "French") -> dict:
        """
        Generates an answer based on the keypoints and checks if further details are needed.
        """
        template = f"""You are an email assistant that helps a user to answer their question.

        User data:
        {keypoints}

        User question:
        {self.question}
        
        If you estimate that the answer is likely to be good, set the boolean field to 'true'.
        Otherwise, set it to 'false' if you think the user is very likely to look for further details.
        The answer must be concise and straight to the point without giving explanations.

        ---
        The answer must always be in Json format matching this template:
        {{
            "sure": bool,
            "answer": "answer to the user question in {language}"
        }}
        """
        response = get_prompt_response(template)
        clear_response = response.content[0].text.strip()
        result_json = json.loads(clear_response)

        return result_json

    def summarize_conversation(
        self, body: str, email_id: str, language: str = "French"
    ) -> dict[str:list]:
        """Summarizes an email conversation in the specified language with keypoints."""

        template = f"""As a smart email assistant, 
        For each email in the following conversation, summarize it in {language} as a list of up to three ultra-concise keypoints (up to seven words) that encapsulate the core information. This will aid the user in recalling the past conversation.
        Increment the number of keys to match the number of emails. The number of keys must STRICTLY correspond to the number of emails.
        The sentence must be highly relevant and not deal with details or unnecessary information. If you hesitate, do not add the keypoint.
        In {language}: Add a 'category' (one word), an 'organization', and a 'topic' that best describes the conversation.
        To assist you in categorizing the conversation, here are the existing categories and organizations: {self.get_categories()}.
        If you can classify the conversation in an existing category/organization: Do it. If you hesitate, create another category/organization in {language}.

        Email conversation:
        {body}
        
        ---
        Answer must always be a Json format matching this template:
        {{
            "category": "",
            "organization": "",
            "topic": "",
            "keypoints": {{        
                "1": [list of keypoints],
                "2": [list of keypoints],
                "n": [list of keypoints]
            }}
        }}
        """
        response = get_prompt_response(template)
        clear_response = response.content[0].text.strip()
        result_json = json.loads(clear_response)

        print(f"{Fore.GREEN}summarize_conversation result:{result_json}")

        category = result_json["category"]
        organization = result_json["organization"]
        topic = result_json["topic"]
        keypoints = result_json["keypoints"]

        user_keypoints = [
            keypoint for index in keypoints for keypoint in keypoints[index]
        ]
        self.add_user_data(category, organization, topic, user_keypoints, [email_id])

        return keypoints

    def summarize_email(
        self, body: str, email_id: str, language: str = "French"
    ) -> dict[str:list]:
        """Summarizes an email conversation in the specified language with keypoints."""

        template = f"""As a smart email assistant, 
        Summarize the email body in {language} as a list of up to three ultra-concise keypoints (up to seven words each) that encapsulate the core information. This will aid the user in recalling the content of the email.
        The sentences must be highly relevant and should not include minor details or unnecessary information. If in doubt, do not add the keypoint.
        In {language}: Add a 'category' (one word), an 'organization', and a 'topic' that best describe the conversation.
        To assist you in categorizing the email, here are the existing categories and organizations: {self.get_categories()}.
        If you can classify the email within an existing category/organization, do so. If uncertain, create another category/organization in {language}.

        Email body:
        {body}
        
        ---
        Answer must always be a Json format matching this template:
        {{
            "category": "",
            "organization": "",
            "topic": "",
            "keypoints": [list of keypoints]
        }}
        """
        response = get_prompt_response(template)
        clear_response = response.content[0].text.strip()
        result_json = json.loads(clear_response)

        print(f"{Fore.GREEN}summarize_email result:{result_json}")

        category = result_json["category"]
        organization = result_json["organization"]
        topic = result_json["topic"]
        keypoints = result_json["keypoints"]

        self.add_user_data(category, organization, topic, keypoints, [email_id])

        return keypoints

    def save_user_data(self, data: dict) -> None:
        """
        Saves updated user data to a JSON file.
        """
        with open(self.file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print("Data saved to JSON file successfully.")

    def load_user_data(self) -> dict:
        """
        Loads user data from a JSON file.
        """
        with open(self.file_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)

    def add_user_data(
        self,
        category: str,
        organization: str,
        topic: str,
        keypoints: list[str],
        emails: list[str],
    ) -> None:
        """
        Adds or updates user data for a specific topic within a structured dictionary.
        Ensures no duplication of keypoints or emails, maintaining case-insensitivity.

        Parameters:
            - category (str): Top-level classification.
            - organization (str): Sub-level classification under category.
            - topic (str): Specific topic under organization for data storage.
            - keypoints (list[str]): List of unique keypoints related to the topic.
            - emails (list[str]): List of unique emails associated with the topic.
        """
        if category not in self.knowledge_tree:
            self.knowledge_tree[category] = {}
            self.knowledge_tree[category]["organizations"] = {}
        if organization not in self.knowledge_tree[category]["organizations"]:
            self.knowledge_tree[category]["organizations"][organization] = {}
            self.knowledge_tree[category]["organizations"][organization]["topics"] = {}
        if (
            topic
            not in self.knowledge_tree[category]["organizations"][organization][
                "topics"
            ]
        ):
            self.knowledge_tree[category]["organizations"][organization]["topics"][
                topic
            ] = {}
            self.knowledge_tree[category]["organizations"][organization]["topics"][
                topic
            ]["keypoints"] = keypoints
            self.knowledge_tree[category]["organizations"][organization]["topics"][
                topic
            ]["emails"] = emails
        else:
            prev_keypoints: list = self.knowledge_tree[category]["organizations"][
                organization
            ]["topics"][topic]["keypoints"]

            for keypoint in keypoints:
                if keypoint.lower() not in map(str.lower, prev_keypoints):
                    prev_keypoints.append(keypoint)

            self.knowledge_tree[category]["organizations"][organization]["topics"][
                topic
            ]["keypoints"] = prev_keypoints

            prev_emails: list = self.knowledge_tree[category]["organizations"][
                organization
            ]["topics"][topic]["emails"]

            for email in emails:
                if email.lower() not in prev_emails:
                    prev_emails.append(email)

            self.knowledge_tree[category]["organizations"][organization]["topics"][
                topic
            ]["emails"] = prev_emails

        self.save_user_data(self.knowledge_tree)


# THIS CODE IS TO TEST AO ANSWER WITH TREE KNOWLEDGE
"""Step 1: Prompt with categories and organizations and user query
   Step 2: Prompt with topics and details
   Step 3: Display answer to user
"""
question = "When does the cycling season start?"
# TODO: get real user id
user_id = 1
# data = {} # remove this line to test with Augustin data
search = Search(user_id, question, data)
selected_categories = search.get_selected_categories()
keypoints = search.get_keypoints(selected_categories)

if not selected_categories or not keypoints:
    print("You do not have enough data to answer the question")
else:
    answer = search.get_answer(keypoints)

    if answer["sure"] == False:
        emails = []
        print(
            f"{Fore.YELLOW}Ao is not sure, here is the list of emails that will help you to verify its answer"
        )

        for category in keypoints:
            for organization in keypoints[category]:
                for topic in keypoints[category][organization]:
                    emails.extend(
                        search.knowledge_tree[category]["organizations"][organization][
                            "topics"
                        ][topic]["emails"]
                    )

        print(emails)
    answer = answer["answer"]
    print(f"The answer to the question is:\n{answer}")


# THIS CODE IS TO TEST SUMMARIZING A CONVERSATION AND SAVING IT IN THE JSON FILE
'''email_prompt = """
Bonjour Monsieur CROCHET,

Merci du compliment. Je vous suis très reconnaissant.
Je suis entrain de finir mon ERASMUS et de passer les derniers examens.

Je viens de trouvé un stage en tant qu'ingénieur backend dans une 
startup cet été.

Bonne vacances,

Augustin ROLET

On 12/22/2023 11:18 PM, CROCHET Moise wrote:
> Cher Augustin,
>
> Tu es toujours aussi perspicace, même en vacances. C'est une qualité.
>
> Prends le temps de te poser un peu et prépare ton séjour d'études à venir.
>
> A l'occasion, cela me ferait plaisir de faire un visio avec toi d'ici 
> quelques temps. Nous pourrons échanger tranquillement sur toutes les 
> questions qui te préoccupent.
>
> D'ici là, profite des fêtes de fin d'année pour te ressourcer en 
> famille. Vous avez besoin de repos en cette fin de semestre.
>
> A très bientôt.
> Bien à toi.
> Moïse
>
> Envoyé à partir de Outlook pour Android <https://aka.ms/AAb9ysg>
> ------------------------------------------------------------------------
> *From:* ROLET Augustin <arolet.ing2027@esaip.org>
> *Sent:* Friday, December 22, 2023 6:08:28 PM

> *To:* CROCHET Moise <mcrochet@esaip.org>
> *Subject:* Re: Alternance Cours
>
> Merci monsieur pour votre réponse,
>
> Je vais éviter d'être prolixe comme à mon habitude.
>
> Backend Engineer <https://careers.vinted.com/jobs/j/4198667101>
>
> Data Analyst <https://careers.vinted.com/jobs/j/4223185101>
>
> Lead Backend Engineer <https://careers.vinted.com/jobs/j/4217362101>
>
> _Question simple: Est ce que la plupart des étudiants (initiaux et 
> apprentis) ont le niveau pour prétendre à ce type de poste en sortie 
> d'école ? (A mon avis non car c'est ultra sélectif)_
>
> La technique prime sur ce type de poste (qui est mon objectif 
> principal et c'est pour ça que je me tue à la tâche tout les soirs). 
> C'est extrêmement dur d'être accepté chez Vinted. L'année dernière 
> j'ai "reverse engineered" leur API et eu accès à des données privées 
> (adresse, sexe) des utilisateurs (en autres). Je sais que d'ici 3 ans 
> (voir toute la vie), très peu auront le niveau. Il faut 3 ans d'xp 
> mini. Je ne suis pas contre être chef de projet un jour mais il faut 
> que je commence en bas et que je le mérite. Aucun ingénieur ne 
> commence chef de projet et ça me fait mal au cœur de voir certains 
> rêver qu'ils vont arriver et commander les autres alors qu'ils ont 0 xp.
>
> 1) Tout ça pour dire que le but c'est d'avoir un job (besoin vital) et 
> après on peut se concentrer sur d'autres choses. Je suis ultra 
> pragmatique. Les entreprises ne veulent pas de blabla, juste est ce 
> que tu sais faire ça ? et si Non est ce que tu sais faire un truc 
> similaire et tu apprendras vite ?
>
> 2) Est ce que tu sais parler anglais, oui ou non ?
>
> 3) Quels sont des défauts ?
>
> 4) Et un projet à faire
>
> C'est ça le process de recrutement en IR si je ne dis pas de bêtise 
> (je sais il y a aussi des tests de personnalité mais cela ne compense 
> pas la technique)
>
> Augustin
>
"""

# TODO: use library.preprocess_email() in production
email_content = preprocess_email(email_prompt)

user_id = 1
search = Search(user_id)
keypoints = search.summarize_conversation(email_content, "emailIDTest")
print(json.dumps(search.load_user_data(), indent=4, ensure_ascii=False))
'''

# THIS CODE IS TO TEST SUMMARIZING A SINGLE EMAIL AND SAVING IT IN THE JSON FILE
'''email_prompt = """
Bonjour à
tous,

J'espère
avant toute chose que vous allez tous bien.

Comme
évoqué avec certains d'entre vous, je souhaite faire un
dernier point rapide en visio pour savoir comment se déroule
la fin de votre expérience internationale. Ainsi,

vous
trouverez ci-dessous un lien vers un fichier Excel partagé
pour indiquer vos noms dans le créneau qui vous convient le
mieux :

Entretiens_ING2-EN_23-24_n°6_mai24.xlsx

Comme
habituellement, si les plages horaires ne coïncident pas
avec vos emplois du temps respectifs, je peux prévoir des
créneaux supplémentaires. Le cas échéant, n'hésitez pas à
revenir vers moi.

Une fois
vos créneaux réservés, je vous enverrai une invitation TEAMS
via vos comptes esaip à la date et horaire convenus.

Au
plaisir de vous revoir prochainement.

Bonne
fin de journée.

Cordialement.

MC

Moïse
CROCHET

Pilote
du cycle préparatoire - Enseignant-chercheur

02 41 96 65 51

Campus
Ouest

18,
rue du 8 mai 1945 - CS 80022 - 49180
St-Barthélemy d'Anjou Cedex
"""

# TODO: use library.preprocess_email() in production
email_content = preprocess_email(email_prompt)

user_id = 1
search = Search(user_id)
keypoints = search.summarize_email(email_content, "emailIDTest")
print(json.dumps(search.load_user_data(), indent=4, ensure_ascii=False))
'''
