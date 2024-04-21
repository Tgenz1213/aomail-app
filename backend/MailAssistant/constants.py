"""
File that stores all constants and computed paths
"""

import json
import os


######################## SECURITY ########################
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
CREDS_PATH = f"{BACKEND_DIR}/creds/"
ENV = os.environ.get("ENV")
# TOPIC_NAME = os.environ.get("TOPIC_NAME") => To subscribe to a different TOPIC (OPTIONAL)
BASE_URL = f"https://{ENV}.aochange.com/"
BASE_URL_MA = f"{BASE_URL}MailAssistant/"
REDIRECT_URI_SIGNUP = f"{BASE_URL}signup_part2"
REDIRECT_URI_LINK_EMAIL = f"{BASE_URL}settings"
HOSTS_URLS = [BASE_URL, f"{ENV}.aochange.com"]
ENCRYPTION_KEYS = json.load(open(f"{CREDS_PATH}encryption_keys.json"))
NO_REPLY_CREDS = json.load(open(f"{CREDS_PATH}no_reply_creds.json"))
EMAIL_NO_REPLY = NO_REPLY_CREDS["email"]
EMAIL_NO_REPLY_PASSWORD = NO_REPLY_CREDS["password"]
ADMIN_EMAIL_LIST = ["theo...", "jean...", "augustin.rolet.pro@gmail.com"]


######################## STRIPE ########################
STRIPE_CREDS = json.load(open(f"{CREDS_PATH}stripe_creds.json"))
STRIPE_SECRET_KEY = STRIPE_CREDS["secret_key"]
STRIPE_PUBLISHABLE_KEY = STRIPE_CREDS["publishable_key"]
STRIPE_PAYMENT_FAILED_URL = f"{BASE_URL}stripe/payment_failed/"
STRIPE_PAYMENT_SUCCESS_URL = f"{BASE_URL}stripe/payment_successful/"
STRIPE_PRICES = {
    "start_plan_id": {"name": "start_plan", "price": 0.0},
    "pro_plan_id": {"name": "pro_plan", "price": 0.0},
}


######################## ARTIFICIAL INTELLIGENCE ########################
OPENAI_CREDS = json.load(open(f"{CREDS_PATH}openai_creds.json"))
MISTRAL_CREDS = json.load(open(f"{CREDS_PATH}mistral_creds.json"))
CLAUDE_CREDS = json.load(open(f"{CREDS_PATH}claude_creds.json"))
LLAMA_CREDS = json.load(open(f"{CREDS_PATH}llama_creds.json"))
HUMAN = "\n\nHuman: "
ASSISTANT = "Assistant:"
IMPORTANT = "Important"
INFORMATION = "Information"
USELESS = "Useless"
DEFAULT_CATEGORY = "Others"
PHISHING_CATEGORY = "Phishing"
MAX_RETRIES = 3


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
GOOGLE_CONFIG = json.load(open(GOOGLE_CREDS))["web"]
GOOGLE_PROJECT_ID = GOOGLE_CONFIG["project_id"]
GOOGLE_TOPIC_NAME = "mail_push"
GOOGLE_PROVIDER = "Gmail"
# TODO: put the key in the creds.json!!!
GOOGLE_LISTENER_API_KEY = ""


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
MICROSOFT_CONFIG = json.load(open(MICROSOFT_CREDS))
# PRODUCTION authority
# MICROSOFT_AUTHORITY = f"https://login.microsoftonline.com/common"
# WHITE LIST authority
MICROSOFT_AUTHORITY = (
    f'https://login.microsoftonline.com/{MICROSOFT_CONFIG["tenant_id"]}'
)
GRAPH_URL = "https://graph.microsoft.com/v1.0/"
MICROSOFT_PROVIDER = "Outlook"
MICROSOFT_CLIENT_STATE = MICROSOFT_CONFIG["client_state"]
