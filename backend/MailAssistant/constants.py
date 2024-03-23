"""
File that stores all constants and computed paths
"""

import json
import os


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
CREDS_PATH = f"{BACKEND_DIR}/creds/"
ENV = os.environ.get("ENV")
#TOPIC_NAME = os.environ.get("TOPIC_NAME") => To subscribe to a different TOPIC (OPTIONAL)
BASE_URL = f"https://{ENV}.aochange.com/"
REDIRECT_URI = f"{BASE_URL}signup_part2"
HOSTS_URLS = [BASE_URL, f"{ENV}.aochange.com"]

######################## ARTIFICIAL INTELLIGENCE ########################
OPENAI_CREDS = json.load(open(f"{CREDS_PATH}openai_creds.json", "r"))
MISTRAL_CREDS = json.load(open(f"{CREDS_PATH}mistral_creds.json", "r"))
CLAUDE_CREDS = json.load(open(f"{CREDS_PATH}claude_creds.json", "r"))
HUMAN = "\n\nHuman: "
ASSISTANT = "Assistant:"

######################## GOOGLE API ########################
GOOGLE_READONLY_SCOPE = "https://www.googleapis.com/auth/gmail.readonly"
GOOGLE_SEND_SCOPE = "https://www.googleapis.com/auth/gmail.send"
GOOGLE_CALENDAR_READONLY_SCOPE = "https://www.googleapis.com/auth/calendar.readonly"
GOOGLE_CONTACT_READONLY_SCOPE = "https://www.googleapis.com/auth/contacts.readonly"
GOOGLE_PROFILE_SCOPE = "https://www.googleapis.com/auth/userinfo.profile"
GOOGLE_EMAIL_SCOPE = "https://www.googleapis.com/auth/userinfo.email"
GOOGLE_EMAIL_MODIFY = "https://www.googleapis.com/auth/gmail.modify"
GOOGLE_OPENID_SCOPE = "openid"
GOOGLE_OTHER_CONTACT_READONLY_SCOPE = (
    "https://www.googleapis.com/auth/contacts.other.readonly"
)
GOOGLE_SCOPES = [
    GOOGLE_READONLY_SCOPE,
    GOOGLE_SEND_SCOPE,
    GOOGLE_CALENDAR_READONLY_SCOPE,
    GOOGLE_CONTACT_READONLY_SCOPE,
    GOOGLE_PROFILE_SCOPE,
    GOOGLE_EMAIL_SCOPE,
    GOOGLE_OPENID_SCOPE,
    GOOGLE_OTHER_CONTACT_READONLY_SCOPE,
    GOOGLE_EMAIL_MODIFY,
]
GOOGLE_CREDS = f"{CREDS_PATH}google_creds.json"
GOOGLE_CONFIG = json.load(open(GOOGLE_CREDS, "r"))["web"]

######################## MICROSOFT API ########################
MICROSOFT_READ_SCOPE = "Mail.Read"
MICROSOFT_SEND_SCOPE = "Mail.Send"
MICROSOFT_CALENDAR_READ_SCOPE = "Calendars.Read"
MICROSOFT_CONTACTS_READ_SCOPE = "Contacts.Read"
MICROSOFT_EMAIL_MODIFY = "Mail.ReadWrite"
MICROSOFT_SCOPES = [
    MICROSOFT_READ_SCOPE,
    MICROSOFT_SEND_SCOPE,
    MICROSOFT_CALENDAR_READ_SCOPE,
    MICROSOFT_CONTACTS_READ_SCOPE,
    MICROSOFT_EMAIL_MODIFY,
]
MICROSOFT_CREDS = f"{CREDS_PATH}microsoft_creds.json"
MICROSOFT_CONFIG = json.load(open(MICROSOFT_CREDS, "r"))
# PRODUCTION authority
# MICROSOFT_AUTHORITY = f"https://login.microsoftonline.com/common"
# WHITE LIST authority
MICROSOFT_AUTHORITY = (
    f'https://login.microsoftonline.com/{MICROSOFT_CONFIG["tenant_id"]}'
)
GRAPH_URL = "https://graph.microsoft.com/v1.0/"
