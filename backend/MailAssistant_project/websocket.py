"""
Handles websocket connections between django backend server and client.
"""

from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ClientWebsocket(AsyncWebsocketConsumer):

    async def connect(self):
        print("New WebSocket connection initiated")
        await self.accept()
        print("======WebSocket connection established======")  # Server-side print

        # Send a message to the client to log in the JavaScript console
        await self.send(
            text_data=json.dumps(
                {
                    "type": "console.log",
                    "message": "WebSocket connection established on client side",
                }
            )
        )

    async def disconnect(self, close_code):
        print(f"WebSocket disconnected: {close_code}")

    async def send_email_notification(self, json_data):
        # Send the email data to the client
        await self.send(text_data=json.dumps({"type": "email_data", "data": json_data}))
