"""
ASGI config for Aomail project.

This module configures ASGI for the Aomail application to handle both
synchronous HTTP and asynchronous WebSocket connections.

Documentation:
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

# Setting the default Django settings module for the 'asgi' application.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MailAssistant_project.settings")
django.setup()


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "https": get_asgi_application(),
    }
)
