"""
Handles user statistics computation and retrieval.

Endpoints:
- ✅ get_statistics: Returns required statistics of the user based on specified parameters.
"""

import json
import logging
from django.http import HttpRequest
from rest_framework import status
from django.db.models import Count, Min, Max, Avg
from django.db.models.functions import TruncDate
from aomail.models import Email, Statistics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from aomail.utils.security import subscription
from aomail.constants import (
    ANSWER_REQUIRED,
    ALLOWED_PLANS,
    HIGHLY_RELEVANT,
    IMPORTANT,
    INACTIVE,
    INFORMATIVE,
    MIGHT_REQUIRE_ANSWER,
    NO_ANSWER_REQUIRED,
    NOT_RELEVANT,
    POSSIBLY_RELEVANT,
    USELESS,
)
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import QuerySet
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from aomail.utils.email_processing import camel_to_snake


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


@api_view(["POST"])
@subscription(ALLOWED_PLANS + [INACTIVE])
def get_statistics(request: HttpRequest) -> Response:
    """
    Compute and return statistics for a user based on provided parameters.

    Args:
        request (HttpRequest): HTTP request with JSON body containing parameters.

    Returns:
        Response: Computed statistics and success message, or error message.

    JSON Body (all optional):
        {
            "statName1": {
                "since": ["join", "today", "monday", "mtd", "ytd"],
                "periods": {
                    "24Hours": ["min", "max"],
                    "7Days": ["avg"],
                    ...
                }
            },
            "statName2": { ... },
            ...
        }

    Allowed statName keys:
        nbMightRequireAnswer, nbEmailsReceived, nbAnswerRequired, nbNoAnswerRequired,
        nbHighlyRelevant, nbPossiblyRelevant, nbNotRelevant, nbEmailsImportant,
        nbEmailsInformative, nbEmailsUseless, nbScam, nbSpam, nbNewsletter, nbNotification,
        nbMeeting

    "since" options: join, today, monday, mtd, ytd
    "periods" options: 24Hours, 7Days, 30Days, 3Months, 6Months, 1year, 5years
    For each period: avg, min, max (any combination)
    """
    try:
        user = request.user
        parameters: dict = json.loads(request.body)
        statistics = Statistics.objects.get(user=user)

        computed_stats = compute_statistics(statistics, parameters)

        return Response(
            {"stats": computed_stats, "message": "Statistics computed successfully"},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        LOGGER.error(f"Error in get statistics for user ID {user.id}: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def compute_statistics(statistics: Statistics, parameters: dict) -> dict:
    """
    Compute various statistics based on the provided parameters using threading.

    Args:
        statistics (Statistics): A Statistics object associated with a user.
        parameters (dict): A dictionary of parameters specifying which statistics
                           to compute and for what time periods.

    Returns:
        dict: A dictionary containing the computed statistics, organized by
              statistic name, time period, and metric type.
    """
    computed_stats = {}
    user = statistics.user
    now = timezone.now()
    time_ranges = get_time_ranges(now)

    with ThreadPoolExecutor(max_workers=min(len(parameters), 10)) as executor:
        futures = [
            executor.submit(
                compute_stat, statistics, user, stat_name, stat_config, time_ranges, now
            )
            for stat_name, stat_config in parameters.items()
        ]

        for future in as_completed(futures):
            result = future.result()
            computed_stats.update(result)

    return computed_stats


def compute_stat(
    statistics: Statistics,
    user: User,
    stat_name: str,
    stat_config: dict,
    time_ranges: dict,
    now: datetime,
) -> dict:
    """
    Compute statistics for a single stat_name and its configuration.

    Args:
        statistics (Statistics): A Statistics object associated with a user.
        user (User): The user for whom statistics are being computed.
        stat_name (str): The name of the statistic being computed.
        stat_config (dict): Configuration for the statistic.
        time_ranges (dict): Pre-computed time ranges.
        now (datetime): The current time.

    Returns:
        dict: A dictionary containing the computed statistics for the given stat_name.
    """
    snake_case_stat_name = camel_to_snake(stat_name)
    stat_result = {stat_name: {}}

    if "since" in stat_config:
        stat_result[stat_name]["since"] = {}
        for period in stat_config["since"]:
            if period == "join":
                stat_result[stat_name]["since"]["join"] = getattr(
                    statistics, snake_case_stat_name
                )
            else:
                start_date = time_ranges[period]
                email_queryset = get_filtered_queryset(
                    Email.objects.filter(
                        user=user, date__gte=start_date, date__lte=now
                    ),
                    stat_name,
                )
                count = email_queryset.count()
                stat_result[stat_name]["since"][period] = count

    if "periods" in stat_config:
        stat_result[stat_name]["periods"] = {}
        for period, stats in stat_config["periods"].items():
            stat_result[stat_name]["periods"][period] = {}
            start_date = time_ranges[period]
            email_queryset = get_filtered_queryset(
                Email.objects.filter(user=user, date__gte=start_date, date__lte=now),
                stat_name,
            )

            for stat in stats:
                if stat == "min":
                    min_value = get_min_value(email_queryset, start_date, now)
                    stat_result[stat_name]["periods"][period]["min"] = min_value
                elif stat == "max":
                    max_value = get_max_value(email_queryset, start_date, now)
                    stat_result[stat_name]["periods"][period]["max"] = max_value
                elif stat == "count":
                    count = email_queryset.count()
                    stat_result[stat_name]["periods"][period]["count"] = count
                elif stat == "avg":
                    avg_value = get_avg_value(email_queryset, start_date, now)
                    stat_result[stat_name]["periods"][period]["avg"] = avg_value

    return stat_result


def get_filtered_queryset(queryset: QuerySet, stat_name: str) -> QuerySet:
    """
    Filter a queryset based on the given statistic name.

    Args:
        queryset (QuerySet): The initial queryset to be filtered.
        stat_name (str): The name of the statistic, which determines how the
                         queryset will be filtered.

    Returns:
        QuerySet: A filtered queryset based on the provided stat_name.
    """
    match stat_name:
        case "nbEmailsReceived":
            return queryset
        case "nbAnswerRequired":
            return queryset.filter(answer=ANSWER_REQUIRED)
        case "nbMightRequireAnswer":
            return queryset.filter(answer=MIGHT_REQUIRE_ANSWER)
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
        case _:
            return queryset


def get_time_ranges(now: datetime) -> dict:
    """
    Generate a dictionary of time ranges based on the current time.

    Args:
        now (datetime): The current date and time.

    Returns:
        dict: A dictionary where keys are time range names and values are datetime objects
              representing the start of each time range.
    """
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


def get_min_value(queryset: QuerySet, start_date: datetime, end_date: datetime) -> int:
    """
    Get the minimum daily count from a queryset within a date range using Django's Min aggregation.

    Args:
        queryset (QuerySet): The queryset of Email objects to analyze.
        start_date (datetime): The start date of the range to consider.
        end_date (datetime): The end date of the range to consider.

    Returns:
        int: The minimum daily count of emails within the date range. Returns 0 if no emails are found.
    """
    result = (
        queryset.filter(date__range=(start_date, end_date))
        .annotate(truncated_date=TruncDate("date"))
        .values("truncated_date")
        .annotate(count=Count("id"))
        .aggregate(min_count=Min("count"))
    )
    return result["min_count"] or 0


def get_max_value(queryset: QuerySet, start_date: datetime, end_date: datetime) -> int:
    """
    Get the maximum daily count from a queryset within a date range using Django's Max aggregation.

    Args:
        queryset (QuerySet): The queryset of Email objects to analyze.
        start_date (datetime): The start date of the range to consider.
        end_date (datetime): The end date of the range to consider.

    Returns:
        int: The maximum daily count of emails within the date range. Returns 0 if no emails are found.
    """
    result = (
        queryset.filter(date__range=(start_date, end_date))
        .annotate(truncated_date=TruncDate("date"))
        .values("truncated_date")
        .annotate(count=Count("id"))
        .aggregate(max_count=Max("count"))
    )
    return result["max_count"] or 0


def get_avg_value(
    queryset: QuerySet, start_date: datetime, end_date: datetime
) -> float:
    """
    Get the average daily count from a queryset within a date range using Django's Avg aggregation.

    Args:
        queryset (QuerySet): The queryset of Email objects to analyze.
        start_date (datetime): The start date of the range to consider.
        end_date (datetime): The end date of the range to consider.

    Returns:
        float: The average daily count of emails within the date range. Returns 0 if no emails are found.
    """
    result = (
        queryset.filter(date__range=(start_date, end_date))
        .annotate(truncated_date=TruncDate("date"))
        .values("truncated_date")
        .annotate(count=Count("id"))
        .aggregate(avg_count=Avg("count"))
    )
    return result["avg_count"] or 0
