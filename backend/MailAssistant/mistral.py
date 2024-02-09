from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import time

start_time = time.time()

model = "mistral-small"

client = MistralClient(api_key='lm7Rv2zv20DfIh5XvBrqSZIpQ2EIi2XJ')

template = """As an email assistant, write a Short and Formal email in FRENCH.
    Improve the QUANTITY and QUALITY in FRENCH according to the user guideline: 'Je serais absent à la réunion de vendredi', it should strictly contain only the information present in the input.

    Answer must be a Json format with two keys: subject (STRING) AND body (HTML)
    """

messages = [
    ChatMessage(role="user", content=template)
]

# No streaming
chat_response = client.chat(
    model=model,
    messages=messages,
)

print(chat_response.choices[0].message.content)

execution_time = time.time() - start_time

print(f"Le temps d'exécution du script est de {execution_time} secondes.")