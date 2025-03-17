"""
Handles Labels (Categories) operations with Graph API

Features:
- ✅ replicate_labels: Replicate labels on Outlook.
"""

import logging
import requests
from aomail.models import SocialAPI
from aomail.email_providers.microsoft.authentication import (
    get_headers,
    refresh_access_token,
)
from aomail.constants import GRAPH_URL


LOGGER = logging.getLogger(__name__)


def replicate_labels(social_api: SocialAPI, ai_output: dict, email_id: str):
    """
    Replicate labels on Outlook based on AI output.

    Args:
        social_api (SocialAPI): The social API object associated with the email.
        ai_output (dict): AI output containing email categorization details.
        email_id (str): ID of the email to update.
    """
    LOGGER.info(f"Replication of labels on Outlook for {social_api.email} started")

    category_colors = {
        "important": "Preset16",  # Orange
        "informative": "Preset7",  # Blue
        "useless": "Preset12",  # Gray
        "Answer Required": "Preset9",  # Amber/Gold
    }

    try:
        access_token = refresh_access_token(social_api)
        headers = get_headers(access_token)
        email_url = f"{GRAPH_URL}me/messages/{email_id}"

        categories_to_apply = []

        # Process AI output - only apply specific categories
        for key, value in ai_output.items():
            if key == "importance" or key == "topic":
                if value:
                    categories_to_apply.append(value)
            elif key == "response" and value == "Answer Required":
                categories_to_apply.append(value)

        # Create categories if they don't exist
        existing_categories = get_existing_categories(headers)
        for category in categories_to_apply:
            if category not in existing_categories:
                create_category(
                    headers,
                    category,
                    category_colors[category],
                )

        # Update the email with categories (labels)
        update_payload = {"categories": categories_to_apply}
        LOGGER.info(f"Attempting to apply categories: {categories_to_apply}")

        update_response = requests.patch(
            email_url, headers=headers, json=update_payload
        )

        if update_response.status_code != 200:
            LOGGER.error(f"Failed to apply categories: {update_response.json()}")

        # Move email to category folder
        folder_id = ensure_folder_exists(headers, ai_output["topic"])
        if folder_id:
            move_url = f"{GRAPH_URL}me/messages/{email_id}/move"
            move_response = requests.post(
                move_url, headers=headers, json={"destinationId": folder_id}
            )

            if move_response.status_code != 201:
                LOGGER.error(f"Failed to move email: {move_response.json()}")

        LOGGER.info(
            f"Labels replicated successfully for email_id: {email_id} and social_api email: {social_api.email}"
        )

    except Exception as e:
        LOGGER.error(f"Failed to replicate labels: {str(e)}")


def get_existing_categories(headers):
    """Get existing categories from Outlook."""
    try:
        response = requests.get(
            f"{GRAPH_URL}me/outlook/masterCategories", headers=headers
        )
        if response.status_code == 200:
            return {cat["displayName"] for cat in response.json().get("value", [])}
        return set()
    except Exception as e:
        LOGGER.error(f"Failed to get existing categories: {str(e)}")
        return set()


def create_category(headers: dict, category_name: str, color: str) -> bool:
    """Create a category in Outlook."""
    try:
        payload = {"displayName": category_name, "color": color}
        response = requests.post(
            f"{GRAPH_URL}me/outlook/masterCategories", headers=headers, json=payload
        )
        if response.status_code == 201:
            LOGGER.info(f"Created category: {category_name}")
            return True
        LOGGER.warning(f"Failed to create category {category_name}: {response.json()}")
        return False
    except Exception as e:
        LOGGER.error(f"Error creating category {category_name}: {str(e)}")
        return False


def ensure_folder_exists(headers: dict, folder_name: str) -> str | None:
    """Ensure folder exists and return its ID."""
    try:
        # First try to find existing folder
        response = requests.get(f"{GRAPH_URL}me/mailFolders", headers=headers)
        if response.status_code == 200:
            folders = response.json().get("value", [])
            for folder in folders:
                if folder["displayName"] == folder_name:
                    return folder["id"]

        # Create new folder if not found
        response = requests.post(
            f"{GRAPH_URL}me/mailFolders",
            headers=headers,
            json={"displayName": folder_name},
        )
        if response.status_code == 201:
            return response.json()["id"]

        LOGGER.error(f"Failed to create folder: {response.json()}")
        return None
    except Exception as e:
        LOGGER.error(f"Error managing folder {folder_name}: {str(e)}")
        return None
