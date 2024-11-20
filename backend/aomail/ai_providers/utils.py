import json
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


def extract_json_from_response(response_text: str) -> dict:
    """
    Extracts and parses a JSON block from the given response text.

    Args:
        response_text (str): The raw text response potentially containing
                              JSON wrapped in markers and unnecessary characters.

    Returns:
        dict: The parsed JSON object if valid JSON is found in the response.

    Raises:
        json.JSONDecodeError: If the response does not contain valid JSON or
                              cannot be parsed.
    """
    try:
        json_text = (
            response_text.replace("Content: ```json", "")
            .replace("```", "")
            .replace("json\n", "")
            .strip()
        )
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding JSON: {str(e)}")
