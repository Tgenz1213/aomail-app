"""
TODO: Everything about stats data bout a suer


Endpoints:
- ⚒️ get_statistics: ...
"""

import json
import logging
import re
from django.http import HttpRequest
from rest_framework import status
from django.db.models import Count, Min, Max, Avg
from MailAssistant.models import Email, Statistics
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from MailAssistant.utils.security import subscription
from MailAssistant.constants import ANSWER_REQUIRED, FREE_PLAN, HIGHLY_RELEVANT, IMPORTANT, INFORMATIVE, MIGHT_REQUIRE_ANSWER, NO_ANSWER_REQUIRED, NOT_RELEVANT, POSSIBLY_RELEVANT, USELESS
from django.contrib.auth.models import User
from django.utils import timezone

######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


def camel_to_snake(name):
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    return pattern.sub("_", name).lower()


# START OF DOC
# allowed keys
# general_stats = {
#     "nbEmailsReceived": statistics.nb_emails_received,
#     "nbEmailsImportant": statistics.nb_emails_important,
#     "nbEmailsInformative": statistics.nb_emails_informative,
#     "nbEmailsUseless": statistics.nb_emails_useless,
#     "nbTokensInput": statistics.nb_tokens_input,
#     "nbTokensOutput": statistics.nb_tokens_output,
#     "nbAnswerRequired": statistics.nb_answer_required,
#     "nbMightRequireAnswer": statistics.nb_might_require_answer,
#     "nbNoAnswerRequired": statistics.nb_no_answer_required,
#     "nbHighlyRelevant": statistics.nb_highly_relevant,
#     "nbPossiblyRelevant": statistics.nb_possibly_relevant,
#     "nbNotRelevant": statistics.nb_not_relevant,
#     "nbSpam": statistics.nb_spam,
#     "nbScam": statistics.nb_scam,
#     "nbNewsletter": statistics.nb_newsletter,
#     "nbNotification": statistics.nb_notification,
#     "nbMeeting": statistics.nb_meeting,
# nbTokensInput
# nbTokensOutput
# }



# @api_view(["POST"])
# @subscription([FREE_PLAN])
@api_view(["POST"])
@permission_classes([AllowAny])
def get_statistics(request: HttpRequest) -> Response:
    try:
        user_id = 1
        user = User.objects.get(id=user_id)
        parameters: dict = json.loads(request.body)
        statistics = Statistics.objects.get(user=user)

        computed_stats = compute_statistics(statistics, parameters)

        return Response(
            {"stats": computed_stats, "message": "Statistics computed successfully"},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        LOGGER.error(f"Error in get statistics for user ID {user_id}: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def get_time_ranges(now):
    return {
        "today": now.replace(hour=0, minute=0, second=0, microsecond=0),
        "24Hours": now - timedelta(hours=24),
        "monday": now - timedelta(days=now.weekday()),
        "7Days": now - timedelta(days=7),
        "mtd": now.replace(day=1, hour=0, minute=0, second=0, microsecond=0),
        "30Days": now - timedelta(days=30),
        "3Months": now - timedelta(days=90),
        "6Months": now - timedelta(days=180),
        "ytd": now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0),
        "1year": now - timedelta(days=365),
        "5years": now - timedelta(days=1825),
    }
def compute_statistics(statistics, parameters):
    computed_stats = {}
    user = statistics.user
    now = timezone.now()
    time_ranges = get_time_ranges(now)

    for stat_name, stat_config in parameters.items():
        snake_case_stat_name = camel_to_snake(stat_name)
        computed_stats[stat_name] = {}

        if stat_name in ["nbTokensInput", "nbTokensOutput"]:
            count = getattr(statistics, snake_case_stat_name)
            for stat in stat_config["statistics"]:
                if stat == "count":
                    computed_stats[stat_name]["count"] = count
                elif stat == "avg":
                    nb_emails_received = statistics.nb_emails_received
                    computed_stats[stat_name]["avg"] = count / nb_emails_received if nb_emails_received > 0 else 0
        else:
            if "since" in stat_config:
                computed_stats[stat_name]["since"] = {}
                for period in stat_config["since"]:
                    if period == "join":
                        computed_stats[stat_name]["since"]["join"] = getattr(statistics, snake_case_stat_name)
                    else:
                        start_date = time_ranges[period]
                        email_queryset = get_filtered_queryset(Email.objects.filter(user=user, date__gte=start_date, date__lte=now), stat_name)
                        count = email_queryset.count()
                        computed_stats[stat_name]["since"][period] = count

            if "periods" in stat_config:
                computed_stats[stat_name]["periods"] = {}
                for period, stats in stat_config["periods"].items():
                    computed_stats[stat_name]["periods"][period] = {}
                    start_date = time_ranges[period]
                    email_queryset = get_filtered_queryset(Email.objects.filter(user=user, date__gte=start_date, date__lte=now), stat_name)

                    for stat in stats:
                        if stat == "min":
                            min_value = get_min_value(email_queryset, start_date, now)
                            computed_stats[stat_name]["periods"][period]["min"] = min_value
                        elif stat == "max":
                            max_value = get_max_value(email_queryset, start_date, now)
                            computed_stats[stat_name]["periods"][period]["max"] = max_value
                        elif stat == "count":
                            count = email_queryset.count()
                            computed_stats[stat_name]["periods"][period]["count"] = count
                        elif stat == "avg":
                            avg_per_day = email_queryset.count() / ((now - start_date).days + 1)
                            computed_stats[stat_name]["periods"][period]["avg"] = avg_per_day

    return computed_stats

def get_filtered_queryset(queryset, stat_name):
    match stat_name:
        case "nbMightRequireAnswer":
            return queryset.filter(answer=MIGHT_REQUIRE_ANSWER)
        case "nbEmailsReceived":
            return queryset
        case "nbAnswerRequired":
            return queryset.filter(answer=ANSWER_REQUIRED)
        case "nbNoAnswerRequired":
            return queryset.filter(answer=NO_ANSWER_REQUIRED)
        case "nbHighlyRelevant":
            return queryset.filter(relevance=HIGHLY_RELEVANT)
        case "nbPossiblyRelevant":
            return queryset.filter(relevance=POSSIBLY_RELEVANT)
        case "nbNotRelevant":
            return queryset.filter(relevance=NOT_RELEVANT)
        case "nbImportant":
            return queryset.filter(priority=IMPORTANT)
        case "nbInformative":
            return queryset.filter(priority=INFORMATIVE)
        case "nbUseless":
            return queryset.filter(priority=USELESS)
        case "nbScam":
            return queryset.filter(scam=True)
        case "nbSpam":
            return queryset.filter(spam=True)
        case "nbNewsletter":
            return queryset.filter(newsletter=True)
        case "nbNotification":
            return queryset.filter(notification=True)
        case "nbMeeting":
            return queryset.filter(meeting=True)
        case "nbHasAttachments":
            return queryset.filter(has_attachments=True)
        case "nbRead":
            return queryset.filter(read=True)
        case "nbUnread":
            return queryset.filter(read=False)
        case _:
            return queryset
        
    
def get_min_value(queryset, start_date, end_date):
    date_range = (end_date - start_date).days + 1
    daily_counts = [queryset.filter(date__date=start_date.date() + timedelta(days=i)).count() for i in range(date_range)]
    return min(daily_counts) if daily_counts else 0

def get_max_value(queryset, start_date, end_date):
    date_range = (end_date - start_date).days + 1
    daily_counts = [queryset.filter(date__date=start_date.date() + timedelta(days=i)).count() for i in range(date_range)]
    return max(daily_counts) if daily_counts else 0