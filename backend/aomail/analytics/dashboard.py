"""
Handles the retrival of data ready to be ploted in charts

Endpoints:
- ✅ dashboard_data: Returns the distribution of emails per category per answer requirement
"""

import logging
from django.http import HttpRequest
from rest_framework import status
from aomail.models import Category, Email
from rest_framework.response import Response
from rest_framework.decorators import api_view
from aomail.utils.security import subscription
from aomail.constants import (
    ALLOW_ALL,
    ANSWER_REQUIRED,
    HIGHLY_RELEVANT,
    IMPORTANT,
    INFORMATIVE,
    MIGHT_REQUIRE_ANSWER,
    NO_ANSWER_REQUIRED,
    NOT_RELEVANT,
    POSSIBLY_RELEVANT,
    USELESS,
)

LOGGER = logging.getLogger(__name__)


@api_view(["GET"])
@subscription(ALLOW_ALL)
def dashboard_data(request: HttpRequest) -> Response:
    """
    Returns email distribution statistics per category for the authenticated user.

    Returns:
        Response with distribution data mapping category names to email counts
        for each classification, or error response if fetch fails.
    """
    try:
        user = request.user
        categories = Category.objects.filter(user=user)

        distribution = {}
        for category in categories:
            nb_emails_important = Email.objects.filter(
                user=user, category=category.id, priority=IMPORTANT
            )
            nb_emails_informative = Email.objects.filter(
                user=user, category=category.id, priority=INFORMATIVE
            )
            nb_emails_useless = Email.objects.filter(
                user=user, category=category.id, priority=USELESS
            )

            nb_emails_answer_required = Email.objects.filter(
                user=user, category=category.id, answer=ANSWER_REQUIRED
            )
            nb_emails_might_require_answer = Email.objects.filter(
                user=user, category=category.id, answer=MIGHT_REQUIRE_ANSWER
            )
            nb_emails_no_answer_required = Email.objects.filter(
                user=user, category=category.id, answer=NO_ANSWER_REQUIRED
            )

            nb_emails_highly_relevant = Email.objects.filter(
                user=user, category=category.id, answer=HIGHLY_RELEVANT
            )
            nb_emails_possibly_relevant = Email.objects.filter(
                user=user, category=category.id, answer=POSSIBLY_RELEVANT
            )
            nb_emails_not_relevant = Email.objects.filter(
                user=user, category=category.id, answer=NOT_RELEVANT
            )

            distribution[category.name] = {
                "nbEmailsImportant": nb_emails_important.count(),
                "nbEmailsInformative": nb_emails_informative.count(),
                "nbEmailsUseless": nb_emails_useless.count(),
                "nbEmailsAnswerRequired": nb_emails_answer_required.count(),
                "nbEmailsMightRequireAnswer": nb_emails_might_require_answer.count(),
                "nbEmailsNoAnswerRequired": nb_emails_no_answer_required.count(),
                "nbEmailsHighlyRelevant": nb_emails_highly_relevant.count(),
                "nbEmailsPossiblyRelevant": nb_emails_possibly_relevant.count(),
                "nbEmailsNotRelevant": nb_emails_not_relevant.count(),
            }

        return Response(
            {"distribution": distribution},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        LOGGER.error(f"Error fetching dashboard data: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
