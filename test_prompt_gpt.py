
import json
from colorama import Fore, init
import openai
import time
import statistics



######################## GPT - 3.5 turbo API SETTINGS ########################
openai.organization = "org-YSlFvq9rM1qPzM15jewopUUt"
openai.api_key = "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"
init(autoreset=True)




def gpt_new_mail_recommendation(mail_content, email_subject, role):
    template = """As an email assistant, enhance the subject and body of this email in both QUANTITY and QUALITY in FRENCH, while preserving key details from the original version.
    
    Answer must be a Json format with two keys: subject (string) AND body (HTML format)

    subject: {email_subject},
    body: {mail_content}
    """
    formatted_prompt = template.format(email_subject=email_subject, mail_content=mail_content)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": role, "content": formatted_prompt}],
    )

    clear_text = response.choices[0].message['content'].strip()
    result_json = json.loads(clear_text)

    return result_json


examples = [
    ("<p>Hello, can I ask a question about Graph API implementation inside an app here?</p>", ""),
    ("<p>bjr Msr DUPONT, je vous souahite une bonne année. Je c que l'algebre ct dure et je nai ps compris grand chse mais g fé de mon miux. Bonne continuatioN. G plein de projet et rencontré d personne fantastiques. Ctt année va etre incroyable, je sui mega focus et j'apprend bcp de ttrucs en info. Augustin <i>Software engineer student</i></p>", "Maths - bilan des 2 dernières ans"),
    ("<p>Salut <strong>papi</strong> cv ? nous on séclate en Espagne!!! on ador la piscine. Claude et la fam</p>", "NEws des vacs"),
    ("<p>slt cv jsp koi dir. si tu voi ca c que test a march ✌️😊</p>", "msg de test ala tem"),
    ("<p>je crois que g trouvé quelquechose de pas mal en <strong>prompt engineering</strong>. jesp que cv de votr cote. un peu de taf en back en front et on pourra push en prod</p>", "proje - on av bien et vite"),
    ("<p>Je vais sans doute vous rejoindre l'année prochaine car je ne suis qu'en ING2 pour l'instant. Et ce semestre est vraiment compliqué, il me reste une seule semaine et après je reviens vers Théo sur Mail Assistant et je me réattaque au pb de licence M365</p>", "Salut Jean, ça se passe bien ton alternance?"),
    ("<p>bsr madama. Je suis en 2eme année de cyle prépa. Est ce ke je peux av la lsit des entreprises ds lesquell les eleves en IR3, 4, 5 on fait soit 1 stage soi une alternance. Merc de votre retour. Augustin ROLET</p>", "Stages & Alter"),
]

# Dictionary to store results
results = {}

for example in examples:
    mail_content, email_subject = example

    for role in ["system", "user", "assistant"]:
        # Record the start time
        start_time = time.time()

        # Call the function with different roles
        result = gpt_new_mail_recommendation(mail_content, email_subject, role)

        elapsed_time = time.time() - start_time

        # Store the results
        results[(mail_content, email_subject, role)] = {
            "result": result,
            "elapsed_time": elapsed_time
        }

        # Print the output
        print(f'{Fore.LIGHTBLUE_EX}{result}')
        print(f"Elapsed Time for role '{role}': {elapsed_time} seconds\n")



# Extracting elapsed times for all prompts and each role
all_elapsed_times = [result["elapsed_time"] for result in results.values()]
elapsed_times_by_role = {role: [] for role in ["system", "user", "assistant"]}
for key, result in results.items():
    role = key[2]
    elapsed_times_by_role[role].append(result["elapsed_time"])

# Round function for rounding to 2 decimal places
def round_to_2_decimal_places(value):
    return round(value, 2)

# Print min and max time
min_time = round_to_2_decimal_places(min(all_elapsed_times))
max_time = round_to_2_decimal_places(max(all_elapsed_times))
print(f"Min Time: {min_time} seconds")
print(f"Max Time: {max_time} seconds")

# Print average time for all prompts
avg_time_all_prompts = round_to_2_decimal_places(statistics.mean(all_elapsed_times))
print(f"Avg Time for All Prompts: {avg_time_all_prompts} seconds")

# Print average time for each role
for role, elapsed_times in elapsed_times_by_role.items():
    avg_time_role = round_to_2_decimal_places(statistics.mean(elapsed_times))
    print(f"Avg Time for Role '{role}': {avg_time_role} seconds")

# Print standard deviation for all prompts
std_dev_all_prompts = round_to_2_decimal_places(statistics.stdev(all_elapsed_times))
print(f"Standard Deviation for All Prompts: {std_dev_all_prompts} seconds")

# Print standard deviation for each role
for role, elapsed_times in elapsed_times_by_role.items():
    std_dev_role = round_to_2_decimal_places(statistics.stdev(elapsed_times))
    print(f"Standard Deviation for Role '{role}': {std_dev_role} seconds")