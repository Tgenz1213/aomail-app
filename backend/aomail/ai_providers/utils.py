import tiktoken
from aomail.models import Statistics
from django.contrib.auth.models import User


def update_tokens_stats(user: User, result: dict) -> dict:
    """
    Update token statistics for a user and remove token information from the result dictionary.

    Args:
        user (User): The User object for whom the token statistics are being updated.
        result (dict): A dictionary containing the result of an AI function.

    Returns:
        dict: The modified result dictionary with 'tokens_input' and 'tokens_output' keys removed.
    """
    statistics = Statistics.objects.get(user=user)
    statistics.nb_tokens_input += result.pop("tokens_input")
    statistics.nb_tokens_output += result.pop("tokens_output")
    statistics.save()
    return result
