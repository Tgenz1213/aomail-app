from aomail.ai_providers.google.client import extract_contacts_recipients


def test_extract_contacts_recipients():
    query = "Send an email to John Doe, Jane Doe, and John Smith"
    result = extract_contacts_recipients(query)
    assert result["main_recipients"] == ["John Doe", "Jane Doe", "John Smith"]
    assert result["cc_recipients"] == []
    assert result["bcc_recipients"] == []
    assert type(result["tokens_input"]) == int
    assert type(result["tokens_output"]) == int
