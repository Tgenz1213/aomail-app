"""
File that stores all constants and computed paths
"""

import os

######################## SECURITY ########################
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
ENV = os.environ.get("ENV")
SOCIAL_API_REFRESH_TOKEN_KEY = os.getenv("SOCIAL_API_REFRESH_TOKEN_KEY")
EMAIL_ONE_LINE_SUMMARY_KEY = os.getenv("EMAIL_ONE_LINE_SUMMARY_KEY")
EMAIL_SHORT_SUMMARY_KEY = os.getenv("EMAIL_SHORT_SUMMARY_KEY")
EMAIL_HTML_CONTENT_KEY = os.getenv("EMAIL_HTML_CONTENT_KEY")

# ----------------------- PICTURES ------------------------#
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BACKEND_DIR, "media")

# ----------------------- URLS AND CORS -----------------------#
DOMAIN = f"https://{ENV}.aomail.ai"
BASE_URL = f"{DOMAIN}/"
BASE_URL_MA = f"{BASE_URL}aomail/"
REDIRECT_URI_SIGNUP = f"{BASE_URL}signup-link"
REDIRECT_URI_LINK_EMAIL = f"{BASE_URL}settings"
HOSTS_URLS = [BASE_URL, f"{ENV}.aomail.ai"]
CORS_ALLOWED_ORIGINS = [DOMAIN, "https://admin.aomail.ai"]

# ----------------------- EMAIL CREDS -----------------------#
EMAIL_NO_REPLY = os.getenv("EMAIL_NO_REPLY")
EMAIL_NO_REPLY_PASSWORD = os.getenv("EMAIL_NO_REPLY_PASSWORD")
EMAIL_ADMIN = os.getenv("EMAIL_ADMIN")

######################## PAYMENTS ########################
INACTIVE = "inactive"
START_PLAN = "start"
PREMIUM_PLAN = "premium"
ENTREPRISE_PLAN = "entreprise"
ALLOWED_PLANS = [START_PLAN, PREMIUM_PLAN, ENTREPRISE_PLAN]
ALLOW_ALL = ALLOWED_PLANS + [INACTIVE]

######################## ARTIFICIAL INTELLIGENCE ########################
IMPORTANT = "important"
INFORMATIVE = "informative"
USELESS = "useless"
ANSWER_REQUIRED = "Answer Required"
MIGHT_REQUIRE_ANSWER = "Might Require Answer"
NO_ANSWER_REQUIRED = "No Answer Required"
HIGHLY_RELEVANT = "Highly Relevant"
POSSIBLY_RELEVANT = "Possibly Relevant"
NOT_RELEVANT = "Not Relevant"
DEFAULT_CATEGORY = "Others"
MAX_RETRIES = 3

######################## GOOGLE API ########################
GOOGLE_READONLY_SCOPE = "https://www.googleapis.com/auth/gmail.readonly"
GOOGLE_SEND_SCOPE = "https://www.googleapis.com/auth/gmail.send"
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
    GOOGLE_CONTACT_READONLY_SCOPE,
    GOOGLE_PROFILE_SCOPE,
    GOOGLE_EMAIL_SCOPE,
    GOOGLE_OPENID_SCOPE,
    GOOGLE_OTHER_CONTACT_READONLY_SCOPE,
    GOOGLE_EMAIL_MODIFY,
]
GOOGLE_AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
GOOGLE_TOPIC_NAME = os.getenv("GOOGLE_TOPIC_NAME")
GOOGLE_WEB_CONFIG = {
    "web": {
        "client_id": GOOGLE_CLIENT_ID,
        "project_id": GOOGLE_PROJECT_ID,
        "auth_uri": GOOGLE_AUTH_URI,
        "token_uri": GOOGLE_TOKEN_URI,
        "client_secret": GOOGLE_CLIENT_SECRET,
    }
}
GOOGLE = "google"

######################## MICROSOFT API ########################
MICROSOFT_READ_SCOPE = "Mail.Read"
MICROSOFT_SEND_SCOPE = "Mail.Send"
MICROSOFT_CONTACTS_READ_SCOPE = "Contacts.Read"
MICROSOFT_EMAIL_MODIFY = "Mail.ReadWrite"
MICROSOFT_USER_READ_SCOPE = "User.Read"
MICROSOFT_MAILBOX_SETTINGS_SCOPE = "MailboxSettings.ReadWrite"
MICROSOFT_SCOPES = [
    MICROSOFT_READ_SCOPE,
    MICROSOFT_SEND_SCOPE,
    MICROSOFT_CONTACTS_READ_SCOPE,
    MICROSOFT_EMAIL_MODIFY,
    MICROSOFT_USER_READ_SCOPE,
    MICROSOFT_MAILBOX_SETTINGS_SCOPE,
]
MICROSOFT_AUTHORITY = f"https://login.microsoftonline.com/common"
GRAPH_URL = "https://graph.microsoft.com/v1.0/"
MICROSOFT_CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID")
MICROSOFT_CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET")
MICROSOFT_TENANT_ID = os.getenv("MICROSOFT_TENANT_ID")
MICROSOFT_CLIENT_STATE = os.getenv("MICROSOFT_CLIENT_STATE")
MICROSOFT = "microsoft"
