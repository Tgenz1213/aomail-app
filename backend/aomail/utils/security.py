"""
Handles all functions linked with logging and encryption.
"""

import logging
import base64
from functools import wraps
from django.http import HttpRequest
from datetime import timedelta
from django.utils import timezone
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from aomail.models import Subscription
from rest_framework.response import Response
from rest_framework import status
from aomail.constants import EMAIL_ADMIN, INACTIVE


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
def block_user(view_func):
    @wraps(view_func)
    def _wrapped_view(request: HttpRequest, *args, **kwargs):
        """
        Decorator to restrict access to users with a blocked subscription.

        Returns:
            Function: The wrapped view function if the user is not blocked.
                      Otherwise, returns a 403 response with an error message.
        """
        user = request.user
        subscription = Subscription.objects.get(user=user)
        if subscription.is_block:
            return Response(
                {
                    "error": f"You have been blocked. Send an email at: {EMAIL_ADMIN} to get more informations"
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def subscription(allowed_plans: list):
    """
    Decorator to ensure that the requesting user has an active subscription and the required plan.

    Args:
        allowed_plans (list): A list of subscription plans allowed to access the view.

    Returns:
        Function: The wrapped view function if subscription is valid. Otherwise, redirects to "not-authorized".
    """

    def decorator(view_func):
        @wraps(view_func)
        @permission_classes([IsAuthenticated])
        def _wrapped_view(request: HttpRequest, *args, **kwargs):
            user = request.user
            subscription = Subscription.objects.get(user=user)

            if not INACTIVE in allowed_plans:
                if subscription.is_trial:
                    trial_period = timedelta(days=30)
                    if timezone.now() - subscription.created_at > trial_period:
                        LOGGER.info(f"Free trial expired for user ID: {user.id}")
                        return Response(
                            {"error": "Free trial expired"},
                            status=status.HTTP_403_FORBIDDEN,
                        )

                if subscription.plan not in allowed_plans:
                    LOGGER.info(
                        f"User with ID: {user.id} does not have the required plan"
                    )
                    return Response(
                        {"error": "Plan not allowed.", "allowedPlans": allowed_plans},
                        status=status.HTTP_403_FORBIDDEN,
                    )

                if not subscription.is_active:
                    LOGGER.info(
                        f"User with ID: {user.id} does not have an active subscription"
                    )
                    return Response(
                        {"error": "Subscription is inactive", "isActive": False},
                        status=status.HTTP_403_FORBIDDEN,
                    )

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def admin_access_required(view_func):
    """
    Decorator to ensure that the requesting user is an authenticated admin (superuser).

    Args:
        view_func: The view function to be wrapped.

    Returns:
        The wrapped view function.
    """

    @wraps(view_func)
    def _wrapped_view(request: HttpRequest, *args, **kwargs):
        try:
            user = request.user

            if not user.is_authenticated:
                return Response(
                    {"error": "Unauthorized: User is not authenticated."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            if not user.is_superuser:
                return Response(
                    {"error": "Forbidden: Admin access required."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            return view_func(request, *args, **kwargs)

        except Exception as e:
            LOGGER.error(
                f"Error occurred when trying to access admin resource: {str(e)}"
            )
            return Response(
                {"error": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return _wrapped_view


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
