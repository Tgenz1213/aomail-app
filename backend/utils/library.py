import base64
import re

from bs4 import BeautifulSoup

import sys
sys.path.append('/Users/shost/Documents/MailAssistant/MailAssistant_project/MailAssistant')

# uses BeautifulSoup to clear html from text
def html_clear(text):
    # Utiliser BeautifulSoup pour parser le HTML et extraire le texte
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text('\n') 
    return text

# if mime_type is correct, text is extracted from email body
def get_text_from_mail(mime_type,part,decoded_data_temp):
    # The email body is in the "data" of the "body" payload
    data = part['body']["data"]
    # The data is base64url encoded. We can decode it and print the email body
    data = data.replace("-","+").replace("_","/")
    decoded_data_temp = base64.b64decode(data)
    if mime_type== "text/html":
        decoded_data_temp = html_clear(decoded_data_temp)
        # print("get_text_from_mail: ",decoded_data_temp)
    return decoded_data_temp

# True/False from text input if html is present
def contains_html(text):
    if isinstance(text, bytes):
        text = text.decode('utf-8', 'ignore')
    html_patterns = [
        r'<[a-z]+>',         # Opening tags
        r'</[a-z]+>',        # Closing tags
        r'&[a-z]+;',         # HTML entities
        r'<!DOCTYPE html>'   # DOCTYPE declaration
    ]
    
    for pattern in html_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

# checks the type of new text added and adjusts it if necessary before putting it inside text_final
def concat_text(text_final,text):
    if text_final:
        if type(text)==bytes:
            text_str = text.decode('utf-8')
        else:
            text_str = text
        text_final+=text_str
    else:
        if type(text)==bytes:
            text_str = text.decode('utf-8')
        else:
            text_str = text
        text_final=text_str
    return text_final

# if email is structured in "multiparts", goes through all to get the email body
def process_part(part,plaintext_var):
    mime_type = part['mimeType']
    # print("mime_type: ",mime_type,plaintext_var[0])
    decoded_data = None

    if mime_type == "text/plain":
        decoded_data = get_text_from_mail(mime_type,part,decoded_data)
        # if decoded_data != None and decoded_data != "" and decoded_data != b'':
        if contains_html(decoded_data):
            decoded_data = get_text_from_mail('text/html',part,decoded_data.decode('utf-8'))
        # elif decoded_data and decoded_data.strip() not in ["", " ", " b'' ",b'']:
        elif decoded_data and decoded_data.strip() not in ["",b'']:
            # print('decoded_data_test: ',decoded_data,'___',decoded_data.strip())
            plaintext_var[0] = 1
        # else:
        #     decoded_data = None
    elif mime_type == "text/html" and plaintext_var[0]==0:
    # if mime_type == "text/html" or (mime_type == "text/plain" and not decoded_data):
        decoded_data = get_text_from_mail(mime_type,part,decoded_data)
    elif "multipart/" in mime_type:
        # For every subpart, call this function
        subpart_datas = {'html':None,'plain':None}
        for subpart in part['parts']:
            subpart_data = process_part(subpart,plaintext_var)
            if subpart_data:
                if plaintext_var[0]==0:
                    subpart_datas['html']=subpart_data
                else:
                    subpart_datas['plain']=subpart_data
        if subpart_datas:
            # print("subpart_datas: ",subpart_datas)
            if plaintext_var[0]==0:
                subpart_data = subpart_datas['html']
            else:
                subpart_data = subpart_datas['plain']
            
            decoded_data = concat_text(decoded_data,subpart_data)
            # deletes unwanted remnant of images ([images])
            if plaintext_var[0]==1 and decoded_data:
                decoded_data = re.sub(r'\[image[^\]]+\]\s*<\S+>','',decoded_data)
                decoded_data = re.sub(r'\[image[^\]]+\]','',decoded_data)
    # print("decoded_data_process: ",decoded_data)
    return decoded_data

# removes greetings and sign-offs
def preprocess_email(email_content):
    # List of common greetings and sign-offs
    greetings = ["Bonjour", "Hello", "Hi", "Dear", "Salut"]
    sign_offs = ["Regards", "Sincerely", "Best regards", "Cordially", "Yours truly", "Cordialement", "Bien à vous"]
    
    # Create patterns to identify lines with greetings and sign-offs
    greeting_pattern = r"^\s*(" + "|".join(greetings) + r").*\n"
    sign_off_pattern = r"\n\s*(" + "|".join(sign_offs) + r").*$"
    
    # Remove greetings
    email_content = re.sub(greeting_pattern, "", email_content, flags=re.IGNORECASE | re.MULTILINE)
    
    # Remove sign-offs
    email_content = re.sub(sign_off_pattern, "", email_content, flags=re.IGNORECASE | re.MULTILINE)
    
    return email_content.strip()
