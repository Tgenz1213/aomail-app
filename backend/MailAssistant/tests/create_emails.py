import uuid
import random
import datetime
import json
from django.http import HttpRequest
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from MailAssistant.constants import (
    GOOGLE_PROVIDER,
    MICROSOFT_PROVIDER,
    IMPORTANT,
    INFORMATIVE,
    USELESS,
)
from MailAssistant.models import CC_sender, Email

EMAIL_PROVIDERS = [GOOGLE_PROVIDER, MICROSOFT_PROVIDER]


@api_view(["POST"])
@permission_classes([AllowAny])
def create_emails(request: HttpRequest) -> Response:
    try:
        parameters = json.loads(request.body)
        user = 1  # Hardcoded for testing

        # Create the queryset with all filters applied
        filters = {"user": user, "answer_later": False}
        queryset = Email.objects.filter(**filters).order_by("-date")
        first_email = queryset.first()

        if first_email:
            for i in range(999):
                email = Email.objects.create(
                    user=first_email.user,
                    social_api=first_email.social_api,
                    provider_id=str(uuid.uuid4()),  # Generating a unique UUID
                    subject=first_email.subject,
                    sender=first_email.sender,
                    short_summary=first_email.short_summary,
                    one_line_summary="this is a one line summary",
                    html_content=first_email.html_content,
                    date=timezone.now()
                    + datetime.timedelta(
                        days=random.randint(-1825, 1825)
                    ),  # Random date within ±5 years
                    read_date=timezone.now()
                    + datetime.timedelta(
                        days=random.randint(-1825, 1825)
                    ),  # Random date within ±5 years
                    has_attachments=random.choice([True, False]),
                    answer=random.choice(
                        [
                            "Answer Required",
                            "Might Require Answer",
                            "No Answer Required",
                        ]
                    ),
                    relevance=random.choice(
                        ["Highly Relevant", "Possibly Relevant", "Not Relevant"]
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
                        [
                            "augustin.rolet.pro@gmail.com",
                            "augustin@MailAssistant.onmicrosoft.com",
                        ]
                    ),
                    name="name",
                )
                print(f"Created email {i + 1}/999")

        return Response(
            {"message": "Emails filtered and duplicated successfully"},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
