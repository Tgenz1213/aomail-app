"""
Handles user statistics computation and retrieval.

Endpoints:
- ✅ get_statistics: Returns required statistics of the user based on specified parameters.
- ✅ get_combined_statistics:  Retrieves combined statistics for the selected emails.
"""

import json
import logging
from django.http import HttpRequest
from rest_framework import status
from django.db.models import Count, Min, Max, Avg, F, Window, DateField
from django.db.models.functions import TruncDate, TruncHour, FirstValue, Cast
from aomail.models import Email, SocialAPI, Statistics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from aomail.utils.security import subscription
from aomail.constants import (
    ALLOW_ALL,
    ANSWER_REQUIRED,
    GOOGLE,
    HIGHLY_RELEVANT,
    IMPORTANT,
    INFORMATIVE,
    MICROSOFT,
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
from aomail.email_providers.google import profile as profile_google
from aomail.email_providers.microsoft import profile as profile_microsoft
from aomail.email_providers.imap import profile as profile_imap


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


@api_view(["POST"])
@subscription(ALLOW_ALL)
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


def get_period_duration(period: str) -> int:
    """
    Get the duration in days for a given period.

    Args:
        period (str): The period identifier (e.g., "24Hours", "7Days")

    Returns:
        int: Number of days for the period
    """
    period_mapping = {
        "24Hours": 1,
        "7Days": 7,
        "30Days": 30,
        "3Months": 90,
        "6Months": 180,
        "1year": 365,
        "5years": 1825,
    }
    return period_mapping.get(period, 0)


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
            period_days = get_period_duration(period)

            stat_result[stat_name]["periods"][period] = get_period_stats_values(
                stats, user, period_days, stat_name, now)

    return stat_result


def get_period_stats_values(
    stats: list,
    user: User,
    period_days: int,
    stat_name: str,
    now: datetime
) -> dict:
    """Returns a dict with the given stats as keys"""
    result = {}

    min = Email.objects.filter(user=user).count()
    max = 0
    all_counts = []
    date_cursor = user.date_joined

    while date_cursor + timedelta(period_days) <= now:
        email_queryset = get_filtered_queryset(
            Email.objects.filter(
                user=user,
                date__range=(date_cursor, date_cursor +
                             timedelta(period_days))
            ),
            stat_name,
        )

        count = email_queryset.count()
        all_counts.append(count)

        if count < min:
            min = count
        if count > max:
            max = count

        date_cursor += timedelta(period_days)

    if "min" in stats:
        result["min"] = min
    if "max" in stats:
        result["max"] = max
    if "avg" in stats:
        result["avg"] = sum(all_counts) / len(all_counts) + 1e-4

    return result


def get_filtered_queryset(queryset: QuerySet, stat_name: str) -> QuerySet[Email]:
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
        "monday": now - timedelta(days=now.weekday()),
        "mtd": now.replace(day=1, hour=0, minute=0, second=0, microsecond=0),
        "ytd": now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0),
    }

 
def get_min_value(queryset: QuerySet, period_days: int) -> int:
    """
    Get the minimum count for the specified period size.

    Args:
        queryset (QuerySet): The queryset of Email objects to analyze
        period_days (int): The size of each period in days

    Returns:
        int: The minimum count within any period of the specified size
    """
    if period_days == 1:
        # For 24 hours periods, group by hour
        result = (
            queryset.annotate(period=TruncHour("date"))
            .values("period")
            .annotate(count=Count("id"))
            .aggregate(min_count=Min("count"))
        )
    else:
        # For other periods, group by day and calculate min per period_days
        result = (
            queryset.annotate(period=TruncDate("date"))
            .values("period")
            .annotate(count=Count("id"))
            .values("period", "count")
            .order_by("period")
        )

        # Group into periods of period_days and find minimum
        counts = []
        current_count = 0
        current_days = 0

        for entry in result:
            current_count += entry["count"]
            current_days += 1

            if current_days >= period_days:
                counts.append(current_count)
                current_count = 0
                current_days = 0

        # Add the last period if it exists
        if current_count > 0:
            counts.append(current_count)

        return min(counts) if counts else 0

    return result["min_count"] or 0


def get_max_value(queryset: QuerySet, period_days: int) -> int:
    """
    Get the maximum count for the specified period size.

    Args:
        queryset (QuerySet): The queryset of Email objects to analyze
        period_days (int): The size of each period in days

    Returns:
        int: The maximum count within any period of the specified size
    """
    if period_days == 1:
        result = (
            queryset.annotate(period=TruncHour("date"))
            .values("period")
            .annotate(count=Count("id"))
            .aggregate(max_count=Max("count"))
        )
    else:
        # For other periods, group by day and calculate max per period_days
        result = (
            queryset.annotate(period=TruncDate("date"))
            .values("period")
            .annotate(count=Count("id"))
            .values("period", "count")
            .order_by("period")
        )

        # Group into periods of period_days and find maximum
        counts = []
        current_count = 0
        current_days = 0

        for entry in result:
            current_count += entry["count"]
            current_days += 1

            if current_days >= period_days:
                counts.append(current_count)
                current_count = 0
                current_days = 0

        # Add the last period if it exists
        if current_count > 0:
            counts.append(current_count)

        return max(counts) if counts else 0

    return result["max_count"] or 0


