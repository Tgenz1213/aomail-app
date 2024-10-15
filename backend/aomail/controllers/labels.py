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
from aomail.constants import ALLOWED_PLANS, GOOGLE, MEDIA_ROOT, MICROSOFT
from aomail.email_providers.google import email_operations as email_operations_google
from aomail.models import Attachment, Email, Label
from aomail.utils.security import subscription


LOGGER = logging.getLogger(__name__)
REQUIRED_SUBJECT_KEYWORDS = [
    ["shipping label", "use by"],
    ["Bordereau d'envoi", "à utiliser avant le"],
    ["verzendlabel", "Uiterste verzenddatum:"],
    ["Etiqueta de envío", "Utilizar antes del"],
]
DATE_PATTERNS = [
    r"\b\d{2}/\d{2}/\d{4} \d{2}:\d{2}\s*[APM]{2}\b",
    r"\b\d{4}-\d{2}-\d{2} \d{2}:\d{2}\b",
    r"\b\d{2}/\d{2}/\d{4} \d{2}:\d{2}\b",
]
CARRIER_PATTERNS = [
    re.compile(
        r"3\.\s*Drop the parcel off\s*</strong>.*?in the\s*(.*?)\s*drop-off point of your choice\.\s*</p>",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"3\.\s*D\xe9pose le colis.*?dans n'importe\s*quel\s*point\s*(.*?)\s*\.\s*</p>",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"3\.\s*Geef het pakket af bij een\s*</strong>.*?\s*(.*?)\s*afgiftepunt naar keuze\.\s*</p>",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"3\.\s*Entrega el paquete en el punto de entrega\s*</strong>.*?\s*(.*?)\s*(?:de tu elección|más cercano)\.\s*</p>",
        re.IGNORECASE | re.DOTALL,
    ),
]
ITEM_NAME_PATTERNS = [
    re.compile(
        r"<strong>\s*Article\s*:\s*</strong>.*?<td[^>]*>\s*(.*?)\s*</td>",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"<strong>\s*Bestelling\s*:\s*</strong>.*?<td[^>]*>\s*(.*?)\s*</td>",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"<strong>\s*Item\s*:\s*</strong>.*?<td[^>]*>\s*(.*?)\s*</td>",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"<strong>\s*Pedido\s*:\s*</strong>.*?<td[^>]*>\s*(.*?)\s*</td>",
        re.IGNORECASE | re.DOTALL,
    ),
]
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


def process_label(email_address: str, subject: str, email_entry: Email):
    """
    Processes the email label data and creates a shipping label.

    Args:
        email_address (str): The email address of the sender.
        subject (str): The subject of the email.
        email_entry (Email): An instance of the Email class containing email details.
    """
    label_data = extract_label_data(email_address, subject, email_entry.html_content)
    create_shipping_label(email_entry, label_data)


def extract_label_data(email_address: str, subject: str, body: str) -> dict:
    """
    Extracts shipping label information such as carrier name, item name, and postage deadline from the email body and subject.

    Args:
        email_address (str): The email address of the sender.
        subject (str): The subject of the email.
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

    for date_pattern in DATE_PATTERNS:
        date_match = re.search(date_pattern, subject)
        if date_match:
            date_str = date_match.group()
            try:
                if "AM" in date_str or "PM" in date_str:
                    naive_dt = datetime.datetime.strptime(date_str, "%d/%m/%Y %I:%M %p")
                elif len(date_str) > 10 and ":" in date_str:
                    if "-" in date_str:
                        naive_dt = datetime.datetime.strptime(
                            date_str, "%Y-%m-%d %H:%M"
                        )
                    else:
                        naive_dt = datetime.datetime.strptime(
                            date_str, "%d/%m/%Y %H:%M"
                        )
                else:
                    naive_dt = datetime.datetime.strptime(date_str, "%d/%m/%Y")

                aware_dt = timezone.make_aware(
                    naive_dt, timezone.get_current_timezone()
                )
                data["postage_deadline"] = aware_dt.isoformat()
                break
            except ValueError:
                LOGGER.error(f"Date format error: {date_str}")

    if not data["carrier"] or data["carrier"] not in CARRIER_NAMES:
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
            item_name = re.sub(
                r"<br\s*/?>\s*$", "", item_match.group(1).strip()
            ).strip()
            data["item_name"] = item_name
            break

    for platform in ECOMMERCE_PLATFORMS:
        if platform in email_address:
            data["platform"] = platform
            break

    return data


def create_shipping_label(email: Email, label_data: dict[str, str]):
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
    item_lines = re.split(r"<br\s*/?>", label_data["item_name"].strip())

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

            for line in item_lines:
                line = line.strip()
                x = (
                    pdf_reader.pages[0].mediabox.width
                    / (4 if label_data["carrier"] == "mondial_relay" else (3 / 2))
                    - canvas_object.stringWidth(line) / 2
                )
                if line:
                    canvas_object.drawString(x, y, line)
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
                    - canvas_object.stringWidth(item_lines[0]) / 2,
                    2 / 3 * pdf_reader.pages[0].mediabox.height
                    - 0.034 * pdf_reader.pages[0].mediabox.height,
                )
            for line in item_lines:
                line = line.strip()
                if line:
                    canvas_object.drawString(x, y, line)
                    y -= 0.018 * pdf_reader.pages[0].mediabox.height

        canvas_object.save()
        packet.seek(0)
        new_pdf = PdfReader(packet)
        page.merge_page(new_pdf.pages[0])
        pdf_writer.add_page(page)

    label_data["item_name"] = label_data["item_name"].replace("<br/>", " + ")
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


def save_custom_label(pdf_writer: PdfWriter, carrier: str, item_name: str) -> str:
    """
    Saves the shipping label PDF to the specified directory, ensuring the filename is unique.

    Args:
        pdf_writer (PdfWriter): The PdfWriter object containing the modified PDF content.
        carrier (str): The name of the carrier.
        item_name (str): The name of the item.

    Returns:
        str: The name of the saved label file, or None if an error occurred.
    """
    try:
        directory = os.path.join(MEDIA_ROOT, "labels")
        os.makedirs(directory, exist_ok=True)

        label_name = f"{carrier}_{item_name}.pdf"
        n = 1

        while os.path.exists(os.path.join(directory, label_name)):
            label_name = f"{carrier}_{item_name}({n}).pdf"
            n += 1

        if len(label_name) > 246:
            label_name = label_name[:246] + ".pdf"

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
@subscription([ALLOWED_PLANS])
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
        ids = parameters.get("ids", [])

        if not ids:
            return Response(
                {"error": "No label IDs provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        labels = Label.objects.filter(id__in=ids, user=user)
        if labels.count() != len(ids):
            return Response(
                {
                    "error": "One or more labels not found or not associated with this user"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        for label in labels:
            label_path = os.path.join(MEDIA_ROOT, "labels", label.label_name)
            if os.path.exists(label_path):
                os.remove(label_path)
            label.delete()

        return Response(
            {"message": "Labels deleted successfully"}, status=status.HTTP_200_OK
        )

    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON in request body"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        LOGGER.error(f"Error when deleting labels: {str(e)}")
        return Response(
            {"error": "An unexpected error occurred"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
