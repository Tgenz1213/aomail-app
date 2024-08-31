"""
Handles label operations, returns results to frontend, and saves to database.

Endpoints:
- ✅ delete_labels: Deletes multiple labels based on a list of IDs.
"""

import datetime
import json
import logging
import os
import re
from io import BytesIO
from django.http import HttpRequest
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from aomail.constants import FREE_PLAN, GOOGLE, MEDIA_ROOT, MICROSOFT
from aomail.email_providers.google import email_operations as email_operations_google
from aomail.models import Attachment, Email, Label
from aomail.utils.security import subscription


LOGGER = logging.getLogger(__name__)
REQUIRED_SUBJECT_KEYWORDS = [["shipping label", "use by"]]
DATE_PATTERNS = [r"\b\d{2}/\d{2}/\d{4}\b"]
CARRIER_PATTERNS = [
    re.compile(
        r"3\.\s*Drop the parcel off\s*</strong>.*?in the\s*(.*?)\s*drop-off point of your choice\.\s*</p>",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"3\.\s*D\xe9pose le colis.*?dans n'importe\s*quel\s*point\s*(.*?)\s*\.\s*</p>",
        re.IGNORECASE | re.DOTALL,
    ),
]
DEADLINE_PATTERNS = [
    re.compile(
        r"<strong>\s*Postage\s*deadline:\s*</strong>.*?<td[^>]*>\s*(.*?)\s*</td>",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"<strong>\s*À envoyer\s*avant le\s*:\s*</strong>.*?<td[^>]*>\s*(.*?)\s*</td>",
        re.IGNORECASE | re.DOTALL,
    ),
]
ITEM_NAME_PATTERNS = [
    re.compile(
        r"<strong>\s*Item:\s*</strong>.*?<td[^>]*>\s*(.*?)\s*<br\s*/?>",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"<strong>\s*Article\s*:\s*</strong>.*?<td[^>]*>\s*(.*?)\s*<br\s*/?>",
        re.IGNORECASE | re.DOTALL,
    ),
]
REQUIRED_SUBJECT_KEYWORDS = [
    ["shipping label", "use by"],
    ["Bordereau d'envoi", "à utiliser avant le"],
]
DATE_PATTERNS = [r"\b\d{2}/\d{2}/\d{4}\b", r"\b\d{4}-\d{2}-\d{2}\b"]
ECOMMERCE_PLATFORMS = ["vinted", "labrotique", "augu"]
CARRIER_NAMES = {
    "mondialrelay": "mondial_relay",
    "mondial relay": "mondial_relay",
    "Mondial Relay": "mondial_relay",
    "ups": "ups",
    "UPS": "ups",
    "la poste": "la_poste",
    "laposte": "la_poste",
    "chronopost": "chronopost",
    "Chronopost": "chronopost",
    "relais colis": "relais_colis",
    "relaiscolis": "relais_colis",
}


def process_label(email_address: str, email_entry: Email):
    label_data = extract_label_data(email_address, email_entry.html_content)
    create_shipping_label(email_entry, label_data)


def extract_label_data(email_address: str, body: str) -> dict:
    """
    Extracts shipping label information such as carrier name, item name, and postage deadline from the email body.

    Args:
        email_address (str): The email address of the sender.
        body (str): The HTML content of the email body.

    Returns:
        dict: A dictionary containing the carrier name, postage deadline, and item name.
    """
    data = {
        "carrier": None,
        "postage_deadline": None,
        "item_name": None,
        "platform": None,
    }

    # Normalize the body to remove unwanted characters
    normalized_body = re.sub(r"[\r\n]+", " ", body)  # Replace newlines with spaces
    normalized_body = re.sub(
        r"\s+", " ", normalized_body
    )  # Replace multiple spaces with a single space

    for pattern in CARRIER_PATTERNS:
        carrier_match = pattern.search(normalized_body)
        if carrier_match:
            carrier_name = carrier_match.group(1).strip()
            carrier_name = carrier_name.lower()
            data["carrier"] = CARRIER_NAMES.get(carrier_name, carrier_name)
            break

    for pattern in DEADLINE_PATTERNS:
        deadline_match = pattern.search(normalized_body)
        if deadline_match:
            deadline_str = deadline_match.group(1).strip()
            try:
                naive_dt = datetime.datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
                aware_dt = timezone.make_aware(
                    naive_dt, timezone.get_current_timezone()
                )
                data["postage_deadline"] = aware_dt.isoformat()
            except ValueError:
                try:
                    naive_dt = datetime.datetime.strptime(
                        deadline_str, "%d/%m/%Y %I:%M %p"
                    )
                    aware_dt = timezone.make_aware(
                        naive_dt, timezone.get_current_timezone()
                    )
                    data["postage_deadline"] = aware_dt.isoformat()
                except ValueError:
                    try:
                        naive_dt = datetime.datetime.strptime(deadline_str, "%d/%m/%Y")
                        aware_dt = timezone.make_aware(
                            naive_dt, timezone.get_current_timezone()
                        )
                        data["postage_deadline"] = aware_dt.isoformat()
                    except ValueError:
                        data["postage_deadline"] = None
            break

    if not data["carrier"]:
        carrier_pattern_list = "|".join(
            re.escape(name) for name in CARRIER_NAMES.keys()
        )
        carrier_fallback_pattern = re.compile(
            rf"\b({carrier_pattern_list})\b", re.IGNORECASE
        )

        fallback_match = carrier_fallback_pattern.search(normalized_body)
        if fallback_match:
            carrier_key = fallback_match.group(0).lower()
            data["carrier"] = CARRIER_NAMES.get(carrier_key, carrier_key.capitalize())

    for pattern in ITEM_NAME_PATTERNS:
        item_match = pattern.search(normalized_body)
        if item_match:
            data["item_name"] = item_match.group(1).strip()
            break

    for platform in ECOMMERCE_PLATFORMS:
        if platform in email_address:
            data["platform"] = platform
            break

    return data


