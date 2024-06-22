"""
Handles all functions linked with logging and encryption
"""

import logging
from functools import wraps
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from django.http import HttpRequest
from django.shortcuts import redirect
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from MailAssistant.constants import BASE_URL
from MailAssistant.models import Subscription


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


# ----------------------- LOGGING -----------------------#
def get_ip_with_port(request: HttpRequest) -> str | None:
    """
    Returns the IP address with the connection port from the given HTTP request.

    Args:
        request (HttpRequest): The HTTP request object containing metadata.

    Returns:
        str | None: The IP address with the connection port in the format 'IP:PORT',
                    or None if an error occurs.
    """
    try:
        source_port = request.META.get("SERVER_PORT", None)
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        ip_with_port = f"{ip}:{source_port}"
        return ip_with_port

    except Exception as e:
        LOGGER.error(f"An error occurred while retrieving IP with port: {str(e)}")
        return None


# ----------------------- DECORATOR -----------------------#
# THIS IS USED TO CHECK IF THE USER SUBSCRIPTION IS STILL VALID
def subscription(allowed_plans):
    def decorator(view_func):
        @wraps(view_func)
        @permission_classes([IsAuthenticated])
        def _wrapped_view(request: HttpRequest, *args, **kwargs):
            user = request.user
            now = timezone.now()
            active_subscription = Subscription.objects.filter(
                user=user, end_date__gt=now, plan__in=allowed_plans
            ).exists()

            if not active_subscription:
                # TODO: Redirect to a subscription expired page with expiration date
                # explain on this page what the user can still acces (ONLY settings page)
                # explain that we will stop receiving its email in X days => according to google and microsoft (make a request to know)

                print("User does not have an active subscription.")

                #  (NOT 401 page) => TODO: change (it does not work anyway => TO debug)
                # return redirect(f"{BASE_URL}not-authorized")

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


# ----------------------- CRYPTOGRAPHY -----------------------#
def encrypt_unsalted(encryption_key: str, plaintext: str) -> str:
    """
    Encrypts the input plaintext using AES encryption without salt.

    Args:
        encryption_key (str): The base64-encoded encryption key.
        plaintext (str): The plaintext string to be encrypted.

    Returns:
        str: The base64-encoded ciphertext.
    """
    aes_key = base64.b64decode(encryption_key.encode("utf-8"))
    cipher = Cipher(algorithms.AES(aes_key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_plaintext = plaintext + " " * (16 - len(plaintext) % 16)
    ciphertext = (
        encryptor.update(padded_plaintext.encode("utf-8")) + encryptor.finalize()
    )
    ciphertext_base64 = base64.b64encode(ciphertext).decode("utf-8")
    return ciphertext_base64


def decrypt_unsalted(encryption_key: str, ciphertext_base64: str) -> str:
    """
    Decrypts the input encrypted ciphertext using AES decryption without salt.

    Args:
        encryption_key (str): The base64-encoded encryption key.
        ciphertext_base64 (str): The base64-encoded ciphertext to be decrypted.

    Returns:
        str: The decrypted plaintext string.
    """
    aes_key = base64.b64decode(encryption_key.encode("utf-8"))
    ciphertext = base64.b64decode(ciphertext_base64.encode("utf-8"))
    cipher = Cipher(algorithms.AES(aes_key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()
    unpadded_text = decrypted_text.rstrip()
    return unpadded_text.decode("utf-8")


def encrypt_text(encryption_key: str, plaintext: str) -> str:
    """
    Encrypts the input plaintext using Fernet encryption with salt.

    Args:
        encryption_key (str): The base64-encoded encryption key.
        plaintext (str): The plaintext string to be encrypted.

    Returns:
        str: The base64-encoded encrypted text.
    """
    fernet = Fernet(encryption_key)
    encrypted_text = fernet.encrypt(plaintext.encode())
    return encrypted_text.decode()


def decrypt_text(encryption_key: str, encrypted_text: str) -> str:
    """
    Decrypts the input encrypted text using Fernet decryption with salt.

    Args:
        encryption_key (str): The base64-encoded encryption key.
        encrypted_text (str): The base64-encoded encrypted text to be decrypted.

    Returns:
        str: The decrypted plaintext string.
    """
    fernet = Fernet(encryption_key)
    decrypted_text = fernet.decrypt(encrypted_text.encode())
    return decrypted_text.decode()
