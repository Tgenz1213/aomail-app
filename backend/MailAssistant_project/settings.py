"""
Mail Assistant Project - Django settings

QUICK-START DEVELOPMENT SETTINGS - UNSUITABLE FOR PRODUCTION
"""
import json
import os
from datetime import timedelta
from pathlib import Path



######################## CHECKLIST FOR PRODUCTION ########################
"""
1. Debug Mode:
   - Turn off debug mode in production.
     DEBUG = False

2. Allowed Hosts:
   - Define a list of allowed hosts for serving the application.
   - Add your domain name(s).
     ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

3. CORS Configuration:
   - Review CORS_ALLOW_ALL_ORIGINS parameter for Cross-Origin Resource Sharing.
   - Set to False and specify allowed origins if necessary.
     CORS_ALLOW_ALL_ORIGINS = False
     CORS_ALLOWED_ORIGINS = ['https://yourfrontenddomain.com']

4. Logging Configuration:
   - Set appropriate logging configurations for production.
   - Avoid logging sensitive information like passwords or tokens.
   - Adjust log levels and handlers for effective monitoring.

5. Remove Dangerous Print:
   - Remove all print statements containing sensitive information.
   - Enhance security by minimizing unnecessary print statements.

6. Backup and Recovery:
   - Implement a backup strategy for the database and logging files.
   - Set up a reliable backup server for data recovery.

7. Setup Critical Auto Email:
   - Establish monitoring systems to detect critical issues.
   - Configure automatic email alerts for timely response to critical alerts.
"""



######################## CREDENTIALS ########################
# root of the project MailAssistant
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG = json.load(open('creds/django_creds.json', 'r'))
SECRET_KEY = CONFIG['secret_key']
DJ_REST_AUTH_JWT_SECRET_KEY = CONFIG['secret_key']



######################## GENERAL CONFIGURATION ########################
ROOT_URLCONF = 'MailAssistant_project.urls'
ASGI_APPLICATION = 'MailAssistant_project.asgi.application'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
#----------------------- DATABASE CONFIGURATION -----------------------#
# For site in DB
SITE_ID = 3 
DATABASES = CONFIG['database_conf']

INSTALLED_APPS = [
    'django_extensions', # mandatory to get a https certificate
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'MailAssistant',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'WARNING'),
        },
    },
}



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# TODO: find where we need it and delete it as the folder does not exist anymore
STATIC_URL = 'static/'



######################## SECURITY ########################
CORS_ALLOW_ALL_ORIGINS = True
DEBUG = True
ALLOWED_HOSTS = ['*']

SIMPLE_JWT = {
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1), # Token expires in 1 day
    'ROTATE_REFRESH_TOKENS': False, # Whether to rotate refresh tokens upon each request
    'ALGORITHM': 'HS256',
    'VERIFYING_KEY': None,
    'VALIDATED_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
}
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]