def create_shipping_label(email: Email, label_data: dict):
    """
    Create the shipping label by merging the official shipping label with a custom message.

    Args:
        email (Email): The email object that contains information about the email message.
        label_data (dict): A dictionary containing the label information such as:
            carrier: The carrier name.
            item_name: The name of the item.
            platform: The platform information.
            postage_deadline: The postage deadline.
    """
    attachment_name = Attachment.objects.get(email=email).name

    if email.social_api.type_api == GOOGLE:
        attachment = email_operations_google.get_attachment_data(
            email.user, email.social_api.email, email.provider_id, attachment_name
        )
    elif email.social_api.type_api == MICROSOFT:
        ...

    pdf_reader = PdfReader(BytesIO(attachment["data"]))
    pdf_writer = PdfWriter()

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        packet = BytesIO()

        if label_data["carrier"] in [
            "mondial_relay",
            "ups",
            "la_poste",
            "chronopost",
            "relais_colis",
        ]:
            orientation = landscape(letter)
        else:
            orientation = landscape(letter)

        canvas_object = canvas.Canvas(packet, pagesize=orientation)
        canvas_object.setFont("Helvetica", 10)

        if label_data["carrier"] in ["mondial_relay", "ups"]:
            if label_data["carrier"] == "mondial_relay":
                y = (
                    pdf_reader.pages[0].mediabox.height / 2
                    - 0.11 * pdf_reader.pages[0].mediabox.height
                )
            else:
                y = (
                    pdf_reader.pages[0].mediabox.height
                    - 0.11 * pdf_reader.pages[0].mediabox.height
                )

            x = pdf_reader.pages[0].mediabox.width / (
                4 if label_data["carrier"] == "mondial_relay" else (3 / 2)
            )
            x -= canvas_object.stringWidth(label_data["item_name"]) / 2
            canvas_object.drawString(x, y, label_data["item_name"])
            y -= 0.018 * pdf_reader.pages[0].mediabox.height

        else:
            if label_data["carrier"] == "la_poste":
                x, y = (
                    1 / 10 * pdf_reader.pages[0].mediabox.width,
                    1 / 5 * pdf_reader.pages[0].mediabox.height
                    - 0.07 * pdf_reader.pages[0].mediabox.height,
                )
            elif label_data["carrier"] == "chronopost":
                x, y = (
                    0.035 * pdf_reader.pages[0].mediabox.width,
                    0.034 * pdf_reader.pages[0].mediabox.height,
                )
            elif label_data["carrier"] == "relais_colis":
                x, y = (
                    3 / 4 * pdf_reader.pages[0].mediabox.width
                    - canvas_object.stringWidth(label_data["item_name"]) / 2,
                    2 / 3 * pdf_reader.pages[0].mediabox.height
                    - 0.034 * pdf_reader.pages[0].mediabox.height,
                )
            canvas_object.drawString(x, y, label_data["item_name"])

        canvas_object.save()
        packet.seek(0)
        new_pdf = PdfReader(packet)
        page.merge_page(new_pdf.pages[0])
        pdf_writer.add_page(page)

    label_name = save_custom_label(
        pdf_writer, label_data["carrier"], label_data["item_name"]
    )
    if label_name:
        save_label_to_db(email, label_data, label_name)


def save_label_to_db(email: Email, label_data: dict, label_name: str):
    """
    Saves the shipping label details to the database.

    Args:
        email (Email): An instance of the Email model representing the email associated with the shipping label.
        label_data (dict): A dictionary containing details about the label.
        label_name (str): The name of the PDF file containing the shipping label.
    """
    Label.objects.create(
        user=email.user,
        email=email,
        item_name=label_data["item_name"],
        platform=label_data["platform"],
        carrier=label_data["carrier"],
        label_name=label_name,
        postage_deadline=label_data["postage_deadline"],
    )


def save_custom_label(
    pdf_writer: PdfWriter, carrier: str, item_name: str
) -> str | None:
    """
    Saves the shipping label PDF to the specified directory, ensuring the filename is unique.

    Args:
        pdf_writer (PdfWriter): The PdfWriter object containing the modified PDF content.
        carrier (str): The name of the carrier.
        item_name (str): The name of the item.
    """
    try:
        directory = os.path.join(MEDIA_ROOT, "labels")
        label_name = f"{carrier}_{item_name}.pdf"
        n = 1

        while os.path.exists(os.path.join(directory, label_name)):
            label_name = f"{carrier}_{item_name}({n}).pdf"
            n += 1

        with open(os.path.join(directory, label_name), "wb") as f:
            pdf_writer.write(f)

        return label_name

    except FileNotFoundError as e:
        LOGGER.error(f"Directory not found while saving the label: {str(e)}")
        return None
    except IOError as e:
        LOGGER.error(f"IO error occurred while saving the label: {str(e)}")
        return None
    except Exception as e:
        LOGGER.error(f"An unexpected error occurred while saving the label: {str(e)}")
        return None


def is_shipping_label(subject: str) -> bool:
    """
    Determines if the email contains a shipping label based on specific keywords and date patterns.

    Args:
        subject (str): The subject of the email.

    Returns:
        bool: True if the email contains a shipping label, False otherwise.
    """
    for keywords in REQUIRED_SUBJECT_KEYWORDS:
        if all(keyword in subject for keyword in keywords):
            for date_pattern in DATE_PATTERNS:
                if re.search(date_pattern, subject):
                    return True

    return False


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
