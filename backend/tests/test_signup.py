import pytest
from aomail.authentication.signup import validate_signup_data


@pytest.mark.django_db
def test_validate_signup_data():
    assert validate_signup_data({"username": "test test"}) == {
        "error": "Username must not contain spaces"
    }
    assert validate_signup_data({"username": "test", "password": "test"}) == {
        "error": "Password length must be between 8 and 128 characters"
    }
    assert validate_signup_data(
        {
            "username": "test",
            "password": "testtest",
            "emailAddress": "test@test.com",
            "imapAppPassword": "secureAppPassword",
            "imapHost": "imap.company.com",
            "imapPort": 993,
            "imapEncryption": "tls",
            "smtpAppPassword": "secureAppPassword",
            "smtpHost": "smtp.company.com",
            "smtpPort": 465,
            "smtpEncryption": "ssl",
        }
    ) == {"message": "User signup data validated successfully"}


@pytest.mark.django_db
def test_validate_signup_data_oauth():
    assert validate_signup_data(
        {"username": "test", "password": "testtest", "code": 100}
    ) == {"error": "Code must be a string"}
    assert validate_signup_data(
        {"username": "test", "password": "testtest", "code": "valid_code"}
    ) == {"message": "User signup data validated successfully"}


@pytest.mark.django_db
def test_validate_signup_data_imap_errors():
    assert validate_signup_data(
        {
            "username": "test",
            "password": "testtest",
        }
    ) == {"error": "Email address is not in a valid format"}
    assert validate_signup_data(
        {"username": "test", "password": "testtest", "emailAddress": "test@test.com"}
    ) == {"error": "IMAP app password is required"}
    assert validate_signup_data(
        {
            "username": "test",
            "password": "testtest",
            "emailAddress": "test@test.com",
            "imapAppPassword": "secureAppPassword",
        }
    ) == {"error": "IMAP host is required"}
    assert validate_signup_data(
        {
            "username": "test",
            "password": "testtest",
            "emailAddress": "test@test.com",
            "imapAppPassword": "secureAppPassword",
            "imapHost": "imap.company.com",
            "imapPort": "993",
        }
    ) == {"error": "IMAP port must be an integer"}
    assert validate_signup_data(
        {
            "username": "test",
            "password": "testtest",
            "emailAddress": "test@test.com",
            "imapAppPassword": "secureAppPassword",
            "imapHost": "imap.company.com",
            "imapPort": 993,
        }
    ) == {"error": "IMAP encryption must be either 'tls' or 'none'"}
    assert validate_signup_data(
        {
            "username": "test",
            "password": "testtest",
            "emailAddress": "test@test.com",
            "imapAppPassword": "secureAppPassword",
            "imapHost": "imap.company.com",
            "imapPort": 993,
            "imapEncryption": "fake",
        }
    ) == {"error": "IMAP encryption must be either 'tls' or 'none'"}


@pytest.mark.django_db
def test_validate_signup_data_imap_errors():
    assert validate_signup_data(
        {
            "username": "test",
            "password": "testtest",
            "emailAddress": "test@test.com",
            "imapAppPassword": "secureAppPassword",
            "imapHost": "imap.company.com",
            "imapPort": 993,
            "imapEncryption": "tls",
        }
    ) == {"error": "SMTP app password is required"}
    assert validate_signup_data(
        {
            "username": "test",
            "password": "testtest",
            "emailAddress": "test@test.com",
            "imapAppPassword": "secureAppPassword",
            "imapHost": "imap.company.com",
            "imapPort": 993,
            "imapEncryption": "tls",
            "smtpAppPassword": "secureAppPassword",
        }
    ) == {"error": "SMTP host is required"}
    assert validate_signup_data(
        {
            "username": "test",
            "password": "testtest",
            "emailAddress": "test@test.com",
            "imapAppPassword": "secureAppPassword",
            "imapHost": "imap.company.com",
            "imapPort": 993,
            "imapEncryption": "tls",
            "smtpAppPassword": "secureAppPassword",
            "smtpHost": "smtp.company.com",
            "smtpPort": "465",
        }
    ) == {"error": "SMTP port must be an integer"}
    assert validate_signup_data(
        {
            "username": "test",
            "password": "testtest",
            "emailAddress": "test@test.com",
            "imapAppPassword": "secureAppPassword",
            "imapHost": "imap.company.com",
            "imapPort": 993,
            "imapEncryption": "tls",
            "smtpAppPassword": "secureAppPassword",
            "smtpHost": "smtp.company.com",
            "smtpPort": 465,
        }
    ) == {"error": "SMTP encryption must be either 'tls' or 'ssl' or 'none'"}
    assert validate_signup_data(
        {
            "username": "test",
            "password": "testtest",
            "emailAddress": "test@test.com",
            "imapAppPassword": "secureAppPassword",
            "imapHost": "imap.company.com",
            "imapPort": 993,
            "imapEncryption": "tls",
            "smtpAppPassword": "secureAppPassword",
            "smtpHost": "smtp.company.com",
            "smtpPort": 465,
            "smtpEncryption": "fake",
        }
    ) == {"error": "SMTP encryption must be either 'tls' or 'ssl' or 'none'"}
