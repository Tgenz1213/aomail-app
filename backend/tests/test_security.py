import pytest
from aomail.utils.security import encrypt_text, decrypt_text


@pytest.fixture
def encryption_key():
    return "XP6XNlULLDpZnZvskYE_dvJ3PPpXsmtFAv37Dlt3ak4="


def test_encrypt_text(encryption_key: str):
    assert encrypt_text(encryption_key, "test") != "test"


def test_decrypt_text(encryption_key: str):
    assert decrypt_text(encryption_key, encrypt_text(encryption_key, "test")) == "test"
