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
from django.db.models import Count, Min, Max
from MailAssistant.models import Email, Statistics
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from MailAssistant.utils.security import subscription
from MailAssistant.constants import FREE_PLAN
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
# TODO: camelCase
# nb_tokens_input
# nb_tokens_output
# }

# FOR EACH DICT
# "statistics": [
#     "avg",
#     "min",
#     "max"
# ] is optionnal

# All allowed keys + there allowed subkeys (they are all optionnal)
# "day": {
#             ,
#             "last24Hours": true,
#             "sinceToday": true
#         },
#         "week": {
#             "statistics": [
#                 "avg",
#                 "max"
#             ],
#             "last7Days": true,
#             "sinceMonday": true
#         },
#         "month": {
#             "statistics": [
#                 "min"
#             ],
#             "last30Days": true,
#             "sinceThisMonth": true
#         },
#         "3Months": {
#             "statistics": [
#                 "avg"
#             ],
#             "last3Months": true
#         },
#         "6Months": {
#             "statistics": [
#                 "max"
#             ],
#             "last6Months": true
#         },
#         "year": {
#             "statistics": [
#                 "min"
#             ],
#             "last12Months": true,
#             "ytd": true
#         },
#         "5years": {
#             "statistics": [
#                 "min"
#             ],
#             "last5Years": true
#         },
#         "sinceJoined": true


# @api_view(["POST"])
# @subscription([FREE_PLAN])
@api_view(["POST"])
@permission_classes([AllowAny])
def get_statistics(request: HttpRequest) -> Response:
    try:
        # user = request.user
        user_id = 1
        user = User.objects.get(id=user_id)

        parameters: dict = json.loads(request.body)
        statistics = Statistics.objects.get(user=user)

        now = timezone.now()
        time_ranges = {
            "last24Hours": now - timedelta(hours=24),
            "today": now.replace(hour=0, minute=0, second=0, microsecond=0),
            "within7Days": now - timedelta(days=7),
            "sinceMonday": now - timedelta(days=now.weekday()),
            "last30Days": now - timedelta(days=30),
            "thisMonth": now.replace(day=1, hour=0, minute=0, second=0, microsecond=0),
            "last12Months": now - timedelta(days=365),
            "ytd": now.replace(
                month=1, day=1, hour=0, minute=0, second=0, microsecond=0
            ),
            "last3Months": now - timedelta(days=90),
            "last6Months": now - timedelta(days=180),
            "last5Years": now - timedelta(days=1825),
            "sinceJoined": user.date_joined,
        }

        computed_stats = {}

        for stat_name, stat_config in parameters.items():
            computed_stats[stat_name] = {}

            snake_case_stat_name = camel_to_snake(stat_name)

            if stat_name in ["nbTokensInput", "nbTokensOutput"]:
                computed_stats[stat_name]["count"] = getattr(
                    statistics, snake_case_stat_name
                )
            else:
                for period, period_config in stat_config.items():
                    if period == "sinceJoined":
                        computed_stats[stat_name]["sinceJoined"] = getattr(
                            statistics, snake_case_stat_name
                        )
                        continue

                    computed_stats[stat_name][period] = {}

                    for time_range, include in period_config.items():
                        if (
                            include
                            and time_range != "statistics"
                            and time_range in time_ranges
                        ):
                            queryset = Email.objects.filter(
                                user=user, date__gte=time_ranges[time_range]
                            )

                            if stat_name == "nbEmailsReceived":
                                count = queryset.count()
                            elif stat_name == "nbEmailsImportant":
                                count = queryset.filter(priority="important").count()
                            elif stat_name == "nbEmailsInformative":
                                count = queryset.filter(priority="informative").count()
                            elif stat_name == "nbEmailsUseless":
                                count = queryset.filter(priority="useless").count()
                            elif stat_name == "nbAnswerRequired":
                                count = queryset.filter(answer="required").count()
                            elif stat_name == "nbMightRequireAnswer":
                                count = queryset.filter(answer="might_require").count()
                            elif stat_name == "nbNoAnswerRequired":
                                count = queryset.filter(answer="not_required").count()
                            elif stat_name == "nbHighlyRelevant":
                                count = queryset.filter(
                                    relevance="highly_relevant"
                                ).count()
                            elif stat_name == "nbPossiblyRelevant":
                                count = queryset.filter(
                                    relevance="possibly_relevant"
                                ).count()
                            elif stat_name == "nbNotRelevant":
                                count = queryset.filter(
                                    relevance="not_relevant"
                                ).count()
                            elif stat_name in [
                                "nbSpam",
                                "nbScam",
                                "nbNewsletter",
                                "nbNotification",
                                "nbMeeting",
                            ]:
                                count = queryset.filter(
                                    **{snake_case_stat_name[3:]: True}
                                ).count()
                            else:
                                count = getattr(statistics, snake_case_stat_name, 0)

                            computed_stats[stat_name][period][time_range] = count

                    if "statistics" in period_config:
                        stats = period_config["statistics"]
                        values = [
                            v
                            for k, v in computed_stats[stat_name][period].items()
                            if k != "statistics"
                        ]
                        if values:
                            if "avg" in stats:
                                computed_stats[stat_name][period]["avg"] = sum(
                                    values
                                ) / len(values)
                            if "min" in stats:
                                computed_stats[stat_name][period]["min"] = min(values)
                            if "max" in stats:
                                computed_stats[stat_name][period]["max"] = max(values)

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
