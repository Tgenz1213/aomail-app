"""
Handles prompt engineering requests for GPT-4 API.

⚠️ Some functions are outdated ⚠️
"""

import logging
import os
import openai


LOGGER = logging.getLogger(__name__)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID")


######################## TEXT PROCESSING UTILITIES ########################
def get_prompt_response(formatted_prompt):
    """Returns the prompt response"""
    client = openai.OpenAI(organization=OPENAI_ORG_ID, api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "system", "content": formatted_prompt}],
    )
    return response
