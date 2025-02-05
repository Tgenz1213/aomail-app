"""
Handles Labels operations with Gmail API

Features:
- ✅ replicate_labels: Replicate labels on Gmail.
"""

import logging
from aomail.email_providers.google.authentication import (
    authenticate_service,
)
from aomail.models import SocialAPI
from aomail.constants import (
    ANSWER_REQUIRED,
    MIGHT_REQUIRE_ANSWER,
    NO_ANSWER_REQUIRED,
    HIGHLY_RELEVANT,
    POSSIBLY_RELEVANT,
    NOT_RELEVANT,
)


LOGGER = logging.getLogger(__name__)
HIDE_LABEL_NAMES = [
    ANSWER_REQUIRED,
    MIGHT_REQUIRE_ANSWER,
    NO_ANSWER_REQUIRED,
    HIGHLY_RELEVANT,
    POSSIBLY_RELEVANT,
    NOT_RELEVANT,
    "spam",
    "scam",
    "newsletter",
    "notification",
    "meeting",
]


def replicate_labels(social_api: SocialAPI, ai_output: dict, email_id: str):
    """
    Replicate labels on Gmail based on AI output.

    Args:
        social_api (SocialAPI): The social API object associated with the email.
        ai_output (dict): AI output containing email categorization details.
        email_id (str): ID of the email to update.
    """
    LOGGER.info(f"Replication of labels on Gmail for {social_api.email} started")

    gmail = authenticate_service(social_api.user, social_api.email, ["gmail"])["gmail"]
    labels_list = gmail.users().labels().list(userId="me").execute()
    existing_labels = labels_list.get("labels", [])

    allowed_colors = {
        "#000000",
        "#434343",
        "#666666",
        "#999999",
        "#cccccc",
        "#efefef",
        "#f3f3f3",
        "#ffffff",
        "#fb4c2f",
        "#ffad47",
        "#fad165",
        "#16a766",
        "#43d692",
        "#4a86e8",
        "#a479e2",
        "#f691b3",
        "#f6c5be",
        "#ffe6c7",
        "#fef1d1",
        "#b9e4d0",
        "#c6f3de",
        "#c9daf8",
        "#e4d7f5",
        "#fcdee8",
        "#efa093",
        "#ffd6a2",
        "#fce8b3",
        "#89d3b2",
        "#a0eac9",
        "#a4c2f4",
        "#d0bcf1",
        "#fbc8d9",
        "#e66550",
        "#ffbc6b",
        "#fcda83",
        "#44b984",
        "#68dfa9",
        "#6d9eeb",
        "#b694e8",
        "#f7a7c0",
        "#cc3a21",
        "#eaa041",
        "#f2c960",
        "#149e60",
        "#3dc789",
        "#3c78d8",
        "#8e63ce",
        "#e07798",
        "#ac2b16",
        "#cf8933",
        "#d5ae49",
        "#0b804b",
        "#2a9c68",
        "#285bac",
        "#653e9b",
        "#b65775",
        "#822111",
        "#a46a21",
        "#aa8831",
        "#076239",
        "#1a764d",
        "#1c4587",
        "#41236d",
        "#83334c",
        "#464646",
        "#e7e7e7",
        "#0d3472",
        "#b6cff5",
        "#0d3b44",
        "#98d7e4",
        "#3d188e",
        "#e3d7ff",
        "#711a36",
        "#fbd3e0",
        "#8a1c0a",
        "#f2b2a8",
        "#7a2e0b",
        "#ffc8af",
        "#7a4706",
        "#ffdeb5",
        "#594c05",
        "#fbe983",
        "#684e07",
        "#fdedc1",
        "#0b4f30",
        "#b3efd3",
        "#04502e",
        "#a2dcc1",
        "#c2c2c2",
        "#4986e7",
        "#2da2bb",
        "#b99aff",
        "#994a64",
        "#f691b2",
        "#ff7537",
        "#ffad46",
        "#662e37",
        "#ebdbde",
        "#cca6ac",
        "#094228",
        "#42d692",
        "#16a765",
    }

    label_colors = {
        "important": "#fb4c2f",
        "informative": "#4a86e8",
        "useless": "#999999",
        "spam": "#cc3a21",
        "scam": "#994a64",
        "newsletter": "#16a766",
        "notification": "#fad165",
        "meeting": "#6d9eeb",
        "Answer Required": "#ffc8af",
        "Might Require Answer": "#ffad46",
        "No Answer Required": "#98d7e4",
        "Highly Relevant": "#43d692",
        "Possibly Relevant": "#a2dcc1",
        "Not Relevant": "#cccccc",
    }

    # Remove colors already used in existing labels
    for label in existing_labels:
        color = label.get("color", {}).get("backgroundColor")
        if color in allowed_colors:
            allowed_colors.remove(color)

    def find_or_create_label(name: str) -> str:
        """Find an existing label or create a new one."""
        for label in existing_labels:
            if name == "important":
                name = "important_"
            elif name == "spam":
                name = "spam_"
            if label.get("name", "") == name:
                return label.get("id")

        label_color = label_colors.get(name, allowed_colors.pop())
        label_body = {
            "name": name,
            "color": {
                "textColor": "#000000",
                "backgroundColor": label_color,
            },
            "messageListVisibility": "hide" if name in HIDE_LABEL_NAMES else "show",
            "labelListVisibility": (
                "labelHide" if name in HIDE_LABEL_NAMES else "labelShow"
            ),
        }
        response = gmail.users().labels().create(userId="me", body=label_body).execute()
        return response.get("id")

    # Process AI output
    label_ids = []
    for key, value in ai_output.items():
        if key == "flags":
            for flag, active in value.items():
                if active:
                    label_id = find_or_create_label(flag)
                    label_ids.append(label_id)

        else:
            label_id = find_or_create_label(value)
            label_ids.append(label_id)

    gmail.users().messages().modify(
        userId="me",
        id=email_id,
        body={"addLabelIds": label_ids},
    ).execute()

    LOGGER.info(
        f"Labels replicated successfully on Gmail for {social_api.email} and email_id: {email_id}"
    )
