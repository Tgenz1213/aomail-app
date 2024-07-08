"""
This file is just used for debugging with POSTMAN. It can be deleted without any problems
"""

import uuid
import random
import datetime
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpRequest
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from MailAssistant.constants import (
    ANSWER_REQUIRED,
    GOOGLE,
    MICROSOFT,
    IMPORTANT,
    INFORMATIVE,
    MIGHT_REQUIRE_ANSWER,
    USELESS,NO_ANSWER_REQUIRED,HIGHLY_RELEVANT,POSSIBLY_RELEVANT,NOT_RELEVANT
)
from MailAssistant.models import CC_sender, Email, Statistics

EMAIL_PROVIDERS = [GOOGLE, MICROSOFT]

def create_single_email(first_email, i):
    email = Email.objects.create(
        user=first_email.user,
        social_api=first_email.social_api,
        provider_id=str(uuid.uuid4()),
        subject=first_email.subject,
        sender=first_email.sender,
        short_summary=first_email.short_summary,
        one_line_summary="this is a one line summary",
        html_content=first_email.html_content,
        date=timezone.now() + datetime.timedelta(days=random.randint(-1825, 1825)),
        read_date=timezone.now() + datetime.timedelta(days=random.randint(-1825, 1825)),
        has_attachments=random.choice([True, False]),
        answer=random.choice(
            [ANSWER_REQUIRED, MIGHT_REQUIRE_ANSWER, NO_ANSWER_REQUIRED]
        ),
        relevance=random.choice(
            [HIGHLY_RELEVANT, POSSIBLY_RELEVANT, NOT_RELEVANT]
        ),
        priority=random.choice([IMPORTANT, INFORMATIVE, USELESS]),
        scam=random.choice([True, False]),
        spam=random.choice([True, False]),
        newsletter=random.choice([True, False]),
        notification=random.choice([True, False]),
        meeting=random.choice([True, False]),
        category=first_email.category,
        email_provider=random.choice(EMAIL_PROVIDERS),
    )
    CC_sender.objects.create(
        mail_id=email,
        email=random.choice(
            ["augustin.rolet.pro@gmail.com", "augustin@MailAssistant.onmicrosoft.com"]
        ),
        name="name",
    )
    return i


def update_stats():
    user_id = 1
    user = User.objects.get(id=user_id)

    stats = Statistics.objects.get(user=user)

    # Update email categories
    stats.nb_emails_received = Email.objects.filter(user=user).count()
    stats.nb_emails_important = Email.objects.filter(
        user=user, category__name="Important"
    ).count()
    stats.nb_emails_informative = Email.objects.filter(
        user=user, category__name="Informative"
    ).count()
    stats.nb_emails_useless = Email.objects.filter(
        user=user, category__name="Useless"
    ).count()

    # Update token usage (example calculation)
    stats.nb_tokens_input = random.randint(10_000, 1_000_000)
    stats.nb_tokens_output = random.randint(1_000, 10_000)

    # Update answer status
    stats.nb_answer_required = Email.objects.filter(
        user=user, answer="Required"
    ).count()
    stats.nb_might_require_answer = Email.objects.filter(
        user=user, answer="Might Require"
    ).count()
    stats.nb_no_answer_required = Email.objects.filter(
        user=user, answer="No Answer"
    ).count()

    # Update relevance
    stats.nb_highly_relevant = Email.objects.filter(
        user=user, relevance="Highly Relevant"
    ).count()
    stats.nb_possibly_relevant = Email.objects.filter(
        user=user, relevance="Possibly Relevant"
    ).count()
    stats.nb_not_relevant = Email.objects.filter(
        user=user, relevance="Not Relevant"
    ).count()

    # Update flags
    stats.nb_spam = Email.objects.filter(user=user, spam=True).count()
    stats.nb_scam = Email.objects.filter(user=user, scam=True).count()
    stats.nb_newsletter = Email.objects.filter(user=user, newsletter=True).count()
    stats.nb_notification = Email.objects.filter(user=user, notification=True).count()
    stats.nb_meeting = Email.objects.filter(user=user, meeting=True).count()

    stats.save()


@api_view(["POST"])
@permission_classes([AllowAny])
def create_emails(request: HttpRequest) -> Response:
    try:
        parameters = json.loads(request.body)
        user = 1  # Hardcoded for testing

        update_stats()

        filters = {"user": user, "answer_later": False}
        queryset = Email.objects.filter(**filters).order_by("-date")
        first_email = queryset.first()

        if first_email:
            num_emails = 0
            with ThreadPoolExecutor(max_workers=20) as executor:
                futures = [
                    executor.submit(create_single_email, first_email, i)
                    for i in range(num_emails)
                ]

                for future in as_completed(futures):
                    i = future.result()
                    if (i + 1) % 100 == 0:
                        print(f"Created email {i + 1}/{num_emails}")

        return Response(
            {"message": "Emails filtered and duplicated successfully"},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
