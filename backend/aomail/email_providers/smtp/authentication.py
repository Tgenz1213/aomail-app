"""
This file contains the authentication logic for the SMTP protocol.
"""

import logging
from smtplib import SMTP, SMTP_SSL


LOGGER = logging.getLogger(__name__)


def validate_smtp_connection(
    email_address: str,
    app_password: str,
    smtp_host: str,
    smtp_port: int,
    smtp_encryption: str,
) -> bool:
    smtp = connect_to_smtp(
        email_address, app_password, smtp_host, smtp_port, smtp_encryption
    )
    if smtp:
        smtp.quit()
        return True
    return False


def connect_to_smtp(
    email_address: str,
    app_password: str,
    smtp_host: str,
    smtp_port: int,
    smtp_encryption: str,
) -> SMTP | SMTP_SSL | None:
    try:
        LOGGER.info(
            f"Validating SMTP (Encryption: {smtp_encryption}) connection for {email_address} on {smtp_host}:{smtp_port}"
        )

        smtp_class = SMTP_SSL if smtp_encryption == "ssl" else SMTP
        smtp = smtp_class(smtp_host, smtp_port)
        if smtp_encryption == "tls":
            LOGGER.info(f"Starting TLS connection")
            smtp.ehlo()
            smtp.starttls()

        LOGGER.info(
            f"Logging in to SMTP server for {email_address} on {smtp_host}:{smtp_port}"
        )
        smtp.login(email_address, app_password)
        LOGGER.info(
            f"Logged in to SMTP server for {email_address} on {smtp_host}:{smtp_port}"
        )
        return smtp

    except Exception as e:
        LOGGER.error(
            f"Error validating SMTP connection for {email_address} on {smtp_host}:{smtp_port}: {e}"
        )
        return None
