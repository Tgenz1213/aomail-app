"""
Handles all functions linked with logging and encryption
"""

import logging
import base64
from django.http import HttpRequest
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


# ----------------------- LOGGING -----------------------#
def get_ip_with_port(request: HttpRequest):
    """Returns the ip with the connection port"""
    try:
        source_port = request.META.get("SERVER_PORT", None)
        x_forwarded_for: str = request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        ip_with_port = f"{ip}:{source_port}"
        return ip_with_port

    except Exception as e:
        LOGGER.error(f"An error occurred while generating IP with port: {str(e)}")


# ----------------------- CRYPTOGRAPHY -----------------------#
def encrypt_unsalted(encryption_key: str, plaintext: str) -> str:
    """Encrypts input plaintext"""
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
    """Decrypts input encrypted ciphertext"""
    aes_key = base64.b64decode(encryption_key.encode("utf-8"))
    ciphertext = base64.b64decode(ciphertext_base64.encode("utf-8"))
    cipher = Cipher(algorithms.AES(aes_key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()
    unpadded_text = decrypted_text.rstrip()
    return unpadded_text.decode("utf-8")


def encrypt_text(plaintext: str, encryption_key: str) -> str:
    """Encrypts input plaintext with salt"""
    fernet = Fernet(encryption_key)
    encrypted_text = fernet.encrypt(plaintext.encode())
    return encrypted_text.decode()


def decrypt_text(encrypted_text: str, encryption_key: str) -> str:
    """Decrypts input encrypted with salt"""
    fernet = Fernet(encryption_key)
    decrypted_text = fernet.decrypt(encrypted_text.encode())
    return decrypted_text.decode()
