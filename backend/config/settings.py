"""
Mail Assistant Project - Django settings

QUICK-START DEVELOPMENT SETTINGS - UNSUITABLE FOR PRODUCTION
"""

import json
from datetime import timedelta
from aomail.constants import (
    BACKEND_DIR,
    EMAIL_NO_REPLY,
    EMAIL_NO_REPLY_PASSWORD,
    HOSTS_URLS,
    CORS_ALLOWED_ORIGINS,
)


######################## CHECKLIST FOR PRODUCTION ########################
"""
1. Debug Mode:
   - Turn off debug mode in production.
     DEBUG = False

2. Logging Configuration:
   - Set appropriate logging configurations for production.
   - Avoid logging sensitive information like passwords or tokens.
   - Adjust log levels and handlers for effective monitoring.

3. Backup and Recovery:
   - Implement a backup strategy for the database and logging files.
   - Set up a reliable backup server for data recovery.

4. Setup Critical Auto Email:
   - Establish monitoring systems to detect critical issues.
   - Configure automatic email alerts for timely response to critical alerts.
"""


######################## CREDENTIALS ########################
CONFIG = json.load(open("creds/django_creds.json"))
SECRET_KEY = CONFIG["secret_key"]
BACKEND_LOG_PATH = "backend.log"
CUSTOM_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


######################## GENERAL CONFIGURATION ########################
ROOT_URLCONF = "config.urls"
ASGI_APPLICATION = "config.asgi.application"
SESSION_ENGINE = "django.contrib.sessions.backends.db"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
STATIC_URL = "static/"
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# ----------------------- DJANGO DEPENDENCIES -----------------------#
INSTALLED_APPS = [
    "django_extensions",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "MailAssistant",
    "aomail.ai_providers",
    "aomail.controllers",
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "rest_framework.authtoken",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "django_crontab",
]
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.CommonMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [f"{BACKEND_DIR}/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ----------------------- LOGGING CONFIGURATION -----------------------#
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "basic",
            "level": "INFO",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": BACKEND_LOG_PATH,
            "level": "INFO",
            "formatter": "json",
        },
    },
    "loggers": {
        "django": {  # Exclude Django's logs
            "handlers": ["console"],
            "propagate": False,
        },
        "httpx": {  # Exclude httpx logs
            "handlers": ["console"],
            "propagate": False,
        },
        "": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
    },
    "formatters": {
        "basic": {
            "format": "{levelname} - {message}",
            "style": "{",
        },
        "verbose": {
            "format": "{asctime} | {name}.py | Line {lineno} | {levelname} - {message}",
            "style": "{",
            "datefmt": CUSTOM_DATE_FORMAT,
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s | %(name)s.py | Line %(lineno)d | %(levelname)s - %(message)s",
            "datefmt": CUSTOM_DATE_FORMAT,
        },
    },
}


######################## SECURITY ########################
DEBUG = True
ALLOWED_HOSTS = HOSTS_URLS
CORS_ALLOWED_ORIGINS = CORS_ALLOWED_ORIGINS

# ----------------------- DATABASE CONFIGURATION -----------------------#
DATABASES = CONFIG["database_conf"]

# ----------------------- PASSWORD RESET CONFIGURATION -----------------------#
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = EMAIL_NO_REPLY
EMAIL_HOST_PASSWORD = EMAIL_NO_REPLY_PASSWORD

# ----------------------- AUTHENTICATION SETTINGS -----------------------#
SIMPLE_JWT = {
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),  # Token expires in 1 day
    # Whether to rotate refresh tokens upon each request
    "ROTATE_REFRESH_TOKENS": False,
    "ALGORITHM": "HS256",
    "VERIFYING_KEY": None,
    "VALIDATED_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
}
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ----------------------- SCHEDULED TASKS -----------------------#
CRONJOBS = [
    (
        "0 3 * * *",
        "aomail.schedule_tasks.renew_gmail_subscriptions",
    ),
]
