import json
import pytest
from aomail.ai_providers.utils import extract_json_from_response, count_corrections
from django.contrib.auth.models import User
from aomail.models import Statistics
from aomail.ai_providers.utils import update_tokens_stats


def test_extract_json_from_response():
    response_text = """
    Content: ```json
    {
        "response": "Hello, world!"
    }
    ```
    """
    assert extract_json_from_response(response_text) == {"response": "Hello, world!"}
    response_text = """
    Content: ```
    {
        "response": "Hello, world!"
    }
    ```
    """
    assert extract_json_from_response(response_text) == {"response": "Hello, world!"}
    response_text = """
    {
        "response": "Hello, world!"
    }
    """
    assert extract_json_from_response(response_text) == {"response": "Hello, world!"}


def test_extract_json_from_response_errors():
    with pytest.raises(IndexError):
        extract_json_from_response("")
    with pytest.raises(IndexError):
        extract_json_from_response("Hello, world!")
    with pytest.raises(json.JSONDecodeError):
        extract_json_from_response("```{'key': 'value}```")
    with pytest.raises(json.JSONDecodeError):
        extract_json_from_response("```{Hello, world!}```")
    with pytest.raises(json.JSONDecodeError):
        extract_json_from_response("```{Hello, world!```")
    with pytest.raises(json.JSONDecodeError):
        extract_json_from_response("```json{Hello, world!```")


def test_count_corrections():
    assert (
        count_corrections(
            "Hello, world!", "Hello, world!", "Hello, world!", "Hello, world!"
        )
        == 0
    )
    assert (
        count_corrections(
            "Hello, world!", "Hello, world!", "Hello world!", "Hello world!"
        )
        == 2
    )
    assert (
        count_corrections(
            "Original subject", "Original body", "Corrected subject", "Corrected body"
        )
        == 2
    )


@pytest.fixture
def test_update_tokens_stats(user: User, statistics: Statistics):
    update_tokens_stats(user, {"tokens_input": 10, "tokens_output": 20})
    statistics.refresh_from_db()
    assert statistics.nb_tokens_input == 10
    assert statistics.nb_tokens_output == 20
