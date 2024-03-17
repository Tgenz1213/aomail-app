from colorama import Fore, init
import time
import statistics
import gpt_3_5_turbo, claude, mistral


######################## CONSTANTS ########################
# TODO: add gpt_4
# TODO: add role as a parameter in get_prompt_response for testing by role
# TODO: generate a pdf file
LIST_AI_PROVIDERS = [gpt_3_5_turbo, claude, mistral]


# ----------------------- new_mail_recommendation EXAMPLES -----------------------#
examples = [
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


results = {}
ai_providers_stats = {provider.__name__: [] for provider in LIST_AI_PROVIDERS}

for example in examples:
    mail_content, email_subject, user_recommendation = example

    for ai_provider in LIST_AI_PROVIDERS:
        start_time = time.time()
        # TODO: add a counter per ia to check the success rate
        # TODO: store errors for debugging
        try:
            result = ai_provider.new_mail_recommendation(
                mail_content, email_subject, user_recommendation
            )
        except:
            pass
        elapsed_time = time.time() - start_time

        # Store the results
        results[(mail_content, email_subject, ai_provider.__name__)] = {
            "result": result,
            "elapsed_time": elapsed_time,
            "ai_provider": ai_provider.__name__,
        }
        ai_providers_stats[ai_provider.__name__].append(elapsed_time)

        print(f"AI Provider: {ai_provider.__name__}")
        print(f"{Fore.LIGHTBLUE_EX}{result}")
        print(f"Elapsed Time: {elapsed_time} seconds\n")

# Extracting elapsed times for all prompts
all_elapsed_times = [result["elapsed_time"] for result in results.values()]

# ----------------------- PRINT RESULTS -----------------------#
min_time = round(min(all_elapsed_times), 2)
max_time = round(max(all_elapsed_times), 2)
print(f"Min Time: {min_time} seconds")
print(f"Max Time: {max_time} seconds")

avg_time_all_prompts = round(statistics.mean(all_elapsed_times), 2)
print(f"Avg Time for All Prompts: {avg_time_all_prompts} seconds")

std_dev_all_prompts = round(statistics.stdev(all_elapsed_times), 2)
print(f"Standard Deviation for All Prompts: {std_dev_all_prompts} seconds")

# Print statistics for each AI provider
for provider, elapsed_times in ai_providers_stats.items():
    min_time_provider = round(min(elapsed_times), 2)
    max_time_provider = round(max(elapsed_times), 2)
    avg_time_provider = round(statistics.mean(elapsed_times), 2)
    std_dev_provider = round(statistics.stdev(elapsed_times), 2)

    print(f"\nAI Provider: {provider}")
    print(f"Min Time: {min_time_provider} seconds")
    print(f"Max Time: {max_time_provider} seconds")
    print(f"Avg Time: {avg_time_provider} seconds")
    print(f"Standard Deviation: {std_dev_provider} seconds")


"""    start_time = time.time()
correct_mail_language_mistakes("peti test appl", "c un  emai de test envoyer depus l'appl")
execution_time = time.time() - start_time

print(f"{Fore.GREEN}Le temps d'exécution du script n°2 est de {execution_time} secondes.")"""
