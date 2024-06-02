"""
Utility Functions for Email Processing

TODO: 
- rename this file into utils.py
- Log important messages/errors using IP, user id, clear error name when possible
- Clean the code by adding data types.
- Improve documentation to be concise.
"""

import datetime
import logging
import re
import base64
from django.db import IntegrityError
from django.http import HttpRequest
from django.shortcuts import redirect
from MailAssistant.constants import BASE_URL, DEFAULT_CATEGORY
from .models import Category, Contact
from bs4 import BeautifulSoup
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from functools import wraps
from rest_framework.permissions import AllowAny, IsAuthenticated
from MailAssistant.models import Subscription

######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


# ----------------------- DECORATOR -----------------------#
# THIS IS USED TO CHECK IF THE USER SUBSCRIPTION IS STILL VALID
def subscription(allowed_plans):
    def decorator(view_func):
        @wraps(view_func)
        @permission_classes([IsAuthenticated])
        def _wrapped_view(request: HttpRequest, *args, **kwargs):
            user = request.user
            now = timezone.now()
            active_subscription = Subscription.objects.filter(
                user=user, end_date__gt=now, plan__in=allowed_plans
            ).exists()

            if not active_subscription:
                # TODO: Redirect to a subscription expired page with expiration date
                # explain on this page what the user can still acces (ONLY settings page)
                # explain that we will stop receiving its email in X days => according to google and microsoft (make a request to know)

                print("User does not have an active subscription.")

                #  (NOT 401 page) => TODO: change (it does not work anyway => TO debug)
                return redirect(f"{BASE_URL}not-authorized")

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator


# ----------------------- LOGGING -----------------------#
def get_ip_with_port(request: HttpRequest):
    """Returns the ip with the connection port"""
    try:
        source_port = request.META.get("SERVER_PORT", None)
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        ip_with_port = f"{ip}:{source_port}"
        return ip_with_port

    except Exception as e:
        LOGGER.error(
            f"An error occurred while generating IP with port: {str(e)}")


# ----------------------- CRYPTOGRAPHY -----------------------#
def encrypt_unsalted(encryption_key, plaintext):
    """Encrypts input plaintext"""
    aes_key = base64.b64decode(encryption_key.encode("utf-8"))
    cipher = Cipher(algorithms.AES(aes_key), modes.ECB(),
                    backend=default_backend())
    encryptor = cipher.encryptor()
    padded_plaintext = plaintext + " " * (16 - len(plaintext) % 16)
    ciphertext = (
        encryptor.update(padded_plaintext.encode("utf-8")) +
        encryptor.finalize()
    )
    ciphertext_base64 = base64.b64encode(ciphertext).decode("utf-8")
    return ciphertext_base64


