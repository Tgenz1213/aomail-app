"""
Handles user rule operations, returns results to frontend, and saves to database.

Endpoints:
- ✅ set_rule_block_for_sender: Set a blocking rule for the sender of the specified email.
- ✅ get_user_rules: Retrieve rules associated with the authenticated user.
- ✅ get_user_rule_by_id: Retrieve details of a specific rule.
- ✅ delete_user_rule_by_id: Delete a specific rule.
- ✅ create_user_rule: Create a new rule.
- ✅ update_user_rule: Update an existing rule.
"""

import json
import logging
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from aomail.utils.security import subscription
from aomail.constants import (
    FREE_PLAN,
)
from aomail.models import (
    Email,
    Rule,
)
from aomail.utils.serializers import (
    RuleBlockUpdateSerializer,
    RuleSerializer,
)


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


@api_view(["POST"])
@subscription([FREE_PLAN])
def set_rule_block_for_sender(request: HttpRequest, email_id) -> Response:
    """
    Sets a blocking rule for the sender of the specified email associated with the authenticated user.

    Args:
        request (HttpRequest): HTTP request object containing the authenticated user.
        email_id (int): The ID of the email whose sender should be blocked.

    Returns:
        Response: A JSON response containing the updated rule data indicating the sender has been blocked.
    """
    user = request.user
    email = get_object_or_404(Email, user=user, id=email_id)

    rule, created = Rule.objects.get_or_create(
        sender=email.sender, user=user, defaults={"block": True}, priority=""
    )
    if not created:
        rule.block = True
        rule.save()

    serializer = RuleBlockUpdateSerializer(rule)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@subscription([FREE_PLAN])
def get_user_rules(request: HttpRequest) -> Response:
    """
    Retrieves rules associated with the authenticated user.

    Args:
        request (HttpRequest): HTTP request object containing the authenticated user.

    Returns:
        Response: A JSON response containing a list of rules owned by the user.
    """
    user_rules = Rule.objects.filter(user=request.user)
    rules_data = []

    for rule in user_rules:
        rule_serializer = RuleSerializer(rule)
        rule_data = rule_serializer.data

        category_name = rule.category.name if rule.category else None
        sender_name = rule.sender.name if rule.sender else None
        sender_email = rule.sender.email if rule.sender else None

        rule_data["categoryName"] = category_name
        rule_data["senderName"] = sender_name
        rule_data["senderEmail"] = sender_email

        rules_data.append(rule_data)

    return Response(rules_data, status=status.HTTP_200_OK)


@api_view(["GET"])
@subscription([FREE_PLAN])
def get_user_rule_by_id(request: HttpRequest, id_rule: int) -> Response:
    """
    Retrieves details of a specific rule owned by the authenticated user.

    Args:
        request (HttpRequest): HTTP request object containing the authenticated user.
        id_rule (int): ID of the rule to retrieve.

    Returns:
        Response: A JSON response containing details of the rule.
                      If the rule is not found, returns {"error": "Rule not found"} with status 400.
    """
    try:
        user_rule = Rule.objects.get(id=id_rule, user=request.user)
    except Rule.DoesNotExist:
        return Response({"error": "Rule not found"}, status=status.HTTP_400_BAD_REQUEST)

    rule_serializer = RuleSerializer(user_rule)
    rule_data = rule_serializer.data

    category_name = user_rule.category.name if user_rule.category else None
    sender_name = user_rule.sender.name if user_rule.sender else None
    sender_email = user_rule.sender.email if user_rule.sender else None

    rule_data["categoryName"] = category_name
    rule_data["senderName"] = sender_name
    rule_data["senderEmail"] = sender_email

    return Response(rule_data)


@api_view(["DELETE"])
@subscription([FREE_PLAN])
def delete_user_rule_by_id(request: HttpRequest, id_rule: int) -> Response:
    """
    Deletes a specific rule owned by the authenticated user.

    Args:
        request (HttpRequest): HTTP request object containing the authenticated user.
        id_rule (int): ID of the rule to delete.

    Returns:
        Response: {"message": "Rule deleted successfully"} if the rule is deleted.
                      {"error": "Rule not found"} with status 400 if the rule doesn't exist for the user.
    """
    try:
        user_rule = Rule.objects.get(id=id_rule, user=request.user)
    except Rule.DoesNotExist:
        return Response({"error": "Rule not found"}, status=status.HTTP_400_BAD_REQUEST)

    user_rule.delete()

    return Response({"message": "Rule deleted successfully"})


@api_view(["POST"])
@subscription([FREE_PLAN])
def create_user_rule(request: HttpRequest) -> Response:
    """
    Creates a new rule for the authenticated user based on the request data.

    Args:
        request (HttpRequest): HTTP request object containing rule data in the request body.

    Returns:
        Response: JSON response with the created rule data if successful.
                      {"error": "Details of the specific error."} if there's an issue with the creation.
    """
    data: dict = json.loads(request.body)
    user = request.user

    sender_id = data.get("sender")
    if not sender_id:
        return Response(
            {"error": "Sender ID must be provided"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    existing_rule = Rule.objects.filter(sender_id=sender_id, user=user)
    if existing_rule.exists():
        return Response(
            {"error": "A rule already exists for that sender"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = RuleSerializer(data=data, context={"user": user})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["PUT"])
@subscription([FREE_PLAN])
def update_user_rule(request: HttpRequest) -> Response:
    """
    Updates an existing rule for the authenticated user based on the request data.

    Args:
        request (HttpRequest): HTTP request object containing rule data in the request body.

    Returns:
        Response: JSON response with the updated rule data if successful.
                      {"error": "Details of the specific error."} if there's an issue with the update.
    """
    data: dict = json.loads(request.body)
    rule_id = data.get("id")

    try:
        rule = Rule.objects.get(id=rule_id, user=request.user)
    except Rule.DoesNotExist:
        return Response(
            {"error": "Rule not found."}, status=status.HTTP_400_BAD_REQUEST
        )

    serializer = RuleSerializer(
        rule, data=data, partial=True, context={"user": request.user}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
