import uuid
import random
import datetime
import json
from collections import defaultdict
from django.db.models import Subquery, Exists, OuterRef
from django.http import HttpRequest
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import HttpRequest
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from collections import defaultdict
import json
import datetime


from MailAssistant.constants import (
    GOOGLE_PROVIDER,
    IMPORTANT,
    INFORMATIVE,
    MICROSOFT_PROVIDER,
    USELESS,
)
from MailAssistant.models import (
    CC_sender,
    Category,
    SocialAPI,
    Email,
    Rule,
)

EMAIL_PROVIDERS = [GOOGLE_PROVIDER, MICROSOFT_PROVIDER]



# TODO: create a endpoint get_emails_data (returns data for a list of ids (between 25 and 100 ids max))
# "html_content": email.html_content



# TODO: only 1 endpoint for answer later emails and normal emails
# split the function into smallers for clarity
@api_view(["POST"])
@permission_classes([AllowAny])
def get_user_emails(request: HttpRequest) -> Response:
    """
    Retrieves filtered user emails based on provided criteria and formats them grouped by category and priority.

    Args:
        request (HttpRequest): The HTTP request object containing JSON data with filtering parameters.

    JSON Body:
        Mandatory params:

            category (str): The category of emails to filter
            resultPerPage (int): Number of results per page (must be between 25 and 100)

        Optional filters:
            sort (str): Sorting order ("asc" for ascending, "desc" for descending). Default is "asc".
            emailProvider (list[str]): List of email providers to filter by.
            subject (str): Keyword to filter by email subject.
            senderEmail (str): Keyword to filter by sender's email.
            senderName (str): Keyword to filter by sender's name.
            CCEmails (list[str]): List of email addresses to filter by CC recipients.
            CCNames (list[str]): List of names to filter by CC recipients.
            emailAddresses (list[str]): List of email addresses to filter by any associated email.
            read (bool): Filter by read/unread status.
            sentDate (datetime): Filter by sent date (emails sent on or after this date).
            readDate (datetime): Filter by read date (emails read on or after this date).
            answer (list[str]): Filter by answer status.
            relevance (list[str]): Filter by relevance status.
            priority (list[str]): Filter by priority status.
            hasAttachments (bool): Filter by emails with attachments.
            spam (bool): Filter by spam status.
            scam (bool): Filter by scam status.
            newsletter (bool): Filter by newsletter status.
            notification (bool): Filter by notification status.
            meeting (bool): Filter by meeting status.

    Returns:
        Response: JSON response with the following structure:
            {
                "count": int,  # Total number of emails matching the filters.
                "data": dict,  # Filtered and formatted email data grouped by category and priority, limited to max results.
                "ids": list[int]  # List of email IDs matching the filters.
            }
    """
    try:
        parameters: dict = json.loads(request.body)
        category: str = parameters["category"]
        result_per_page: int = parameters["resultPerPage"]
        sort: str = parameters.get("sort", "asc")
        if not 25 <= result_per_page <= 100:
            return Response(
                {
                    "error": "resultPerPage must be an integer between 25 and 100 included"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the user from the request
        user = 1  # leave it hardcoded for testing

        filters = {"user": user, "answer_later": False}

        category_obj = Category.objects.get(name=category)
        filters["category"] = category_obj

        # List of boolean fields we want to filter
        boolean_fields = [
            "scam",
            "spam",
            "newsletter",
            "notification",
            "meeting",
            "read",
            "hasAttachments",
        ]
        for field in boolean_fields:
            if field in parameters:
                filters[field] = parameters[field]

        # Additional filters
        if "priority" in parameters:
            filters["priority__in"] = parameters["priority"]
        if "emailProvider" in parameters:
            filters["email_provider__in"] = parameters["emailProvider"]
        if "subject" in parameters:
            filters["subject__icontains"] = parameters["subject"]
        if "senderEmail" in parameters:
            filters["sender__email__icontains"] = parameters["senderEmail"]
        if "senderName" in parameters:
            filters["sender__name__icontains"] = parameters["senderName"]
        if "sentDate" in parameters:
            filters["date__gte"] = parameters["sentDate"]
        if "readDate" in parameters:
            filters["read_date__gte"] = parameters["readDate"]
        if "answer" in parameters:
            filters["answer__in"] = parameters["answer"]
        if "relevance" in parameters:
            filters["relevance__in"] = parameters["relevance"]
        if "emailAddresses" in parameters:
            social_apis = SocialAPI.objects.filter(
                email__in=parameters["emailAddresses"], user=user
            )
            filters["social_api__in"] = social_apis
        if "CCEmails" in parameters:
            filters["cc_senders__email__in"] = parameters["CCEmails"]
        if "CCNames" in parameters:
            filters["cc_senders__name__in"] = parameters["CCNames"]

        # Make the query
        queryset = Email.objects.filter(**filters)
        rule_id_subquery = Rule.objects.filter(
            sender=OuterRef("sender"), user=user
        ).values("id")[:1]
        queryset = queryset.annotate(
            has_rule=Exists(rule_id_subquery), rule_id=Subquery(rule_id_subquery)
        )
        # Apply sorting
        if sort == "asc":
            queryset = queryset.order_by("-date")
        else:
            queryset = queryset.order_by("date")

        email_count = queryset.count()
        email_ids = []
        formatted_data = defaultdict(lambda: defaultdict(list))
        nb_email_treated = 0

        current_datetime_utc = timezone.now()
        for email in queryset:
            if email.read_date:
                delta_time = current_datetime_utc - email.read_date

                # Delete read email older than 1 week
                if delta_time > datetime.timedelta(weeks=1):
                    email.delete()
                    continue

            if nb_email_treated < result_per_page:
                email_data = {
                    "id": email.id,
                    "id_provider": email.provider_id,
                    "subject": email.subject,
                    "sender": {
                        "email": email.sender.email,
                        "name": email.sender.name,
                    },
                    "short_summary": email.short_summary,
                    "one_line_summary": email.one_line_summary,
                    "cc": [
                        {"email": cc.email, "name": cc.name}
                        for cc in email.cc_senders.all()
                    ],
                    "bcc": [
                        {"email": bcc.email, "name": bcc.name}
                        for bcc in email.bcc_senders.all()
                    ],
                    "read": email.read,
                    "rule": {
                        "has_rule": email.has_rule,
                        "rule_id": email.rule_id,
                    },
                    "answer_later": email.answer_later,
                    "has_attachments": email.has_attachments,
                    "attachments": [
                        {
                            "attachmentName": attachment.name,
                            "attachmentId": attachment.id_api,
                        }
                        for attachment in email.attachments.all()
                    ],
                    "sent_date": email.date.date() if email.date else None,
                    "sent_time": email.date.strftime("%H:%M") if email.date else None,
                    "answer": email.answer,
                    "relevance": email.relevance,
                    "priority": email.priority,
                    "flags": {
                        "spam": email.spam,
                        "scam": email.scam,
                        "newsletter": email.newsletter,
                        "notification": email.notification,
                        "meeting": email.meeting,
                    },
                }
                formatted_data[email.category.name][email.priority].append(email_data)
                nb_email_treated += 1

            email_ids.append(email.id)

        return Response(
            {"count": email_count, "data": formatted_data, "ids": email_ids},
            status=status.HTTP_200_OK,
        )
    except Category.DoesNotExist:
        return Response(
            {"error": "Invalid category"}, status=status.HTTP_400_BAD_REQUEST
        )
    except KeyError:
        return Response(
            {"error": "Invalid JSON keys in request body"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except TypeError:
        return Response(
            {"error": "resultPerPage must be an integer"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON in request body"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def get_user_emails_with_filter(request: HttpRequest) -> Response:
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
        print(f"Error: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
