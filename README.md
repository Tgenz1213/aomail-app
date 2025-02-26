# 📧 Aomail - Open Source Email Management

> An intelligent, open-source email management platform with AI capabilities. Use our [hosted version](https://app.aomail.ai) or self-host for complete control.
>
> 📧 Support: aomailaipro@gmail.com
  

<div align="center">

[![Discord](https://discord.com/api/guilds/1303091825900257341/widget.png?style=shield)](https://discord.com/invite/JxbPZNDd)

</div>

## ✨ Features

### Core Features
- **📧 Email Provider Integration**
  - Labels are replicated on Gmail & Outlook
  - Link multiple accounts (premium plan)
  
- **🤖 AI-Powered Tools**
  - Smart categorization with custom rules
  - AI chat assistant for composition and replies
  - Customizable AI agents
  - Smart email categorization with summaries
  - Search emails or ask AI questions (beta)

- **📊 Analytics & Management**
  - Usage analytics and insights
  - Multi-account dashboard


### 🚀 Coming Soon
- **AI Custom Rules**: Automatic forwarding and smart replies
- **Platform Integration**: Discord & Slack connectivity with smart summaries
- **LLM Choice**: Support for OpenAI, Anthropic, Llama, Mistral

## 🛠 Self-Hosting Guide

⚠️ **Compatibility Note**: Tested on WSL 2, Docker Desktop, and Debian servers. Other platforms may work but are untested.

### Prerequisites

**Required Services:**
- Gemini API
- Google OAuth
- Google PubSub

**Optional Services:**
- Microsoft Azure
- Stripe

### Quick Start

1. **Clone and Install:**
```bash
git clone https://github.com/aomail-ai/aomail-app
cd aomail-app
cd frontend && npm install
cd .. && cp backend/.env.example backend/.env
```

2. **Google Project Setup:**

    1 Generate a Gemini API key [here](https://console.cloud.google.com/apis/credentials). You also need to enable Gemini API [here](https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com)
    2 Create a [Google Cloud Console Project](https://console.cloud.google.com/projectcreate)
    3 Configure [OAuth screen](https://console.cloud.google.com/apis/credentials) with scopes from `/backend/aomail/constants.py`



   3. Set authorized origins: `http://localhost`
   4. Set redirect URIs:
      - `http://localhost/signup-link`
      - `http://localhost/settings`

   5. **PubSub Setup** (Optional):
      - **For Local Development**:
        1. Install and run [Google Cloud PubSub emulator](https://cloud.google.com/pubsub/docs/emulator)
        2. Configure local webhook endpoint
      
      - **For Production**:
        1. Create a new PubSub topic in Google Cloud Console ([Create topic](https://console.cloud.google.com/cloudpubsub/topic/list))
        2. Configure webhook URL: `https://your-domain/google/receive_mail_notifications/`
        3. Set up push subscription with your webhook


3. **Configure Environment:**
Required variables in `.env`:
```plaintext
# LLM API KEYS
GEMINI_API_KEY=""

# ENCRYPTION KEYS
SOCIAL_API_REFRESH_TOKEN_KEY=""
EMAIL_ONE_LINE_SUMMARY_KEY=""
EMAIL_SHORT_SUMMARY_KEY=""
EMAIL_HTML_CONTENT_KEY=""

# DJANGO CREDENTIALS
DJANGO_SECRET_KEY=""

# Google Configuration (if using Gmail)
GOOGLE_PROJECT_ID=""
GOOGLE_CLIENT_ID=""
GOOGLE_CLIENT_SECRET=""

# Microsoft Configuration (if using Outlook)
MICROSOFT_CLIENT_ID=""
MICROSOFT_CLIENT_SECRET=""
MICROSOFT_TENANT_ID=""
MICROSOFT_CLIENT_STATE=""
```

4. **Launch Application:**
```bash
chmod +x start.sh
./start.sh
```
Access at [http://localhost:8090/](http://localhost:8090/)

## 🔧 Frequently Asked Questions & Troubleshooting

### How do I get unlimited access to Aomail?
You need to setup the admin dashboard to give yourself unlimited access. Check out our admin dashboard repository:
https://github.com/aomail-ai/aomail-admin-dashboard

### How do I fix database migration issues?
If you encounter database migration problems, run these commands:
```bash
sudo rm -fr backend/aomail/migrations
docker exec -it aomail_project-backend_dev-1 python manage.py makemigrations --empty aomail
./start.sh
```

### Why isn't my app starting?
Common port conflict issues:
- Check for any running containers using the same ports
- Look for conflicts between production/development containers
- Try updating ports in `start.sh` if needed

### How do I add a new subdomain?
Follow these steps in order:
1. Configure your DNS record
2. Update the reverse proxy settings
3. Open required port: `sudo ufw allow PORT_NUMBER`
4. Add the subdomain to `ALLOWED_HOSTS` in start.sh

 

## 🤝 Contributing

1. Set up development environment (recommended):
```bash
python3 -m venv py_env
source py_env/bin/activate
pip install -r requirements.txt
```

2. Fork repository
3. Create feature branch
4. Submit pull request

### Issue Reporting
- **Features**: Create issue with `enhancement` + `backend`/`frontend` labels
- **Bugs**: Create issue with `bug` + `backend`/`frontend` labels
 