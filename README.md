# Aomail Web Application

## Getting started with self-hosting

External services:
- Gemini 
- Google OAuth
- Google PubSub
Optional services:
- Stripe
- Microsoft Azure

 
```bash
git clone https://github.com/aomail-ai/aomail-app
cd aomail-app
cp backend/.env.example backend/.env
```
Fill the .env file with your API keys and secrets.

required environment variables:
# todo: putt all links to generate keys
GEMINI_API_KEY
for encryption keys: use ```python3 -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'``` to generate a key 
    SOCIAL_API_REFRESH_TOKEN_KEY
    EMAIL_ONE_LINE_SUMMARY_KEY
    EMAIL_SHORT_SUMMARY_KEY
    EMAIL_HTML_CONTENT_KEY
DJANGO_SECRET_KEY
DJANGO_DB_USER
DJANGO_DB_PASSWORD

If you are using Gmail setup
GOOGLE_TOPIC_NAME
GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET

If you are using Microsoft Azure setup
MICROSOFT_CLIENT_ID 
MICROSOFT_CLIENT_SECRET 
MICROSOFT_TENANT_ID= 
MICROSOFT_CLIENT_STATE 



Google OAuth config

1) create a new project in google cloud console
https://console.cloud.google.com/projectcreate

2) Add all required scopes you can find them in /backend/aomail/constants.py
Link for OAuth consent screen:
https://console.cloud.google.com/projectselector2/auth/overview

Authorized JavaScript origins:
http://localhost:8080

Authorized redirect URIs
http://localhost/signup-link
http://localhost/settings
Authorized JavaScript origins:
http://localhost:8080

Authorized redirect URIs
http://localhost/signup-link
http://localhost/settings

3) Create a pubsub topic in google cloud console



## Start the application
update the variables in the start.sh 
update the NODE_ENV variable to "development" or "production"
```bash
chmod +x start.sh
```

```bash
./start.sh
```

if in dev: go to http://localhost:8080/

if in prod: go to http://localhost:4173/





# Debugging database migrations errors
```bash
sudo rm -fr backend/aomail/migrations
docker exec -it {username}_project-backend-1 python manage.py makemigrations --empty aomail
./start_{username}_dev.sh
```


# Adding a New Subdomain
1) Add the subdomain in the DNS server.
2) Add the subdomain to your reverse proxy server.
3) Open the required port: `sudo ufw allow PORT_NUMBER` 
4) Update vue.config.js: Add the new domain to the list of allowedHosts.


# check this repo if you want to give yourself unlimited access to Aomail
https://github.com/aomail-ai/aomail-admin-dashboard