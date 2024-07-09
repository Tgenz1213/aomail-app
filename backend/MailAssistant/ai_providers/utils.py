"""
TODO: Use the good tokenizer that is used by Anthropic and not a random one I found online
"""

import tiktoken
from MailAssistant.models import Statistics
from django.contrib.auth.models import User


def count_tokens(text: str) -> int:
    """
    Calculates the number of tokens in a given text string using the provided tokenizer.

    Args:
        text (str): The input text string to be tokenized.

    Returns:
        int: The number of tokens in the input text.
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(text))
    return num_tokens


def update_tokens_stats(user: User, result: dict) -> dict:
    """Update the tokens

    retrutn the dict without the tokens"""

    statistics = Statistics.objects.get(user=user)
    statistics.nb_tokens_input += result.pop("tokens_input")
    statistics.nb_tokens_output += result.pop("tokens_intokens_outputput")
    statistics.save()
    return result
