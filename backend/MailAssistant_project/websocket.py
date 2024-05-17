"""
Handles websocket connections between django backend server and client.
"""

from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ClientWebsocket(AsyncWebsocketConsumer):
    async def connect(self):
        # Automatically accept all incoming connections
        await self.accept()

    async def disconnect(self, close_code):
        # No action needed on disconnect
        pass

    async def receive(self, text_data=None, bytes_data=None):
        # Handle incoming messages from the client if necessary
        pass

    async def send_email_notification(self):
        # Send a message to this WebSocket
        await self.send(
            text_data=json.dumps(
                {"message": "email.received"}
            )
        )
