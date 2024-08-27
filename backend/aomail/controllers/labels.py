"""
Handles label operations, returns results to frontend, and saves to database.

Endpoints:
- ✅ delete_labels: Deletes multiple labels based on a list of IDs.
"""

import json
import logging
from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from aomail.utils.security import subscription
from aomail.constants import FREE_PLAN
from aomail.models import Label
from rest_framework import status


LOGGER = logging.getLogger(__name__)


@api_view(["DELETE"])
@subscription([FREE_PLAN])
def delete_labels(request: HttpRequest) -> Response:
    """
    Deletes multiple labels associated with the authenticated user.

    Args:
        request (HttpRequest): HTTP request object containing a list of label IDs in the request body.

    Returns:
        Response:
            {"message": "Labels deleted successfully"} if the labels are deleted successfully.
            {"error": "<error_message>"} if any other error occurs during the process.
    """
    try:
        user = request.user
        parameters: dict = json.loads(request.body)
        ids = parameters.get("ids")

        if not ids:
            return Response(
                {"error": "No label IDs provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        for id in ids:
            label = Label.objects.get(id=id, user=user)
            label.delete()

        return Response(
            {"message": "Labels deleted successfully"}, status=status.HTTP_200_OK
        )

    except Label.DoesNotExist:
        return Response(
            {"error": "One or more labels not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON in request body"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        LOGGER.error(f"Error when deleting labels: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
