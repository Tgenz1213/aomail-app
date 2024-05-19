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
from django.urls import re_path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from .websocket import ClientWebsocket

# Setting the default Django settings module for the 'asgi' application.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MailAssistant_project.settings")
django.setup()

# Define ASGI application protocol type routes handling HTTP and WebSocket requests.
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "https": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    re_path(r"ws/aomail/$", ClientWebsocket.as_asgi()),
                ]
            )
        ),
    }
)
