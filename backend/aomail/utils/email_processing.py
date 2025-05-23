"""
Utility Functions for Email Processing
"""

import logging
import re
import base64
from django.db import IntegrityError
from aomail.constants import DEFAULT_CATEGORY
from aomail.models import Category, Contact
from bs4 import BeautifulSoup
from django.contrib.auth.models import User


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


def validate_email_address(email_address: str) -> bool:
    # https://stackoverflow.com/questions/8022530/how-to-check-for-valid-email-address
    return "@" in email_address


# ----------------------- CONVERTERS -----------------------#
def camel_to_snake(name: str) -> str:
    """
    Convert a camelCase string to snake_case.

    Args:
        name (str): The camelCase string to convert.

    Returns:
        str: The converted snake_case string.
    """
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    return pattern.sub("_", name).lower()


def snake_to_camel(name: str) -> str:
    """
    Convert a snake_case string to camelCase.

    Args:
        name (str): The snake_case string to convert.

    Returns:
        str: The converted camelCase string.
    """
    components = name.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


# ----------------------- NO REPLY CHECKING -----------------------#
def is_no_reply_email(sender_email: str) -> bool:
    """
    Determines if the given email address is a no-reply address.

    Args:
        sender_email (str): The email address to be checked.

    Returns:
        bool: True if the email address is identified as a no-reply address, False otherwise.
    """
    no_reply_patterns = ["no-reply", "donotreply", "noreply", "do-not-reply"]
    return any(pattern in sender_email.lower() for pattern in no_reply_patterns)


def save_email_sender(
    user: User, sender_name: str, sender_email: str, sender_id: int = None
) -> bool:
    """
    Saves the email sender's details to the database if the email is not from a no-reply address.

    Args:
        user (User): The authenticated user object.
        sender_name (str): The name of the email sender.
        sender_email (str): The email address of the sender.
        sender_id (int): The unique identifier for the sender provided by the email service.

    Returns:
        bool: True if the email sender was saved, False otherwise.
    """
    if not is_no_reply_email(sender_email):
        existing_contact = Contact.objects.filter(user=user, email=sender_email).first()

        if not existing_contact:
            try:
                Contact.objects.create(
                    email=sender_email,
                    username=sender_name,
                    user=user,
                    provider_id=sender_id,
                )
                return True
            except IntegrityError:
                return False
        else:
            return False


# ----------------------- SAVE CONTACTS AFTER SENDING EMAIL -----------------------#
def save_contacts(user: User, all_recipients: list[str]):
    """
    Saves contacts to the database if they do not already exist.

    Args:
        user (User): The authenticated user object.
        all_recipients (list[str]): A list of recipient email addresses to be saved as contacts.
    """
    for recipient_email in all_recipients:
        contact = Contact.objects.filter(email=recipient_email)

        if not is_no_reply_email(recipient_email):
            if not contact.exists():
                username = " ".join(
                    [
                        part.capitalize()
                        for part in re.split(r"[.-]", recipient_email.split("@")[0])
                        if part
                    ]
                )
                Contact.objects.create(
                    email=recipient_email, user=user, username=username
                )


######################## EMAIL DATA PROCESSING ########################
def get_db_categories(current_user: User) -> dict[str, str]:
    """
    Retrieves categories specific to the given user from the database.

    Args:
        current_user (User): The authenticated user object.

    Returns:
        dict[str, str]: A dictionary where the keys are category names and the values are category descriptions.
    """
    categories = Category.objects.filter(user=current_user)
    category_list = {category.name: category.description for category in categories}
    category_list[DEFAULT_CATEGORY] = (
        "All emails that can not be classify in any of the given categories"
    )
    return category_list


def html_clear(text: str) -> str:
    """
    Uses BeautifulSoup to clear HTML tags from the given text.

    Args:
        text (str): The HTML text to be cleared.

    Returns:
        str: The text with HTML tags removed.
    """
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text("\n")
    return text


