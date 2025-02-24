"""
Handles user rule operations, returns results to frontend, and saves to database.

Endpoints:
- ✅ handle_rules: Handle Create, Update, Delete operations for rules.
"""

import json
import logging
from django.http import HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from aomail.utils.security import subscription
from aomail.constants import ALLOW_ALL
from aomail.models import Rule
from aomail.utils.serializers import RuleSerializer


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


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
            "logical_operator": data.get("logicalOperator", "OR"),
            "domains": data.get("domains") if data.get("domains") else None,
            "sender_emails": (
                data.get("senderEmails") if data.get("senderEmails") else None
            ),
            "has_attachements": (
                data.get("hasAttachements") if data.get("hasAttachements") else None
            ),
            "categories": data.get("categories") if data.get("categories") else None,
            "priorities": data.get("priorities") if data.get("priorities") else None,
            "answers": data.get("answers") if data.get("answers") else None,
            "relevances": data.get("relevances") if data.get("relevances") else None,
            "flags": data.get("flags") if data.get("flags") else None,
            "email_deal_with": (
                data.get("emailDealWith") if data.get("emailDealWith") else None
            ),
            "action_transfer_recipients": (
                data.get("actionTransferRecipients")
                if data.get("actionTransferRecipients")
                else None
            ),
            "action_set_flags": (
                data.get("actionSetFlags") if data.get("actionSetFlags") else None
            ),
            "action_mark_as": (
                data.get("actionMarkAs") if data.get("actionMarkAs") else None
            ),
            "action_delete": (
                data.get("actionDelete") if data.get("actionDelete") else None
            ),
            "action_set_category": (
                data.get("actionSetCategory") if data.get("actionSetCategory") else None
            ),
            "action_set_priority": (
                data.get("actionSetPriority") if data.get("actionSetPriority") else None
            ),
            "action_set_relevance": (
                data.get("actionSetRelevance")
                if data.get("actionSetRelevance")
                else None
            ),
            "action_set_answer": (
                data.get("actionSetAnswer") if data.get("actionSetAnswer") else None
            ),
            "action_reply_prompt": (
                data.get("actionReplyPrompt") if data.get("actionReplyPrompt") else None
            ),
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
        "logical_operator": data.get("logicalOperator", "OR"),
        "domains": data.get("domains") if data.get("domains") else None,
        "sender_emails": (
            data.get("senderEmails") if data.get("senderEmails") else None
        ),
        "has_attachements": (
            data.get("hasAttachements") if data.get("hasAttachements") else None
        ),
        "categories": data.get("categories") if data.get("categories") else None,
        "priorities": data.get("priorities") if data.get("priorities") else None,
        "answers": data.get("answers") if data.get("answers") else None,
        "relevances": data.get("relevances") if data.get("relevances") else None,
        "flags": data.get("flags") if data.get("flags") else None,
        "email_deal_with": (
            data.get("emailDealWith") if data.get("emailDealWith") else None
        ),
        "action_transfer_recipients": (
            data.get("actionTransferRecipients")
            if data.get("actionTransferRecipients")
            else None
        ),
        "action_set_flags": (
            data.get("actionSetFlags") if data.get("actionSetFlags") else None
        ),
        "action_mark_as": (
            data.get("actionMarkAs") if data.get("actionMarkAs") else None
        ),
        "action_delete": (
            data.get("actionDelete") if data.get("actionDelete") else None
        ),
        "action_set_category": (
            data.get("actionSetCategory") if data.get("actionSetCategory") else None
        ),
        "action_set_priority": (
            data.get("actionSetPriority") if data.get("actionSetPriority") else None
        ),
        "action_set_relevance": (
            data.get("actionSetRelevance") if data.get("actionSetRelevance") else None
        ),
        "action_set_answer": (
            data.get("actionSetAnswer") if data.get("actionSetAnswer") else None
        ),
        "action_reply_prompt": (
            data.get("actionReplyPrompt") if data.get("actionReplyPrompt") else None
        ),
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
        LOGGER.info(f"serializer.errors: {serializer.errors}")
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
