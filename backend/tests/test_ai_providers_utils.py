from aomail.ai_providers.utils import extract_json_from_response, count_corrections


def test_extract_json_from_response():
    response_text = """
    Content: ```json
    {
        "response": "Hello, world!"
    }
    ```
    """
    assert extract_json_from_response(response_text) == {"response": "Hello, world!"}


def test_count_corrections():
    assert count_corrections("Hello, world!", "Hello, world!", "Hello, world!", "Hello, world!") == 0
    assert count_corrections("Hello, world!", "Hello, world!", "Hello world!", "Hello world!") == 2
    assert count_corrections("Original subject", "Original body", "Corrected subject", "Corrected body") == 2
