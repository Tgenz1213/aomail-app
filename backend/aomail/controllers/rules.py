"""
Handles user rule operations, returns results to frontend, and saves to database.

Endpoints:
- ✅ set_rule_block_for_sender: Set a blocking rule for the sender of the specified email.
- ✅ handle_rules: Handle Create, Update, Delete operations for rules.
"""

import json
import logging
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from aomail.utils.security import subscription
from aomail.constants import ALLOW_ALL
from aomail.models import (
    Email,
    Rule,
)
from aomail.utils.serializers import (
    RuleBlockUpdateSerializer,
    RuleSerializer,
)
from django.db import models


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


@api_view(["POST"])
@subscription(ALLOW_ALL)
def set_rule_block_for_sender(request: HttpRequest, email_id) -> Response:
    """
    Sets a blocking rule for the sender of the specified email associated with the authenticated user.
    If a rule already exists that blocks this sender's domain or email, no new rule is created.

    Args:
        request (HttpRequest): HTTP request object containing the authenticated user.
        email_id (int): The ID of the email whose sender should be blocked.

    Returns:
        Response: A JSON response containing the updated rule data indicating the sender has been blocked.
    """
    user = request.user
    email = get_object_or_404(Email, user=user, id=email_id)
    sender_email = email.sender.email
    sender_domain = sender_email.split("@")[1]

    # Check if there's already a rule blocking this sender's domain or email
    existing_rule = (
        Rule.objects.filter(user=user)
        .filter(
            models.Q(domains__contains=[sender_domain])
            | models.Q(sender_emails__contains=[sender_email])
        )
        .filter(action_delete=True)
        .first()
    )

    if existing_rule:
        # Rule already exists that blocks this sender
        serializer = RuleBlockUpdateSerializer(existing_rule)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Create new rule to block this sender
    rule = Rule.objects.create(
        user=user,
        logical_operator="OR",
        sender_emails=[sender_email],
        action_delete=True,
    )

    serializer = RuleBlockUpdateSerializer(rule)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST", "PUT", "DELETE"])
@subscription(ALLOW_ALL)
def handle_rules(request: HttpRequest) -> Response:
    """
    Handle CRUD operations for rules.
    - POST: Create a new rule
    - PUT: Update an existing rule
    - DELETE: Delete a rule

    Args:
        request (HttpRequest): HTTP request object containing rule data in the request body.

    Returns:
        Response: JSON response appropriate to the operation.
    """
    if request.method == "POST":
        return create_rule(request)
    elif request.method == "PUT":
        data = json.loads(request.body)
        try:
            rule = Rule.objects.get(id=data.get("id"), user=request.user)
        except Rule.DoesNotExist:
            return Response(
                {"error": "Rule not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Convert frontend keys to backend keys
        backend_data = {
            "logical_operator": data.get("logicalOperator"),
            "domains": data.get("domains", []),
            "sender_emails": data.get("senderEmails", []),
            "has_attachements": data.get("hasAttachements", False),
            "categories": data.get("categories", []),
            "priorities": data.get("priorities", []),
            "answers": data.get("answers", []),
            "relevances": data.get("relevances", []),
            "flags": data.get("flags", []),
            "email_deal_with": data.get("emailDealWith", ""),
            "action_transfer_recipients": data.get("actionTransferRecipients", []),
            "action_set_flags": data.get("actionSetFlags", []),
            "action_mark_as": data.get("actionMarkAs", []),
            "action_delete": data.get("actionDelete", False),
            "action_set_category": data.get("actionSetCategory"),
            "action_set_priority": data.get("actionSetPriority", ""),
            "action_set_relevance": data.get("actionSetRelevance", ""),
            "action_set_answer": data.get("actionSetAnswer", ""),
            "action_reply_prompt": data.get("actionReplyPrompt", ""),
            "action_reply_recipients": data.get("actionReplyRecipients", []),
        }

        serializer = RuleSerializer(
            rule, data=backend_data, partial=True, context={"user": request.user}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == "DELETE":
        data = json.loads(request.body)
        rule_ids = data.get("ids")
        for rule_id in rule_ids:
            try:
                rule = Rule.objects.get(id=rule_id, user=request.user)
                rule.delete()
            except Rule.DoesNotExist:
                return Response(
                    {"error": "Rule not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response({"message": "Rules deleted successfully"})

    return Response(
        {"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
    )


def create_rule(request: HttpRequest) -> Response:
    """
    Creates a new rule for the authenticated user based on the request data.

    Args:
        request (HttpRequest): HTTP request object containing rule data in the request body.

    Returns:
        Response: JSON response with the created rule data if successful.
                 Error response if validation fails.
    """
    data: dict = json.loads(request.body)
    user = request.user

    # Check for duplicate rules based on email triggers
    if data.get("senderEmails"):
        existing_rule = Rule.objects.filter(
            user=user, sender_emails__overlap=data["senderEmails"]
        ).first()
        if existing_rule:
            return Response(
                {
                    "error": "A rule already exists for one or more of these email addresses"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    if data.get("domains"):
        existing_rule = Rule.objects.filter(
            user=user, domains__overlap=data["domains"]
        ).first()
        if existing_rule:
            return Response(
                {"error": "A rule already exists for one or more of these domains"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # Convert frontend keys to backend keys
    backend_data = {
        "logical_operator": data.get("logicalOperator"),
        "domains": data.get("domains", []),
        "sender_emails": data.get("senderEmails", []),
        "has_attachements": data.get("hasAttachements", False),
        "categories": data.get("categories", []),
        "priorities": data.get("priorities", []),
        "answers": data.get("answers", []),
        "relevances": data.get("relevances", []),
        "flags": data.get("flags", []),
        "email_deal_with": data.get("emailDealWith", ""),
        "action_transfer_recipients": data.get("actionTransferRecipients", []),
        "action_set_flags": data.get("actionSetFlags", []),
        "action_mark_as": data.get("actionMarkAs", []),
        "action_delete": data.get("actionDelete", False),
        "action_set_category": data.get("actionSetCategory"),
        "action_set_priority": data.get("actionSetPriority", ""),
        "action_set_relevance": data.get("actionSetRelevance", ""),
        "action_set_answer": data.get("actionSetAnswer", ""),
        "action_reply_prompt": data.get("actionReplyPrompt", ""),
        "action_reply_recipients": data.get("actionReplyRecipients", []),
    }

    serializer = RuleSerializer(data=backend_data, context={"user": user})
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
