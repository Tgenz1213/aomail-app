"""
Handles prompt engineering requests for Mistral API.

⚠️ Some functions are outdated ⚠️
"""

import logging
import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


LOGGER = logging.getLogger(__name__)
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")


######################## TEXT PROCESSING UTILITIES ########################
def get_prompt_response(formatted_prompt, model, role):
    """Returns the prompt response"""
    client = MistralClient(api_key=MISTRAL_API_KEY)
    message = ChatMessage(role=role, content=formatted_prompt)
    response = client.chat(model=model, messages=[message])
    return response
