"""
ASGI config for Aomail project.

This module configures ASGI for the Aomail application to handle both
synchronous HTTP and asynchronous WebSocket connections.

Documentation:
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()
