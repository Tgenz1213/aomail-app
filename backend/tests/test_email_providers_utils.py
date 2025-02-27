import pytest
from django.contrib.auth.models import User
from aomail.models import Email, Rule, Sender, SocialAPI, Statistics
from aomail.constants import (
    ANSWER_REQUIRED,
    DEFAULT_CATEGORY,
    HIGHLY_RELEVANT,
    IMPORTANT,
    NOT_RELEVANT,
    USELESS,
)
from aomail.email_providers.utils import (
    apply_rules,
    delete_email_rule,
    save_email_to_db,
    verify_condition,
)
from aomail.utils.security import encrypt_text


@pytest.mark.django_db
def user():
    user, _ = User.objects.get_or_create(username="testuser", password="testpassword")
    return user


@pytest.mark.django_db
def social_api(user: User):
    social_api, _ = SocialAPI.objects.get_or_create(
        user=user,
        email="testuser@example.com",
        type_api="google",
        user_description="user_description",
        access_token="access_token",
        refresh_token="refresh_token",
    )
    return social_api


@pytest.mark.django_db
def statistics(user: User):
    statistics, _ = Statistics.objects.get_or_create(user=user)
    return statistics


@pytest.mark.django_db
def rules(user: User):
    rule1 = Rule.objects.create(
        user=user,
        logical_operator="AND",
        domains=["example.com"],
        has_attachements=True,
        action_set_priority=IMPORTANT,
        action_set_category=DEFAULT_CATEGORY,
    )

    rule2 = Rule.objects.create(
        user=user,
        logical_operator="OR",
        sender_emails=["important@company.com"],
        flags=["meeting"],
        action_set_flags=["notification"],
        action_mark_as=["read"],
    )

    rule3 = Rule.objects.create(
        user=user,
        logical_operator="AND",
        categories=[DEFAULT_CATEGORY],
        priorities=[USELESS],
        relevances=[NOT_RELEVANT],
        action_delete=True,
    )

    rule4 = Rule.objects.create(
        user=user,
        logical_operator="OR",
        answers=[ANSWER_REQUIRED],
        action_transfer_recipients=["assistant@company.com"],
        action_reply_prompt="Please handle this request",
    )

    return [rule1, rule2, rule3, rule4]


@pytest.fixture
def processed_email():
    return {
        "email_data": {
            "is_reply": False,
            "email_id": "email_id",
            "from_info": ("testuser", "testuser@example.com"),
            "safe_html": "safe_html",
            "subject": "subject",
            "sent_date": "2024-01-01 00:00:00",
            "has_attachments": True,
            "cc_info": [],
            "bcc_info": [],
            "attachments": [],
            "image_files": [],
        },
        "email_processed": {
            "category": DEFAULT_CATEGORY,
            "priority": IMPORTANT,
            "answer": ANSWER_REQUIRED,
            "relevance": HIGHLY_RELEVANT,
            "flags": {
                "spam": False,
                "scam": False,
                "newsletter": False,
                "notification": True,
                "meeting": True,
            },
            "summary": {
                "one_line": "One sentence summary",
                "short": "Short summary of the email",
            },
        },
        "summary": {
            "keypoints": [
                "keypoint1",
                "keypoint2",
                "keypoint3",
            ],
            "category": DEFAULT_CATEGORY,
            "organization": "organization",
            "topic": "topic",
        },
    }


@pytest.mark.django_db
def sender():
    return Sender.objects.create(
        name="sender",
        email="sender@example.com",
    )


@pytest.mark.django_db
def email_entry(sender: Sender, social_api: SocialAPI):
    return Email.objects.create(
        social_api=social_api,
        provider_id="email_id",
        email_provider=social_api.type_api,
        short_summary=encrypt_text(
            "XP6XNlULLDpZnZvskYE_dvJ3PPpXsmtFAv37Dlt3ak4=", "short summary"
        ),
        one_line_summary=encrypt_text(
            "XP6XNlULLDpZnZvskYE_dvJ3PPpXsmtFAv37Dlt3ak4=",
            "one line summary",
        ),
        html_content=encrypt_text(
            "XP6XNlULLDpZnZvskYE_dvJ3PPpXsmtFAv37Dlt3ak4=", "html content"
        ),
        subject="subject",
        priority=IMPORTANT,
        sender=sender,
        category=DEFAULT_CATEGORY,
        user=user,
        date="2024-01-01 00:00:00",
        has_attachments=True,
        answer="answer",
        relevance=HIGHLY_RELEVANT,
        spam=False,
        scam=False,
        newsletter=False,
        notification=True,
        meeting=True,
    )


def test_apply_rules(processed_email: dict, user: User, email_entry: Email):
    apply_rules(processed_email, user, email_entry)
    assert email_entry.category == DEFAULT_CATEGORY