def get_avg_value(queryset: QuerySet, period_days: int) -> float:
    """
    Get the average count for the specified period size.

    Args:
        queryset (QuerySet): The queryset of Email objects to analyze
        period_days (int): The size of each period in days

    Returns:
        float: The average count per period of the specified size
    """
    if period_days == 1:
        result = (
            queryset.annotate(period=TruncHour("date"))
            .values("period")
            .annotate(count=Count("id"))
            .aggregate(avg_count=Avg("count"))
        )
    else:
        # For other periods, group by day and calculate avg per period_days
        result = (
            queryset.annotate(period=TruncDate("date"))
            .values("period")
            .annotate(count=Count("id"))
            .values("period", "count")
            .order_by("period")
        )

        # Group into periods of period_days and calculate average
        counts = []
        current_count = 0
        current_days = 0

        for entry in result:
            current_count += entry["count"]
            current_days += 1

            if current_days >= period_days:
                counts.append(current_count)
                current_count = 0
                current_days = 0

        # Add the last period if it exists
        if current_count > 0:
            counts.append(current_count)

        return float(sum(counts) / len(counts)) if counts else 0.0

    return float(result["avg_count"] or 0)



@api_view(["POST"])
@subscription(ALLOW_ALL)
def get_combined_statistics(request) -> Response:
    """
    Retrieve combined statistics for the selected emails.

    Args:
        request (HttpRequest): The request object containing user and email selection.

    Returns:
        Response: A JSON response with Aomail and email provider data.
    """
    try:
        user = request.user
        parameters: dict = json.loads(request.body)
        emails_selected: list = parameters["emailsSelected"]

        social_apis = SocialAPI.objects.filter(
            user=user, email__in=emails_selected)

        aomail_data = get_aomail_data(social_apis)
        email_providers_data = get_email_providers_data(social_apis)

        return Response(
            {"aomailData": aomail_data, "emailProvidersData": email_providers_data},
            status=status.HTTP_200_OK,
        )
    except json.JSONDecodeError:
        LOGGER.error("Invalid JSON format in request body.")
        return Response(
            {"error": "Invalid JSON format."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except SocialAPI.DoesNotExist:
        LOGGER.error("Social API not found for user ID {user.id}.")
        return Response(
            {"error": "Social API not found."},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        LOGGER.error(
            f"Error in get statistics for user ID {user.id}: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def get_aomail_data(social_apis: list[SocialAPI]) -> dict:
    """
    Retrieve Aomail data statistics for the given social APIs.

    Args:
        social_apis (list[SocialAPI]): List of social API instances.

    Returns:
        dict: A dictionary containing Aomail data statistics.
    """
    num_emails_received = Email.objects.filter(
        social_api__in=social_apis).count()
    num_emails_read = Email.objects.filter(
        social_api__in=social_apis, read=True
    ).count()
    num_emails_archived = Email.objects.filter(
        social_api__in=social_apis, archive=True
    ).count()
    num_emails_reply_later = Email.objects.filter(
        social_api__in=social_apis, answer_later=True
    ).count()

    return {
        "nbEmailsReceived": num_emails_received,
        "nbEmailsRead": num_emails_read,
        "nbEmailsArchived": num_emails_archived,
        "nbEmailsReplyLater": num_emails_reply_later,
    }


def get_email_providers_data(social_apis: list[SocialAPI]) -> dict:
    """
    Retrieve email provider data statistics for the given social APIs.

    Args:
        social_apis (list[SocialAPI]): List of social API instances.

    Returns:
        dict: A dictionary containing email provider data statistics.
    """
    sum_data = {
        "nbEmailsReceived": 0,
        "nbEmailsRead": 0,
        "nbEmailsArchived": 0,
        "nbEmailsStarred": 0,
        "nbEmailsSent": 0,
    }
    for social_api in social_apis:
        data = {}
        if social_api.type_api == GOOGLE and not social_api.imap_config:
            data = profile_google.get_data(social_api)
        elif social_api.type_api == MICROSOFT and not social_api.imap_config:
            data = profile_microsoft.get_data(social_api)
        elif social_api.imap_config:
            data = profile_imap.get_data(social_api)
        if data:
            sum_data["nbEmailsReceived"] += data["num_emails_received"]
            sum_data["nbEmailsRead"] += data["num_emails_read"]
            sum_data["nbEmailsArchived"] += data["num_emails_archived"]
            sum_data["nbEmailsStarred"] += data["num_emails_starred"]
            sum_data["nbEmailsSent"] += data["num_emails_sent"]

    return sum_data
