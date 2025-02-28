![](https://aomail.ai/aomail-inbox-gif-v2.gif)


# 📧 Aomail - Open Source Email Management

> An intelligent, open-source email management platform with AI capabilities. Use our [hosted version](https://app.aomail.ai) or self-host for complete control.
>
> 🌐 Website: [https://aomail.ai](https://aomail.ai)
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


<div align="center">

## 🚀 Ready to Get Started?

Try Aomail for free today and experience the future of email management.  
No credit card required.

[<img src="https://img.shields.io/badge/Sign_Up_Now-4A90E2?style=for-the-badge&logo=mail&logoColor=white" alt="Sign Up Now" height="40"/>](https://app.aomail.ai/signup)

</div>

## 🛠 Self-Hosting Guide

⚠️ **Compatibility Note**: Tested on WSL 2, Docker Desktop, and Debian servers. Other platforms may work but are untested.

### Prerequisites

**Required Services:**
- Gemini API
- Google OAuth

**Optional Services:**
- Google PubSub
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

## 🔧 Troubleshooting


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

 
## ❓ Frequently Asked Questions

### Security & Privacy

**Q: How do you ensure email security?**  
> A: We take security seriously:
> - All emails are encrypted and stored in a secure database
> - Our code is open source and publicly auditable
> - We've received a 9.7/10 security rating from TAC Security
> - No AI training is performed on your data

[Download Security Assessment Report](https://aomail.ai/aomail-tac-security-tier2-assessment.pdf)

**Q: How do you handle AI and data privacy?**  
> A: We prioritize your privacy:
> - No training is performed on your emails
> - We use stateless API calls to LLM providers
> - You can choose your preferred LLM provider:
  - [Gemini](https://ai.google.dev/gemini-api/terms#paid-services)
  - [Anthropic](https://www.anthropic.com/legal/consumer-terms)
  - [Mistral](https://mistral.ai/en/terms#data-processing-agreement)

### Account & Pricing

**Q: How long is the free trial?**  
> A: We offer a 14-day free trial.

**Q: Do I need to provide credit card information?**  
> A: No, you can start your free trial without entering any payment information.

### Email Integration

**Q: Which email providers are supported?**  
> A: Currently, we support:
> - Gmail
> - Outlook (beta)

**Q: How does mailbox linking work?**  
> A: We use industry-standard OAuth 2.0 for secure mailbox integration. [Learn more about OAuth 2.0](https://oauth.net/2/)

**Q: How do I get unlimited access to Aomail?**  
> A: You'll need to set up the admin dashboard to give yourself unlimited access. Check out our [admin dashboard repository](https://github.com/aomail-ai/aomail-admin-dashboard) for setup instructions.


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

## 🪲 Issue Reporting
- **Feature Requests**: Use our [feature request template](https://github.com/aomail-ai/aomail-app/issues/new?template=feature-request.yml) with `enhancement` + `backend`/`frontend` labels
- **Bug Reports**: Use our [bug report template](https://github.com/aomail-ai/aomail-app/issues/new?template=bug_report.yml) with `bug` + `backend`/`frontend` labels