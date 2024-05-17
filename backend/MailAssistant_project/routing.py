"""
WebSocket URL Configuration

This module handles WebSocket connections for the MailAssistant project.
It maps WebSocket endpoints to their respective ASGI consumers.
"""

from django.urls import re_path
from backend.MailAssistant_project.websocket import ClientWebsocket

websocket_urlpatterns = [
    re_path(r"ws/aomail/$", ClientWebsocket.as_asgi()),
]
