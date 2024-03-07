"""
Utility Functions for Email Processing.

This file contains utility functions for processing email content, including clearing HTML, extracting text, checking for HTML presence, concatenating text, processing email parts, and preprocessing email content.
"""
import sys
import os

# Assuming library.py is in the MailAssistant/backend/MailAssistant directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from models import Category
import re
import base64
from bs4 import BeautifulSoup


######################## UTILS FOR OTHER FUNCTIONS ########################
def html_clear(text):
    """Uses BeautifulSoup to clear HTML tags from the given text."""
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text("\n")
    return text


def get_text_from_mail(mime_type, part, decoded_data_temp):
    """If the MIME type is correct, extracts text from the email body."""
    data = part["body"]["data"]
    data = data.replace("-", "+").replace("_", "/")
    decoded_data_temp = base64.b64decode(data)
    if mime_type == "text/html":
        decoded_data_temp = html_clear(decoded_data_temp)
    return decoded_data_temp


def contains_html(text):
    """Returns True if the given text contains HTML, False otherwise."""
    if isinstance(text, bytes):
        text = text.decode("utf-8", "ignore")
    html_patterns = [r"<[a-z]+>", r"</[a-z]+>", r"&[a-z]+;", r"<!DOCTYPE html>"]

    for pattern in html_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def concat_text(text_final, text):
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


def process_part(part, plaintext_var):
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
                decoded_data = re.sub(r"\[image[^\]]+\]\s*<\S+>", "", decoded_data)
                decoded_data = re.sub(r"\[image[^\]]+\]", "", decoded_data)
    return decoded_data


def preprocess_email(email_content):
    """Removes common greetings and sign-offs from the email content."""
    greetings = ["Bonjour", "Hello", "Hi", "Dear", "Salut"]
    sign_offs = [
        "Regards",
        "Sincerely",
        "Best regards",
        "Cordially",
        "Yours truly",
        "Cordialement",
        "Bien à vous",
    ]

    greeting_pattern = r"^\s*(" + "|".join(greetings) + r").*\n"
    sign_off_pattern = r"\n\s*(" + "|".join(sign_offs) + r").*$"

    email_content = re.sub(
        greeting_pattern, "", email_content, flags=re.IGNORECASE | re.MULTILINE
    )
    email_content = re.sub(
        sign_off_pattern, "", email_content, flags=re.IGNORECASE | re.MULTILINE
    )

    return email_content.strip()


def count_corrections(
    original_subject, original_body, corrected_subject, corrected_body
):
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


####################################################################
######################## UNDER CONSTRUCTION ########################
####################################################################


# strips text of unnecessary spacings
def format_mail(text):
    # Delete links
    text = re.sub(r"<http[^>]+>", "", text)
    # Delete patterns like "[image: ...]"
    text = re.sub(r"\[image:[^\]]+\]", "", text)
    # Convert Windows line endings to Unix line endings
    text = text.replace("\r\n", "\n")
    # Remove spaces at the start and end of each line
    text = "\n".join(line.strip() for line in text.split("\n"))
    # Delete multiple spaces
    text = re.sub(r" +", " ", text)
    # Reduce multiple consecutive newlines to two newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text


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


def get_db_categories(current_user):
    # Query categories specific to the current user from the database.
    categories = Category.objects.filter(user=current_user)

    # Construct the category_list dictionary from the queried data.
    category_list = {category.name: category.description for category in categories}

    return category_list


def separate_name_email(s):
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
        return None, None
