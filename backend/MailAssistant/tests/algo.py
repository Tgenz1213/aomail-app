email_prompt = """
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


import json
import anthropic
from langchain.memory import ChatMessageHistory
from colorama import Fore, init
import re

######################## Claude 3 API SETTINGS ########################
init(autoreset=True)


HUMAN = "Human: "
ASSISTANT = "Assistant:"


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


def summarize_conversation(body: str, language: str = "French") -> dict:
    """Summarizes an email conversation in the specified language."""

    template = f"""{HUMAN}As a smart email assistant, 
    For each email in the following conversation, summarize it in {language} as a list of up to 3 ultra concise keypoints (up to 7 words) that encapsulate the core informations. This will aid the user in recalling the past conversation.
    Increment the number of keys to match the number of emails. The number of keys must STRICTLY correspond to the number of emails.
    The sentence must be highly relevant and not deal with details or unnecessary information. If you hesitate, do not add the keypoint.
    
    Email conversation:
    {body}
    
    ---
    Answer must always be a Json format matching this template:
    {{
        "1": [list of keypoints],
        "2": [list of keypoints],
        "n": [list of keypoints]
    }}
    {ASSISTANT}"""
    response = get_prompt_response(template)
    clear_response = response.content[0].text.strip()
    result_json = json.loads(clear_response)

    print(f"{Fore.GREEN}{result_json}")

    return result_json



email_prompt = re.sub(r"<http(.*?)>", "", email_prompt)
email_prompt = re.sub(r"http(.*?)\ ", "", email_prompt)


summarize_conversation(email_prompt)


# import torch
# from llmlingua import PromptCompressor

# # Check if GPU is available
# if torch.cuda.is_available():
#     device_map = "cuda"
#     gpu_info = torch.cuda.get_device_properties(0)
#     print(f"GPU Name: {gpu_info.name}")
#     print(f"GPU Memory: {gpu_info.total_memory} bytes")
#     print(f"GPU Compute Capability: {gpu_info.major}.{gpu_info.minor}")
# else:
#     device_map = "cpu"
#     print("No GPU detected. Using CPU.")


# # Initialize the PromptCompressor with the specified device
# llm_lingua = PromptCompressor(
#     model_name="microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank",
#     use_llmlingua2=True,
#     device_map=device_map,
# )
# # Compress the email prompt
# compressed_prompt = llm_lingua.compress_prompt(
#     email_prompt,
#     target_token=500,
#     instruction="Compress this email conversation in order to help a LLM to recognize the different emails that the conversation contains",
# )

# # Print the compressed prompt
# print("Compressed Email Prompt:")
# print(compressed_prompt["compressed_prompt"])
