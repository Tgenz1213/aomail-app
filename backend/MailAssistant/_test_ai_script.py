from colorama import Fore, init
import time
import statistics
import gpt_3_5_turbo, claude, mistral


######################## CONSTANTS ########################
# TODO: add gpt_4
# TODO: add role as a parameter in get_prompt_response for testing by role
# TODO: generate a pdf file

# TODO: add a counter per ia in the try except to check the success rate
# TODO: store errors for debugging
LIST_AI_PROVIDERS = [gpt_3_5_turbo, claude, mistral]
LIST_FUNCTIONS = ["new_mail_recommendation", "correct_mail_language_mistakes"]

# Créer une liste combinée des fournisseurs AI et des fonctions
COMBINED_LIST = [
    (provider, function)
    for provider in LIST_AI_PROVIDERS
    for function in LIST_FUNCTIONS
]

# Initialiser le dictionnaire pour stocker les statistiques
ai_providers_stats = {
    provider.__name__: {function: [] for _, function in COMBINED_LIST}
    for provider, _ in COMBINED_LIST
}

# ----------------------- new_mail_recommendation EXAMPLES -----------------------#
examples_new_mail_recommendation = [
    (
        "<p>Hello, can I ask a question about Graph API implementation inside an app here?</p>",
        "",
        "Mail formel et long",
    ),
    (
        "<p>bjr Msr DUPONT, je vous souahite une bonne année. Je c que l'algebre ct dure et je nai ps compris grand chse mais g fé de mon miux. Bonne continuatioN. G plein de projet et rencontré d personne fantastiques. Ctt année va etre incroyable, je sui mega focus et j'apprend bcp de ttrucs en info. Augustin <i>Software engineer student</i></p>",
        "Maths - bilan des 2 dernières ans",
        "Mail très formel, froid et clair et concis",
    ),
    (
        "<p>Salut <strong>papi</strong> cv ? nous on séclate en Espagne!!! on ador la piscine. Claude et la fam</p>",
        "NEws des vacs",
        "Mail informel, court et enjoué",
    ),
    (
        "<p>slt cv jsp koi dir. si tu voi ca c que test a march ✌️😊</p>",
        "msg de test ala tem",
        "Mail totalement informel et ultra court",
    ),
    (
        "<p>je crois que g trouvé quelquechose de pas mal en <strong>prompt engineering</strong>. jesp que cv de votr cote. un peu de taf en back en front et on pourra push en prod</p>",
        "proje - on av bien et vite",
        "Mail court, pro et efficace",
    ),
    (
        "<p>Je vais sans doute vous rejoindre l'année prochaine car je ne suis qu'en ING2 pour l'instant. Et ce semestre est vraiment compliqué, il me reste une seule semaine et après je reviens vers Théo sur Mail Assistant et je me réattaque au pb de licence M365</p>",
        "Salut Jean, ça se passe bien ton alternance?",
        "Mail formel et professionnel",
    ),
    (
        "<p>bsr madama. Je suis en 2eme année de cyle prépa. Est ce ke je peux av la lsit des entreprises ds lesquell les eleves en IR3, 4, 5 on fait soit 1 stage soi une alternance. Merc de votre retour. Augustin ROLET</p>",
        "Stages & Alter",
        "Email de haute qualité, irréprochable et d'un niveau de langue présidentiel",
    ),
]

# ----------------------- new_correct_mail_language_mistakes EXAMPLES -----------------------#
examples_correct_mail_language_mistakes = [
    ("Salut, cmt ça va?", "Juste pr prendre de tes nouvelles, cmt ça va?"),
    ("Lol, tu là?", "Hey, lol, tu là?"),
    ("A tooute à l'h", "A laproch  on se voit plus tard!"),
    ("peti test appl", "c un  emai de test envoyer depus l'appl"),
    ("Hey! Quoi de neuf?", "Hey! Quoi de neuf? Pas de news de toî depuis un moment."),
    ("Attend ta réponse", "Toujours en atente de ta réponse o dernier mail."),
    ("Merci", "Merci pr l'info, c'est simpà!"),
    ("Coucou", "Coucou, t'as une minute? Besoin dton avis sur kke chose."),
    (
        "Discus proj entrprena",
        "Bonjour, j'espère que tu va bi1. Je voula discuter avec toi du proj",
    ),
]





# Dictionnaire pour stocker les résultats
results = {}

# Parcourir les exemples
for example in (
    examples_new_mail_recommendation + examples_correct_mail_language_mistakes
):
    # Déterminer le nombre d'éléments par tuple
    num_elements = len(example)

    # Assigner les éléments du tuple
    if num_elements == 3:
        mail_content, email_subject, user_recommendation = example
    elif num_elements == 2:
        mail_content, email_subject = example
    else:
        continue

    # Parcourir les fournisseurs AI
    for ai_provider in LIST_AI_PROVIDERS:
        # Parcourir les fonctions AI
        for function in LIST_FUNCTIONS:
            start_time = time.time()
            try:
                # Appeler la fonction AI correspondante
                if num_elements == 3:
                    result = getattr(ai_provider, function)(
                        mail_content, email_subject, user_recommendation
                    )
                elif num_elements == 2:
                    result = getattr(ai_provider, function)(mail_content, email_subject)

            except:
                pass
            elapsed_time = time.time() - start_time

            # Stocker les résultats
            results[(mail_content, email_subject, ai_provider.__name__, function)] = {
                "result": result,
                "elapsed_time": elapsed_time,
                "ai_provider": ai_provider.__name__,
                "function_name": function,
                "example": example,
            }
            ai_providers_stats[ai_provider.__name__][function].append(elapsed_time)

            # Afficher les résultats
            print(f"AI Provider: {ai_provider.__name__}, Function: {function}")
            print(f"{Fore.LIGHTBLUE_EX}{result}")
            print(f"Elapsed Time: {elapsed_time} seconds\n")

# Extraire les temps écoulés pour tous les prompts
all_elapsed_times = [result["elapsed_time"] for result in results.values()]

# Afficher les statistiques générales
min_time = round(min(all_elapsed_times), 2)
max_time = round(max(all_elapsed_times), 2)
print(f"Min Time: {min_time} seconds")
print(f"Max Time: {max_time} seconds")

avg_time_all_prompts = round(statistics.mean(all_elapsed_times), 2)
print(f"Avg Time for All Prompts: {avg_time_all_prompts} seconds")

std_dev_all_prompts = round(statistics.stdev(all_elapsed_times), 2)
print(f"Standard Deviation for All Prompts: {std_dev_all_prompts} seconds")

# Afficher les statistiques pour chaque fournisseur AI et fonction
for provider, functions in ai_providers_stats.items():
    print(f"\nAI Provider: {provider}")
    for function, elapsed_times in functions.items():
        min_time_function = round(min(elapsed_times), 2)
        max_time_function = round(max(elapsed_times), 2)
        avg_time_function = round(statistics.mean(elapsed_times), 2)
        std_dev_function = round(statistics.stdev(elapsed_times), 2)

        print(f"\tFunction: {function}")
        print(f"\tMin Time: {min_time_function} seconds")
        print(f"\tMax Time: {max_time_function} seconds")
        print(f"\tAvg Time: {avg_time_function} seconds")
        print(f"\tStandard Deviation: {std_dev_function} seconds")