def test_verify_condition(processed_email: dict, rules: list[Rule]):
    rule1, rule2, rule3, rule4 = rules

    # Test domain condition
    processed_email["email_data"]["from_info"] = ("Test User", "user@example.com")
    assert verify_condition("domains", processed_email, rule1) == True
    processed_email["email_data"]["from_info"] = ("Test User", "user@other.com")
    assert verify_condition("domains", processed_email, rule1) == False

    # Test sender email condition
    processed_email["email_data"]["from_info"] = ("Important", "important@company.com")
    assert verify_condition("sender_emails", processed_email, rule2) == True
    processed_email["email_data"]["from_info"] = ("Other", "other@company.com")
    assert verify_condition("sender_emails", processed_email, rule2) == False

    # Test attachments condition
    processed_email["email_data"]["has_attachments"] = True
    assert verify_condition("has_attachements", processed_email, rule1) == True
    processed_email["email_data"]["has_attachments"] = False
    assert verify_condition("has_attachements", processed_email, rule1) == False

    # Test category condition
    processed_email["email_processed"]["category"] = DEFAULT_CATEGORY
    assert verify_condition("categories", processed_email, rule3) == True
    processed_email["email_processed"]["category"] = "Other"
    assert verify_condition("categories", processed_email, rule3) == False

    # Test priority condition
    processed_email["email_processed"]["priority"] = USELESS
    assert verify_condition("priorities", processed_email, rule3) == True
    processed_email["email_processed"]["priority"] = IMPORTANT
    assert verify_condition("priorities", processed_email, rule3) == False

    # Test relevance condition
    processed_email["email_processed"]["relevance"] = NOT_RELEVANT
    assert verify_condition("relevances", processed_email, rule3) == True
    processed_email["email_processed"]["relevance"] = HIGHLY_RELEVANT
    assert verify_condition("relevances", processed_email, rule3) == False

    # Test flags condition
    processed_email["email_processed"]["flags"] = {
        "meeting": True,
        "notification": True,
    }
    assert verify_condition("flags", processed_email, rule2) == True
    processed_email["email_processed"]["flags"] = {"other": True}
    assert verify_condition("flags", processed_email, rule2) == False

    # Test answer condition
    processed_email["email_processed"]["answer"] = ANSWER_REQUIRED
    assert verify_condition("answers", processed_email, rule4) == True
    processed_email["email_processed"]["answer"] = "No Answer"
    assert verify_condition("answers", processed_email, rule4) == False

    # Test transfer recipients condition (should always return True as it's an action)
    assert verify_condition("transfer_recipients", processed_email, rule4) == True

    # Test non-existing condition
    assert verify_condition("non_existing_condition", processed_email, rule1) == False


def test_delete_email_rule_with_domain(user: User):
    """Test email deletion rule based on domain."""
    email_data = {"from_info": ("Spam", "spammer@spam.com")}

    Rule.objects.create(user=user, domains=["spam.com"], action_delete=True)

    assert delete_email_rule(user, email_data) == True


def test_delete_email_rule_with_specific_email(user: User):
    email_data = {"from_info": ("Specific", "bad@company.com")}

    Rule.objects.create(
        user=user, sender_emails=["bad@company.com"], action_delete=True
    )
    assert delete_email_rule(user, email_data) == True

    email_data["from_info"] = ("Good", "good@company.com")
    assert delete_email_rule(user, email_data) == False


def test_save_email_to_db(processed_email: dict, user: User, social_api: SocialAPI):
    email_entry = save_email_to_db(processed_email, user, social_api)

    assert email_entry.short_summary != "short summary"
    assert email_entry.one_line_summary != "one line summary"
    assert email_entry.html_content != "html content"
    assert email_entry.subject == "subject"
    assert email_entry.priority == IMPORTANT
    assert email_entry.sender == sender
    assert email_entry.category == DEFAULT_CATEGORY
    assert email_entry.user == user
    assert email_entry.date == "2024-01-01 00:00:00"
    assert email_entry.has_attachments == True
    assert email_entry.answer == "answer"
    assert email_entry.relevance == HIGHLY_RELEVANT
    assert email_entry.spam == False
    assert email_entry.scam == False
    assert email_entry.newsletter == False
    assert email_entry.notification == True
    assert email_entry.meeting == True
    assert email_entry.read == False
    assert email_entry.archive == False
    assert email_entry.answer_later == False
    assert email_entry.read_date == None
    assert email_entry.social_api == social_api
    assert email_entry.provider_id == "email_id"
    assert email_entry.email_provider == social_api.type_api
    assert email_entry.cc_senders.count() == 0
    assert email_entry.bcc_senders.count() == 0
    assert email_entry.pictures.count() == 0
    assert email_entry.attachments.count() == 0
