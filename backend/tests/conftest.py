import pytest
from django.contrib.auth.models import User
from aomail.models import SocialAPI, Statistics


@pytest.fixture
def user():
    user, _ = User.objects.get_or_create(username="testuser", password="testpassword")
    return user


@pytest.fixture
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
def statistics(user: User):
    statistics, _ = Statistics.objects.get_or_create(user=user)
    return statistics
