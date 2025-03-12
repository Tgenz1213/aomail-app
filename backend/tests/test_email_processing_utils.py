from aomail.utils.email_processing import (
    camel_to_snake,
    is_no_reply_email,
    preprocess_email,
    validate_email_address,
    snake_to_camel,
    contains_html,
    concat_text,
)


def test_validate_email_address():
    assert validate_email_address("test.test@gmail.com") == True
    assert validate_email_address("faKeEmail@outlook.fr") == True
    assert validate_email_address("faKe239Email@outlook.fr") == True
    assert validate_email_address("") == False
    assert validate_email_address("test.test.test") == False


def test_camel_to_snake():
    assert camel_to_snake("nbEmailsReceived") == "nb_emails_received"
    assert camel_to_snake("camelCase") == "camel_case"
    assert camel_to_snake("ABC") == "a_b_c"
    assert camel_to_snake("alreadysnakecase") == "alreadysnakecase"
    assert camel_to_snake("") == ""


def test_snake_to_camel():
    assert snake_to_camel("nb_emails_received") == "nbEmailsReceived"
    assert snake_to_camel("camel_case") == "camelCase"
    assert snake_to_camel("already_snake") == "alreadySnake"
    assert snake_to_camel("") == ""
    assert snake_to_camel("_hidden") == "Hidden"


def test_is_no_reply_email():
    assert is_no_reply_email("no-reply@gmail.com") == True
    assert is_no_reply_email("donotreply@gmail.com") == True
    assert is_no_reply_email("do-not-reply@gmail.com") == True
    assert is_no_reply_email("noreply@gmail.com") == True
    assert is_no_reply_email("test.test@gmail.com") == False
    assert is_no_reply_email("faKeEmail@outlook.fr") == False
    assert is_no_reply_email("faKe239Email@outlook.fr") == False


def test_preprocess_email():
    assert preprocess_email("<https://aomail.ai>") == ""
    assert preprocess_email("https://aomail.ai") == ""
    assert preprocess_email("http://aomail.ai") == ""
    assert preprocess_email("random text\r\nend of text") == "random text\nend of text"
    assert (
        preprocess_email("random text\n\n\n\n\nend of text")
        == "random text\n\nend of text"
    )
    assert preprocess_email("[image:[myImageStuff]") == ""
    assert preprocess_email("  spaces  at  ends  ") == "spaces at ends"
    assert preprocess_email("http://link.com some text") == "some text"
    assert (
        preprocess_email("mixed\r\nline\nending\r\nstyles")
        == "mixed\nline\nending\nstyles"
    )


def test_contains_html():
    assert contains_html("<div>test</div>") == True
    assert contains_html("plain text") == False
    assert contains_html("&nbsp; with entity") == True
    assert contains_html("<!DOCTYPE html>") == True
    assert contains_html(b"<span>bytes test</span>") == True


def test_concat_text():
    assert concat_text(None, "first") == "first"
    assert concat_text("existing", "append") == "existingappend"
    assert concat_text(None, b"bytes text") == "bytes text"
    assert concat_text("existing", b"bytes append") == "existingbytes append"
