"""
Utils module for IMAP operations
"""


def get_imap_email_id(message_id: str) -> str:
    """
    Extracts the email ID from a message ID string.

    Args:
        message_id (str): The message ID string.

    Returns:
        str: The email ID.
    """
    return message_id[0].split("<")[1].split(">")[0]
