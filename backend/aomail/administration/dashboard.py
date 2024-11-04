"""
Handles the administrative dashboard views and functionalities for Aomail.

Endpoints:
- ✅ get_costs_info: Retrieve token usage statistics and compute estimated costs for input/output.
- ✅ create_superuser: Allows admin to create a new superuser account.
- ✅ search_user_info: Search and retrieve detailed statistics for a specific user.
- ✅ get_dashboard_data: Fetch overall statistics for emails, social APIs, and users in the system.
- ✅ update_admin_data: Update details (username, password, etc.) of the authenticated admin.
- ✅ delete_admin: Delete admin account.
- ✅ login: Authenticate admin user and return access token.
- ✅ update_user_info: Update information (plan, email, username) for a specified user.
"""

import json
import logging
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.db.models import Count, Case, When
from django.contrib.auth import authenticate
from datetime import timedelta
from aomail.controllers.statistics import compute_statistics
from aomail.utils.security import admin_access_required
from aomail.models import Email, SocialAPI, Statistics, Subscription
from aomail.utils import security
from aomail.constants import ALLOWED_PLANS, GOOGLE, MICROSOFT


LOGGER = logging.getLogger(__name__)


@api_view(["GET"])
@admin_access_required
def get_costs_info(request: HttpRequest) -> Response:
    """
    Get token usage stats and estimated costs.

    Returns:
        - Min/max input and output tokens.
        - Total and average tokens per user.
        - Estimated costs for input and output tokens.

    Response:
        JSON with token stats and cost estimates, or 404/500 on error.
    """
    admin = request.user
    ip = security.get_ip_with_port(request)

    LOGGER.info(
        f"Cost report requested by admin {admin.username} with ID: {admin.id} from IP: {ip}"
    )

    try:
        first_stat = Statistics.objects.first()
        if not first_stat:
            LOGGER.error(
                f"No statistics found in the database (requested by admin {admin.username}, IP: {ip})"
            )
            return Response(
                {"error": "No statistics available"}, status=status.HTTP_404_NOT_FOUND
            )

        min_nb_tokens_output, max_nb_tokens_output = (
            first_stat.nb_tokens_output,
            first_stat.nb_tokens_output,
        )
        min_nb_tokens_input, max_nb_tokens_input = (
            first_stat.nb_tokens_input,
            first_stat.nb_tokens_input,
        )

        total_nb_tokens_input = 0
        total_nb_tokens_output = 0
        user_count = User.objects.filter(is_superuser=False).count()

        if user_count == 0:
            LOGGER.error(
                f"No users found in the system (requested by admin {admin.username}, IP: {ip})"
            )
            return Response(
                {"error": "No users found in the system"},
                status=status.HTTP_404_NOT_FOUND,
            )

        for statistic in Statistics.objects.all():
            total_nb_tokens_input += statistic.nb_tokens_input
            total_nb_tokens_output += statistic.nb_tokens_output

            if statistic.nb_tokens_input > max_nb_tokens_input:
                max_nb_tokens_input = statistic.nb_tokens_input
            if statistic.nb_tokens_input < min_nb_tokens_input:
                min_nb_tokens_input = statistic.nb_tokens_input

            if statistic.nb_tokens_output > max_nb_tokens_output:
                max_nb_tokens_output = statistic.nb_tokens_output
            if statistic.nb_tokens_output < min_nb_tokens_output:
                min_nb_tokens_output = statistic.nb_tokens_output

        # Estimate costs
        estimated_cost_input = total_nb_tokens_input / 1_000_000 * 0.25
        estimated_cost_output = total_nb_tokens_output / 1_000_000 * 1.25
        total_estimated_cost = estimated_cost_input + estimated_cost_output

        # Average tokens per user
        avg_tokens_input_per_user = total_nb_tokens_input / user_count
        avg_tokens_output_per_user = total_nb_tokens_output / user_count

        # Costs per user
        avg_cost_input_per_user = avg_tokens_input_per_user / 1_000_000 * 0.25
        avg_cost_output_per_user = avg_tokens_output_per_user / 1_000_000 * 1.25
        avg_total_cost_per_user = avg_cost_input_per_user + avg_cost_output_per_user

        LOGGER.info(
            f"Report data generated successfully by admin {admin.username} (ID: {admin.id}) from IP: {ip}"
        )
        return Response(
            {
                "costs": {
                    "minTokensOutput": min_nb_tokens_output,
                    "maxTokensOutput": max_nb_tokens_output,
                    "minTokensInput": min_nb_tokens_input,
                    "maxTokensInput": max_nb_tokens_input,
                    "totalTokensInput": total_nb_tokens_input,
                    "totalTokensOutput": total_nb_tokens_output,
                    "totalEstimatedCostInput": estimated_cost_input,
                    "totalEstimatedCostOutput": estimated_cost_output,
                    "totalEstimatedCost": total_estimated_cost,
                    "averageTokensInputPerUser": avg_tokens_input_per_user,
                    "averageTokensOutputPerUser": avg_tokens_output_per_user,
                    "averageCostInputPerUser": avg_cost_input_per_user,
                    "averageCostOutputPerUser": avg_cost_output_per_user,
                    "averageTotalCostPerUser": avg_total_cost_per_user,
                }
            },
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        LOGGER.error(
            f"Error while generating cost report (admin {admin.username}, IP: {ip}): {str(e)}"
        )
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@admin_access_required
def create_superuser(request: HttpRequest) -> Response:
    """
    Creates a superuser account.

    Parameters:
        request (HttpRequest): The HTTP request object containing the following parameters in the POST data:
            - username (str): The username for the new superuser account.
            - password (str): The password for the new superuser account.

    Returns:
        Response: JSON response indicating success or failure of superuser creation.
    """
    admin = request.user
    ip = security.get_ip_with_port(request)

    LOGGER.info(
        f"Superuser creation request received from admin {admin.username} with ID: {admin.id} from IP: {ip}"
    )

    try:
        parameters: dict = json.loads(request.body)
        username = parameters.get("username")
        password = parameters.get("password")

        if not username:
            LOGGER.error(
                f"Username missing in superuser creation request by admin {admin.username} from IP: {ip}"
            )
            return Response(
                {"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not password:
            LOGGER.error(
                f"Password missing in superuser creation request by admin {admin.username} from IP: {ip}"
            )
            return Response(
                {"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            LOGGER.error(
                f"Superuser creation failed: Username '{username}' already exists (requested by admin {admin.username} from IP: {ip})"
            )
            return Response(
                {"error": "Username already taken"}, status=status.HTTP_409_CONFLICT
            )

        User.objects.create_superuser(username=username, password=password)

        LOGGER.info(
            f"Superuser '{username}' successfully created by admin {admin.username} from IP: {ip}"
        )
        return Response(
            {"message": "Superuser successfully created"},
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        LOGGER.error(
            f"Error during superuser creation by admin {admin.username} from IP: {ip}: {str(e)}"
        )
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@admin_access_required
def search_user_info(request: HttpRequest) -> Response:
    """
    Search and retrieve information about a user including token statistics, estimated cost,
    email stats, linked email addresses, and subscription details.

    Request Parameters:
        - id (int, optional): User ID.
        - username (str, optional): Username of the user.
        - emailAddress (str, optional): Email address associated with the user.
        - emailsStatsParam (str, optional): Additional parameters for computing email stats.

    Returns:
        Response: JSON object with user information and statistics or an error message if not found.
    """
    ip = security.get_ip_with_port(request)
    admin = request.user
    LOGGER.info(
        f"Admin {admin.id} ({admin.username}) from IP {ip} is searching user information."
    )

    try:
        parameters: dict = json.loads(request.body)
        user_id = parameters.get("id")
        username = parameters.get("username")
        email_address = parameters.get("emailAddress")
        email_stats_param = parameters.get("emailsStatsParam")

        user = None
        if email_address:
            user = SocialAPI.objects.get(email=email_address).user
        elif user_id:
            user = User.objects.get(id=user_id, is_superuser=False)
        elif username:
            user = User.objects.get(username=username, is_superuser=False)

        if not user:
            LOGGER.error(
                f"Admin {admin.id} ({admin.username}) from IP {ip} - User not found."
            )
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        subscription = Subscription.objects.get(user=user)
        trial_period = timedelta(days=30)
        statistics = Statistics.objects.get(user=user)
        social_apis = SocialAPI.objects.filter(user=user)

        nb_tokens_input = statistics.nb_tokens_input
        nb_tokens_output = statistics.nb_tokens_output
        price_tokens_input = nb_tokens_input / 1_000_000 * 0.25
        price_tokens_output = nb_tokens_output / 1_000_000 * 1.25
        computed_stats = compute_statistics(statistics, email_stats_param)

        LOGGER.info(
            f"Admin {admin.id} ({admin.username}) from IP {ip} successfully retrieved info for user {user.id}."
        )
        return Response(
            {
                "socialAPIs": {
                    "linked": [
                        {"typeApi": social_api.type_api, "email": social_api.email}
                        for social_api in social_apis
                    ],
                    "count": social_apis.count(),
                },
                "emailsStats": computed_stats,
                "plan": {
                    "creationDate": subscription.created_at,
                    "name": subscription.plan,
                    "isTrial": subscription.is_trial,
                    "isActive": subscription.is_active,
                    "expiresThe": (
                        subscription.created_at + trial_period
                        if subscription.is_trial
                        else None
                    ),
                },
                "nbTokensInput": nb_tokens_input,
                "nbTokensOutput": nb_tokens_output,
                "estimatedCostUser": {
                    "priceTokensInput": price_tokens_input,
                    "priceTokensOutput": price_tokens_output,
                    "total": price_tokens_input + price_tokens_output,
                },
            },
            status=status.HTTP_200_OK,
        )

    except User.DoesNotExist:
        LOGGER.error(
            f"Admin {admin.id} ({admin.username}) from IP {ip} - User not found with provided details."
        )
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except SocialAPI.DoesNotExist:
        LOGGER.error(
            f"Admin {admin.id} ({admin.username}) from IP {ip} - No SocialAPI record found for email: {email_address}"
        )
        return Response(
            {"error": "No SocialAPI record found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Statistics.DoesNotExist:
        LOGGER.error(
            f"Admin {admin.id} ({admin.username}) from IP {ip} - Statistics not found for user: {user.id}"
        )
        return Response(
            {"error": "Statistics not found for the user"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        LOGGER.error(
            f"Admin {admin.id} ({admin.username}) from IP {ip} - Unexpected error: {str(e)}"
        )
        return Response(
            {"error": "An unexpected error occurred"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@admin_access_required
def get_dashboard_data(request: HttpRequest) -> Response:
    """
    Retrieve key statistics for the Aomail application.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: JSON with total email count, social API count, user count (non-admin),
        and admin count (superusers).
    """
    ip = security.get_ip_with_port(request)
    admin = request.user
    LOGGER.info(
        f"Dashboard data request from IP: {ip} by admin {admin.username} (ID: {admin.id})"
    )

    try:
        email_count = Email.objects.count()
        social_api_counts = SocialAPI.objects.aggregate(
            microsoft_count=Count(Case(When(type_api=MICROSOFT, then=1))),
            google_count=Count(Case(When(type_api=GOOGLE, then=1))),
            total=Count("id"),
        )
        user_counts = User.objects.aggregate(
            superuser_count=Count(Case(When(is_superuser=True, then=1))),
            total_count=Count("id"),
        )
        regular_user_count = user_counts["total_count"] - user_counts["superuser_count"]

        LOGGER.info(
            f"Dashboard data successfully retrieved by admin {admin.username} (ID: {admin.id}) from IP: {ip}"
        )
        return Response(
            {
                "emailCount": email_count,
                "socialApiCount": {
                    MICROSOFT: social_api_counts["microsoft_count"],
                    GOOGLE: social_api_counts["google_count"],
                    "total": social_api_counts["total"],
                },
                "userCount": regular_user_count,
                "adminCount": user_counts["superuser_count"],
            },
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        LOGGER.error(
            f"Error retrieving dashboard data by admin {admin.username} (ID: {admin.id}) from IP: {ip}: {str(e)}"
        )
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["PUT"])
@admin_access_required
def update_admin_data(request: HttpRequest) -> Response:
    """
    Update authenticated admin details (username, password).

    Args:
        request (HttpRequest): JSON body with optional fields:
            - username (str): New admin username.
            - password (str): New admin password.

    Returns:
        Response: Success message or error details on failure.
    """
    ip = security.get_ip_with_port(request)
    admin = request.user
    LOGGER.info(
        f"Admin update request from IP: {ip} by admin {admin.username} (ID: {admin.id})"
    )
    parameters: dict = json.loads(request.body)
    username = parameters.get("username")
    password = parameters.get("password")

    if username:
        if len(username) < 4:
            LOGGER.error(
                f"Invalid username update attempt by admin {admin.username} (ID: {admin.id}) from IP: {ip}"
            )
            return Response(
                {"error": "Username must be at least 4 characters long."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        admin.username = username

    if password:
        if not (8 <= len(password) <= 50):
            LOGGER.error(
                f"Invalid password update attempt by admin {admin.username} (ID: {admin.id}) from IP: {ip}"
            )
            return Response(
                {"error": "Password length must be between 8 and 50 characters."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        admin.set_password(password)

    admin.save()
    LOGGER.info(
        f"Admin {admin.username} (ID: {admin.id}) successfully updated details from IP: {ip}"
    )
    return Response(
        {"success": "Details updated successfully."}, status=status.HTTP_200_OK
    )


@api_view(["DELETE"])
@admin_access_required
def delete_admin(request: HttpRequest) -> Response:
    """
    Deletes an admin account based on the provided username or ID.

    Parameters:
        - id (int, optional): The ID of the admin to be deleted.
        - username (str, optional): The username of the admin to be deleted.

    Returns:
        Response: JSON response indicating success or failure.
    """
    admin = request.user
    ip = security.get_ip_with_port(request)
    LOGGER.info(
        f"Delete admin request received from admin {admin.username} (ID: {admin.id}) from IP: {ip}"
    )

    parameters: dict = json.loads(request.body)
    admin_id = parameters.get("id")
    username = parameters.get("username")

    try:
        if admin_id:
            user_to_delete = User.objects.get(id=admin_id, is_superuser=True)
        elif username:
            user_to_delete = User.objects.get(username=username, is_superuser=True)
        else:
            LOGGER.error(
                f"Admin deletion failed: No ID or username provided by admin {admin.username} from IP: {ip}"
            )
            return Response(
                {"error": "ID or username must be provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_to_delete.delete()
        LOGGER.info(
            f"Admin '{user_to_delete.username}' (ID: {user_to_delete.id}) deleted by admin {admin.username} (ID: {admin.id}) from IP: {ip}"
        )
        return Response(
            {"message": "Admin deleted successfully."}, status=status.HTTP_200_OK
        )

    except User.DoesNotExist:
        LOGGER.error(
            f"Admin deletion failed: Admin not found with provided details by admin {admin.username} from IP: {ip}"
        )
        return Response({"error": "Admin not found."}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        LOGGER.error(
            f"Admin deletion error by admin {admin.username} (ID: {admin.id}) from IP: {ip}: {str(e)}"
        )
        return Response(
            {"error": "Internal server error."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request: HttpRequest) -> Response:
    """
    Authenticates a user (admin) using the provided username and password, and returns an access token.

    Args:
        request (HttpRequest): The HTTP request object containing the following parameters in the body:
            username (str): User's unique username for authentication.
            password (str): User's password for authentication.

    Returns:
        Response: JSON response with an access token on successful authentication,
                  or an error message on failure.
    """
    ip = security.get_ip_with_port(request)
    LOGGER.info(f"Login request received from IP: {ip}")

    parameters: dict = json.loads(request.body)
    username = parameters.get("username")
    password = parameters.get("password")

    if not username:
        return Response(
            {"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    if not password:
        return Response(
            {"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)

    if user is None:
        LOGGER.error(f"Failed login attempt for username: {username} from IP: {ip}")
        return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not user.is_superuser:
        LOGGER.error(
            f"Unauthorized login attempt by non-admin user: {username} with ID: {user.id} from IP: {ip}"
        )
        return Response(
            {"error": "Access denied: Admin access required"},
            status=status.HTTP_403_FORBIDDEN,
        )

    refresh: RefreshToken = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    LOGGER.info(f"Admin login successful for username: {username} from IP: {ip}")
    return Response(
        {"accessToken": access_token},
        status=status.HTTP_200_OK,
    )


@api_view(["PUT"])
@admin_access_required
def update_user_info(request: HttpRequest) -> Response:
    """
    Updates the information of a specified user (admin).

    Parameters:
        request (HttpRequest): The HTTP request object containing the following parameters in the body:
            - id (int, optional): The ID of the user to be updated.
            - username (str, optional): The username of the user to be updated.
            - emailAddress (str, optional): The email address of the user to be updated.
            - plan (str, optional): The new subscription plan to assign to the user.

    Returns:
        Response: JSON response indicating success or failure.
    """
    admin = request.user
    ip = security.get_ip_with_port(request)
    LOGGER.info(
        f"Update user info request received from admin {admin.username} (ID: {admin.id}) from IP: {ip}"
    )

    parameters: dict = json.loads(request.body)
    user_id = parameters.get("id")
    username = parameters.get("username")
    email_address = parameters.get("emailAddress")
    plan = parameters.get("plan")

    user = None

    try:
        if email_address:
            user = SocialAPI.objects.get(email=email_address).user
        elif user_id:
            user = User.objects.get(id=user_id, is_superuser=False)
        elif username:
            user = User.objects.get(username=username, is_superuser=False)

        if not user:
            raise User.DoesNotExist()

        if plan not in ALLOWED_PLANS:
            raise ValueError("Plan not allowed")

        subscription = Subscription.objects.get(user=user)
        subscription.plan = plan
        subscription.is_trial = False
        subscription.save()

        LOGGER.info(
            f"Admin {admin.id} ({admin.username}) updated the plan for user {user.username} to '{plan}'."
        )
        return Response(
            {"message": "User information updated successfully."},
            status=status.HTTP_200_OK,
        )

    except (SocialAPI.DoesNotExist, User.DoesNotExist) as e:
        LOGGER.error(f"Admin {admin.id} ({admin.username}) from IP {ip} - {str(e)}.")
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError as e:
        LOGGER.error(f"Admin {admin.id} ({admin.username}) from IP {ip} - {str(e)}.")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Subscription.DoesNotExist:
        LOGGER.error(
            f"Admin {admin.id} ({admin.username}) from IP {ip} - Subscription not found for user {user.username}."
        )
        return Response(
            {"error": "Subscription not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        LOGGER.error(
            f"Admin {admin.id} ({admin.username}) from IP {ip} - Unexpected error: {str(e)}."
        )
        return Response(
            {"error": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
