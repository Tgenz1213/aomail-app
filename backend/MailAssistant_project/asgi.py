"""
ASGI (Asynchronous Server Gateway Interface) config for MailAssistant_project project.
Django's default ASGI handler will run all your code in a synchronous thread

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import os
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MailAssistant_project.settings')

application = get_asgi_application()