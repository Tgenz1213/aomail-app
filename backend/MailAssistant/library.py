"""
Utility Functions for Email Processing.

This file contains utility functions for processing email content, including clearing HTML, extracting text, checking for HTML presence, concatenating text, processing email parts, and preprocessing email content.
"""
import base64
import re
from bs4 import BeautifulSoup


def html_clear(text):
    """Uses BeautifulSoup to clear HTML tags from the given text."""
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text('\n') 
    return text


def get_text_from_mail(mime_type, part, decoded_data_temp):
    """If the MIME type is correct, extracts text from the email body."""
    data = part['body']["data"]
    data = data.replace("-","+").replace("_","/")
    decoded_data_temp = base64.b64decode(data)
    if mime_type == "text/html":
        decoded_data_temp = html_clear(decoded_data_temp)
    return decoded_data_temp


def contains_html(text):
    """Returns True if the given text contains HTML, False otherwise."""
    if isinstance(text, bytes):
        text = text.decode('utf-8', 'ignore')
    html_patterns = [
        r'<[a-z]+>',
        r'</[a-z]+>',
        r'&[a-z]+;',
        r'<!DOCTYPE html>'
    ]
    
    for pattern in html_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def concat_text(text_final, text):
    """Checks the type of new text added and adjusts it if necessary before concatenating it to the final text."""
    if text_final:
        if type(text) == bytes:
            text_str = text.decode('utf-8')
        else:
            text_str = text
        text_final += text_str
    else:
        if type(text) == bytes:
            text_str = text.decode('utf-8')
        else:
            text_str = text
        text_final = text_str
    return text_final


def process_part(part, plaintext_var):
    """Processes each part of an email, extracts the email body, and handles multipart emails."""
    mime_type = part['mimeType']
    decoded_data = None

    if mime_type == "text/plain":
        decoded_data = get_text_from_mail(mime_type, part, decoded_data)
        if contains_html(decoded_data):
            decoded_data = get_text_from_mail('text/html', part, decoded_data.decode('utf-8'))
        elif decoded_data and decoded_data.strip() not in ["", b'']:
            plaintext_var[0] = 1
    elif mime_type == "text/html" and plaintext_var[0] == 0:
        decoded_data = get_text_from_mail(mime_type, part, decoded_data)
    elif "multipart/" in mime_type:
        subpart_datas = {'html': None, 'plain': None}
        for subpart in part['parts']:
            subpart_data = process_part(subpart, plaintext_var)
            if subpart_data:
                if plaintext_var[0] == 0:
                    subpart_datas['html'] = subpart_data
                else:
                    subpart_datas['plain'] = subpart_data
        if subpart_datas:
            if plaintext_var[0] == 0:
                subpart_data = subpart_datas['html']
            else:
                subpart_data = subpart_datas['plain']
            
            decoded_data = concat_text(decoded_data, subpart_data)
            if plaintext_var[0] == 1 and decoded_data:
                decoded_data = re.sub(r'\[image[^\]]+\]\s*<\S+>', '', decoded_data)
                decoded_data = re.sub(r'\[image[^\]]+\]', '', decoded_data)
    return decoded_data


'''def preprocess_email(email_content):
    """Removes common greetings and sign-offs from the email content."""
    greetings = ["Bonjour", "Hello", "Hi", "Dear", "Salut"]
    sign_offs = ["Regards", "Sincerely", "Best regards", "Cordially", "Yours truly", "Cordialement", "Bien à vous"]
    
    greeting_pattern = r"^\s*(" + "|".join(greetings) + r").*\n"
    sign_off_pattern = r"\n\s*(" + "|".join(sign_offs) + r").*$"
    
    email_content = re.sub(greeting_pattern, "", email_content, flags=re.IGNORECASE | re.MULTILINE)
    email_content = re.sub(sign_off_pattern, "", email_content, flags=re.IGNORECASE | re.MULTILINE)
    
    return email_content.strip()'''