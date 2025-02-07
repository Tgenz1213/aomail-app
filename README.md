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
GEMINI_API_KEY
for encryption keys: use ```python3 -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'``` to generate a key 
    SOCIAL_API_REFRESH_TOKEN_KEY
    EMAIL_ONE_LINE_SUMMARY_KEY
    EMAIL_SHORT_SUMMARY_KEY
    EMAIL_HTML_CONTENT_KEY
DJANGO_SECRET_KEY
DJANGO_DB_USER
DJANGO_DB_PASSWORD

GOOGLE_TOPIC_NAME
GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET




## Start the application
update the variables in the start.sh 
update the NODE_ENV variable to "development" or "production"
```bash
chmod +x start.sh
```

```bash
./start.sh
```





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