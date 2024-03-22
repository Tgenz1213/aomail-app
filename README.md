# Repository for MailAssistant

## Quick Setup

# Ask Théo HUBERT for your credentials
1) setup the tunel with Wireguard
2) setup VSC and wsl to connect to the server via ssh
3) connect to database to check

# COMMON ISSUES
**M365 Licenses Error:**
If you encounter the following error while accessing data:
```json
{
  "error": {
    "code": "MailboxNotEnabledForRESTAPI",
    "message": "The mailbox is either inactive, soft-deleted, or is hosted on-premise."
  }
}
```
This error typically indicates that your account does not have the proper license to access the requested data thus you have to pay a M365 license.

# Test Reply Later Gmail
curl -X GET \
     -H "Authorization: Bearer access_token" \
     -H "email: test.mailassistantprod@gmail.com" \
     "https://augustin.aochange.com/MailAssistant/api/save_last_mail"

# Test add email in DB
curl -X GET \
     -H "Authorization: Bearer access_token" \
     -H "email: test.mailassistantprod@gmail.com" \
     "https://augustin.aochange.com/MailAssistant/api/save_last_mail_outlook"