import pytest
from aomail.ai_providers.utils import extract_json_from_response, count_corrections
from django.contrib.auth.models import User
from aomail.models import SocialAPI, Statistics
from aomail.ai_providers.utils import update_tokens_stats


@pytest.fixture
# @pytest.mark.django_db
def user():
    user, _ = User.objects.get_or_create(username="testuser", password="testpassword")
    return user


@pytest.fixture
# @pytest.mark.django_db
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


@pytest.fixture
# @pytest.mark.django_db
def statistics(user: User):
    statistics, _ = Statistics.objects.get_or_create(user=user)
    return statistics


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


@pytest.mark.django_db
def test_update_tokens_stats(user: User, statistics: Statistics):
    update_tokens_stats(user, {"tokens_input": 10, "tokens_output": 20})
    statistics.refresh_from_db()
    assert statistics.nb_tokens_input == 10
    assert statistics.nb_tokens_output == 20