def decrypt_unsalted(encryption_key, ciphertext_base64):
    """Decrypts input encrypted ciphertext"""
    aes_key = base64.b64decode(encryption_key.encode("utf-8"))
    ciphertext = base64.b64decode(ciphertext_base64.encode("utf-8"))
    cipher = Cipher(algorithms.AES(aes_key), modes.ECB(),
                    backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()
    unpadded_text = decrypted_text.rstrip()
    return unpadded_text.decode("utf-8")


def encrypt_text(plaintext: str, encryption_key: str) -> str:
    """Encrypts input plaintext with salt"""
    fernet = Fernet(encryption_key)
    encrypted_text = fernet.encrypt(plaintext.encode())
    return encrypted_text.decode()


def decrypt_text(encrypted_text: str, encryption_key: str) -> str:
    """Decrypts input encrypted with salt"""
    fernet = Fernet(encryption_key)
    decrypted_text = fernet.decrypt(encrypted_text.encode())
    return decrypted_text.decode()


# ----------------------- NO REPLY CHECKING -----------------------#
def is_no_reply_email(sender_email):
    """Returns True if the email is a no-reply address."""
    no_reply_patterns = ["no-reply", "donotreply", "noreply", "do-not-reply"]

    return any(pattern in sender_email.lower() for pattern in no_reply_patterns)


def save_email_sender(user, sender_name, sender_email, sender_id):
    """Saves the sender if the mail is relevant"""
    if not is_no_reply_email(sender_email):
        existing_contact = Contact.objects.filter(
            user=user, email=sender_email).first()

        if not existing_contact:
            try:
                Contact.objects.create(
                    email=sender_email,
                    username=sender_name,
                    user=user,
                    provider_id=sender_id,
                )
            except IntegrityError:
                pass


# ----------------------- SAVE CONTACTS AFTER SENDING EMAIL -----------------------#
def save_contacts(user, email, all_recipients):
    """Saves contacts if they do not exist"""

    for recipient_email in all_recipients:
        contact = Contact.objects.filter(email=recipient_email)

        if not is_no_reply_email(recipient_email):
            if contact.exists() == False:
                username = " ".join(
                    [
                        part.capitalize()
                        for part in re.split(r"[.-]", recipient_email.split("@")[0])
                        if part
                    ]
                )
                Contact.objects.create(
                    email=email, user=user, username=username)


######################## EMAIL DATA PROCESSING ########################
def get_db_categories(current_user) -> dict[str, str]:
    """Retrieves categories specific to the given user from the database."""
    categories = Category.objects.filter(user=current_user)
    category_list = {
        category.name: category.description for category in categories}
    category_list.pop(DEFAULT_CATEGORY)

    return category_list


def html_clear(text: str) -> str:
    """Uses BeautifulSoup to clear HTML tags from the given text."""
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text("\n")
    return text


def get_text_from_mail(mime_type: str, part: dict, decoded_data_temp: bytes) -> bytes:
    """If the MIME type is correct, extracts text from the email body."""
    data: str = part["body"]["data"]
    data = data.replace("-", "+").replace("_", "/")
    decoded_data_temp = base64.b64decode(data)
    if mime_type == "text/html":
        decoded_data_temp = html_clear(decoded_data_temp)
    return decoded_data_temp


def contains_html(text: str | bytes) -> bool:
    """Returns True if the given text contains HTML, False otherwise."""
    if isinstance(text, bytes):
        text = text.decode("utf-8", "ignore")
    html_patterns = [r"<[a-z]+>", r"</[a-z]+>",
                     r"&[a-z]+;", r"<!DOCTYPE html>"]

    for pattern in html_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def concat_text(text_final: str | None, text: str | bytes) -> str:
    """Checks the type of new text added and adjusts it if necessary before concatenating it to the final text."""
    if text_final:
        if type(text) == bytes:
            text_str = text.decode("utf-8")
        else:
            text_str = text
        text_final += text_str
    else:
        if type(text) == bytes:
            text_str = text.decode("utf-8")
        else:
            text_str = text
        text_final = text_str
    return text_final


def process_part(part: dict, plaintext_var: list) -> str | None:
    """Processes each part of an email, extracts the email body, and handles multipart emails."""
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
                decoded_data = re.sub(
                    r"\[image[^\]]+\]\s*<\S+>", "", decoded_data)
                decoded_data = re.sub(r"\[image[^\]]+\]", "", decoded_data)
    return decoded_data


def count_corrections(
    original_subject: str,
    original_body: str,
    corrected_subject: str,
    corrected_body: str,
) -> int:
    """Count and compare corrections in original and corrected texts"""

    # Splitting the original and corrected texts into words
    original_subject_words = original_subject.split()
    corrected_subject_words = corrected_subject.split()
    original_body_words = original_body.split()
    corrected_body_words = corrected_body.split()

    # Counting the differences in the subject
    subject_corrections = sum(
        1
        for orig, corr in zip(original_subject_words, corrected_subject_words)
        if orig != corr
    )

    # Counting the differences in the body
    body_corrections = sum(
        1
        for orig, corr in zip(original_body_words, corrected_body_words)
        if orig != corr
    )

    # Total corrections
    total_corrections = subject_corrections + body_corrections

    return total_corrections


def preprocess_email(email_content: str) -> str:
    """Removes links from the email content and strips text of unnecessary spacings"""
    # Remove links enclosed in <http...> or http... followed by a space
    email_content = re.sub(r"<http(.*?)>", "", email_content)
    email_content = re.sub(r"http(.*?)\ ", "", email_content)
    email_content = re.sub(r"http\S+", "", email_content)

    # rmv email addresses
    email_content = re.sub(r"<mailto:(.*?)>", "", email_content)
    email_content = re.sub(r"mailto:(.*?)\ ", "", email_content)
    # Remove email addresses containing "@"
    email_content = re.sub(
        r"<\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b>", "", email_content
    )
    email_content = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "", email_content
    )

    # Delete patterns like "[image: ...]"
    email_content = re.sub(r"\[image:[^\]]+\]", "", email_content)
    # Convert Windows line endings to Unix line endings
    email_content = email_content.replace("\r\n", "\n")
    # Remove spaces at the start and end of each line
    email_content = "\n".join(line.strip()
                              for line in email_content.split("\n"))
    # Delete multiple spaces
    email_content = re.sub(r" +", " ", email_content)
    # Reduce multiple consecutive newlines to two newlines
    email_content = re.sub(r"\n{3,}", "\n\n", email_content)

    return email_content.strip()


####################################################################
######################## UNDER CONSTRUCTION ########################
####################################################################

"""
def fill_lists(categories, percentages):
    base_categories = ["Important", "Information", "Useless"]

    # Determine which category is in the list
    first_category = categories[0]

    # Remove the category found from the base list
    base_categories.remove(first_category)

    # Construct the new categories list based on the first category
    for i in range(1, 3):
        if not categories[i]:
            categories[i] = base_categories.pop(0)
            percentages[i] = "0%"

    return categories, percentages
"""


'''def separate_name_email(s):
    """
    Separate "Name <email>" or "<email>" into name and email.

    Args:
    - s (str): Input string of format "Name <email>" or "<email>"

    Returns:
    - (str, str): (name, email). If name is not present, it returns (None, email)
    """

    # Regex pattern to capture Name and Email separately
    match = re.match(r"(?:(.*)\s)?<(.+@.+)>", s)
    if match:
        name, email = match.groups()
        return name.strip() if name else None, email
    else:
        return None, None'''
