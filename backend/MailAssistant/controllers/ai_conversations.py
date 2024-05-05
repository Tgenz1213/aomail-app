"""
Provides views for generating new email responses based on user input and chat history.
"""

import logging
from django.http import HttpRequest
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from MailAssistant.ai_providers.ai_memory import EmailReplyConversation
from django.core.mail import send_mail
from langchain.memory import ChatMessageHistory
from langchain.schema import AIMessage, HumanMessage
from django.template.loader import render_to_string
from MailAssistant.constants import (
    ADMIN_EMAIL_LIST,
    EMAIL_NO_REPLY,
    MAX_RETRIES,
)


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


# TODO: think where we should put this function for cleaner code
def dict_to_chat_history(data: dict) -> ChatMessageHistory:
    """
    Convert a dictionary representation of chat history to a ChatMessageHistory object.

    Args:
        data (dict): A dictionary containing chat history data

    Returns:
    ChatMessageHistory: A ChatMessageHistory object representing the chat history.
    """
    messages = []
    if not data.get("messages", []):
        chat_history = ChatMessageHistory()
        chat_history.add_ai_message("Does this answer satisfy you?")
        return chat_history
    for message_data in data["messages"]:
        speaker = message_data["type"]
        content = message_data["content"]
        if speaker == "ai":
            message = AIMessage(content=content)
        else:
            message = HumanMessage(content=content)
        messages.append(message)
    return ChatMessageHistory(messages=messages)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def get_new_email_response(request: HttpRequest) -> Response:
    """
    Generate a new email response based on user input, email importance, subject, body, and chat history.

    Parameters:
        request (HttpRequest): The HTTP request object containing the following parameters in the POST data:
            - userInput (str): User input to enhance the email body response.
            - importance (str): Importance level of the email.
            - subject (str): Subject of the email response.
            - body (str): Current body of the previously generated response.
            - history (dict): Dictionary representing the chat history.

    Returns:
        Response: A response object containing the new email body response or an error message.
    """
    user = request.user
    user_input: str = request.data["userInput"]
    importance: str = request.data["importance"]
    subject: str = request.data["subject"]
    body: str = request.data["body"]
    history: dict = request.data["history"]

    chat_history = dict_to_chat_history(history)
    email_reply_conv = EmailReplyConversation(
        user, importance, subject, body, chat_history
    )

    for i in range(MAX_RETRIES):
        try:
            new_body_response = email_reply_conv.improve_email_response(user_input)
            print("WE HAVE GENERATED A RESPONSE AI CONVERSAIONT SUCCESFULLY")
            print(email_reply_conv.history.dict())
            return Response(
                {"email_body": new_body_response, "history": email_reply_conv.history.dict()},
                status=200,
            )
        except Exception as e:
            LOGGER.critical(
                f"[Attempt n°{i+1}] failed to generate a new body response: {str(e)}"
            )
            context = {"attempt_number": i, "error": str(e), "user": user}
            email_html = render_to_string("ai_failed_gen_body_resp.html", context)
            send_mail(
                subject="Critical Alert: Failed to generate a new body response",
                message="",
                recipient_list=ADMIN_EMAIL_LIST,
                from_email=EMAIL_NO_REPLY,
                html_message=email_html,
                fail_silently=False,
            )

    return Response(
        {
            "error": "The generation of a new email response body failed 3 times in a row. Our team is on his way to fix it."
        },
        status=500,
    )
