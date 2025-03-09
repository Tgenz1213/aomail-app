"""
This file contains the authentication logic for the IMAP protocol.
"""

import logging
from imap_tools import MailBox, MailBoxUnencrypted, BaseMailBox
from aomail.utils import security
from aomail.constants import SOCIAL_API_REFRESH_TOKEN_KEY


LOGGER = logging.getLogger(__name__)


def validate_imap_connection(
    email_address: str,
    app_password: str,
    imap_host: str,
    imap_port: int,
    imap_encryption: str,
) -> bool:
    mailbox = connect_to_imap(
        email_address, app_password, imap_host, imap_port, imap_encryption
    )
    if mailbox:
        mailbox.logout()
        return True
    return False


def connect_to_imap(
    email_address: str,
    app_password_encrypted: str,
    imap_host: str,
    imap_port: int,
    imap_encryption: str,
) -> BaseMailBox | None:
    try:
        app_password = security.decrypt_text(
            SOCIAL_API_REFRESH_TOKEN_KEY, app_password_encrypted
        )
        use_tls = imap_encryption == "tls"
        LOGGER.info(
            f"Validating IMAP (Encryption: {imap_encryption}) connection for {email_address} on {imap_host}:{imap_port}"
        )

        mailbox_class = MailBox if use_tls else MailBoxUnencrypted
        mailbox = mailbox_class(imap_host, imap_port)

        LOGGER.info(
            f"Logging in to IMAP server for {email_address} on {imap_host}:{imap_port}"
        )
        mailbox.login(email_address, app_password)
        LOGGER.info(
            f"Logged in to IMAP server for {email_address} on {imap_host}:{imap_port}"
        )
        return mailbox

    except Exception as e:
        LOGGER.error(
            f"Error validating IMAP connection for {email_address} on {imap_host}:{imap_port}: {e}"
        )
        return None
