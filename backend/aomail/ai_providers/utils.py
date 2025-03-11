import json
from aomail.models import Statistics
from django.contrib.auth.models import User
import re


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
        IndexError: If the response does not contain a JSON block.
    """
    try:
        if "```json" in response_text:
            json_text = (
                response_text.replace("Content: ```json", "")
                .replace("```", "")
                .replace("json\n", "")
                .strip()
            )
        else:
            json_text = response_text.split("```")[1].split("```")[0]
        return json.loads(json_text)
    except IndexError as e:
        raise IndexError(f"Error decoding JSON: {str(e)}")
    except json.JSONDecodeError as e:
        raise


def count_corrections(
    original_subject: str,
    original_body: str,
    corrected_subject: str,
    corrected_body: str,
) -> int:
    """
    Counts and compares corrections in original and corrected texts.

    Args:
        original_subject (str): The original subject text.
        original_body (str): The original body text.
        corrected_subject (str): The corrected subject text.
        corrected_body (str): The corrected body text.

    Returns:
        int: The total number of corrections made in the subject and body texts.
    """
    original_subject_words = original_subject.split()
    corrected_subject_words = corrected_subject.split()
    original_body_words = original_body.split()
    corrected_body_words = corrected_body.split()

    subject_corrections = sum(
        orig != corr
        for orig, corr in zip(original_subject_words, corrected_subject_words)
    )
    body_corrections = sum(
        orig != corr for orig, corr in zip(original_body_words, corrected_body_words)
    )

    total_corrections = subject_corrections + body_corrections

    return total_corrections


def ensure_proper_spacing(text: str, signature: str = "") -> str:
    """
    Ensures EXACTLY ONE blank line between content lines in main content.
    Preserves EXACT spacing in signature block.

    Args:
        text (str): The text to process
        signature (str): The signature text to identify signature section
    """
    if not text:
        return text

    # Normalize paragraph spacing with exactly one line break
    text = re.sub(r"</p>\s*<p>", "</p>\n<p>", text)

    # Convert <br> to newlines to handle them as normal line breaks
    text = re.sub(r"<br\s*/?>(?!</)", "\n", text, flags=re.IGNORECASE)

    # Split content and signature if signature exists
    main_content = text
    sig_part = ""

    if signature and signature.strip() in text:
        # Find the signature position and split
        sig_pos = text.find(signature.strip())
        if sig_pos != -1:
            main_content = text[:sig_pos].rstrip()
            sig_part = text[sig_pos:]  # Keep everything after signature start

    # Process main content - ensure one blank line between content
    lines = main_content.split("\n")
    result = []

    # Add lines with exactly one blank line between content
    for line in lines:
        if line.strip():  # If line has actual content
            if result and result[-1].strip():  # If previous line had content
                result.append("")  # Add exactly one blank line
            result.append(line)

    # Add signature if it exists - preserve its exact spacing
    if sig_part:
        if result and result[-1].strip():
            result.append("")
        result.append(sig_part.rstrip())  # Just add it as is, only trim end

    return "\n".join(result)