def get_text_from_mail(mime_type: str, part: dict, decoded_data_temp: bytes) -> bytes:
    """
    If the MIME type is correct, extracts text from the email body.

    Args:
        mime_type (str): The MIME type of the email part.
        part (dict): The email part containing the body data.
        decoded_data_temp (bytes): A buffer to store the decoded data.

    Returns:
        bytes: The decoded text from the email body.
    """
    data: str = part["body"]["data"]
    data = data.replace("-", "+").replace("_", "/")
    decoded_data_temp = base64.b64decode(data)
    if mime_type == "text/html":
        decoded_data_temp = html_clear(decoded_data_temp).encode()
    return decoded_data_temp


def contains_html(text: str | bytes) -> bool:
    """
    Returns True if the given text contains HTML, False otherwise.

    Args:
        text (str | bytes): The text to be checked for HTML content.

    Returns:
        bool: True if the text contains HTML tags or entities, False otherwise.
    """
    if isinstance(text, bytes):
        text = text.decode("utf-8", "ignore")
    html_patterns = [r"<[a-z]+>", r"</[a-z]+>", r"&[a-z]+;", r"<!DOCTYPE html>"]

    for pattern in html_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def concat_text(text_final: str | None, text: str | bytes) -> str:
    """
    Checks the type of new text added and adjusts it if necessary before concatenating it to the final text.

    Args:
        text_final (str | None): The final text to which new text will be concatenated. It can be None initially.
        text (str | bytes): The new text to be concatenated. It can be a string or bytes.

    Returns:
        str: The concatenated text.
    """
    if text_final:
        if isinstance(text, bytes):
            text_str = text.decode("utf-8")
        else:
            text_str = text
        text_final += text_str
    else:
        if isinstance(text, bytes):
            text_str = text.decode("utf-8")
        else:
            text_str = text
        text_final = text_str
    return text_final


def process_part(part: dict, plaintext_var: list) -> str | None:
    """
    Processes each part of an email, extracts the email body, and handles multipart emails.

    Args:
        part (dict): The part of the email to be processed. It contains information such as MIME type and body data.
        plaintext_var (list): A list with a single integer element to keep track of whether plaintext has been found.

    Returns:
        str | None: The processed email body text, or None if no relevant text is found.
    """
    mime_type = part["mimeType"]
    decoded_data = None

    if mime_type == "text/plain":
        decoded_data = get_text_from_mail(mime_type, part, decoded_data)
        if contains_html(decoded_data):
            decoded_data = get_text_from_mail(
                "text/html", part, decoded_data.decode("utf-8")
            )
        elif decoded_data and decoded_data.strip() not in ["", b""]:
            plaintext_var[0] = 1
    elif mime_type == "text/html" and plaintext_var[0] == 0:
        decoded_data = get_text_from_mail(mime_type, part, decoded_data)
    elif "multipart/" in mime_type:
        subpart_datas = {"html": None, "plain": None}
        for subpart in part["parts"]:
            subpart_data = process_part(subpart, plaintext_var)
            if subpart_data:
                if plaintext_var[0] == 0:
                    subpart_datas["html"] = subpart_data
                else:
                    subpart_datas["plain"] = subpart_data
        if subpart_datas:
            if plaintext_var[0] == 0:
                subpart_data = subpart_datas["html"]
            else:
                subpart_data = subpart_datas["plain"]

            decoded_data = concat_text(decoded_data, subpart_data)
            if plaintext_var[0] == 1 and decoded_data:
                decoded_data = re.sub(r"\[image[^\]]+\]\s*<\S+>", "", decoded_data)
                decoded_data = re.sub(r"\[image[^\]]+\]", "", decoded_data)
    return decoded_data


def preprocess_email(email_content: str) -> str:
    """
    Removes unnecessary spacings, and converts line endings.

    Args:
        email_content (str): The content of the email to be preprocessed.

    Returns:
        str: The preprocessed email content with removed links, email addresses,
             unnecessary spacings, and converted line endings.
    """
    # Delete patterns like "[image: ...]"
    email_content = re.sub(r"\[image:[^\]]+\]", "", email_content)

    # Convert Windows line endings to Unix line endings
    email_content = email_content.replace("\r\n", "\n")

    # Remove spaces at the start and end of each line
    email_content = "\n".join(line.strip() for line in email_content.split("\n"))

    # Delete multiple spaces
    email_content = re.sub(r" +", " ", email_content)

    # Reduce multiple consecutive newlines to two newlines
    email_content = re.sub(r"\n{3,}", "\n\n", email_content)

    return email_content.strip()
