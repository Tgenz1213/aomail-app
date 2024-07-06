"""
TODO:
- split email_to_db + separate call depending on the api
"""

import base64
import datetime
import logging
import re
import string
import threading
import time
import random
import json
import os
from rest_framework import status
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.models import User
from collections import defaultdict
from django.db import IntegrityError
from django.shortcuts import redirect
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.auth import exceptions as auth_exceptions
from google.auth.transport.requests import Request
from google.oauth2 import credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from httpx import HTTPError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from email.utils import parsedate_to_datetime
from MailAssistant.utils.serializers import EmailDataSerializer
from django.core.mail import send_mail
from django.template.loader import render_to_string
from MailAssistant.ai_providers import claude
from MailAssistant.utils.security import subscription
from MailAssistant.utils import security
from MailAssistant.constants import (
    FREE_PLAN,
    ADMIN_EMAIL_LIST,
    DEFAULT_CATEGORY,
    EMAIL_NO_REPLY,
    ENCRYPTION_KEYS,
    GOOGLE,
    GOOGLE_CONFIG,
    GOOGLE_CREDS,
    GOOGLE_PROJECT_ID,
    GOOGLE_PROVIDER,
    GOOGLE_TOPIC_NAME,
    MAX_RETRIES,
    MEDIA_URL,
    MICROSOFT,
    REDIRECT_URI_LINK_EMAIL,
    REDIRECT_URI_SIGNUP,
    GOOGLE_SCOPES,
    BASE_URL_MA,
)
from MailAssistant.utils.tree_knowledge import Search
from MailAssistant.email_providers.google.authentication import authenticate_service
from MailAssistant.utils import email_processing
from MailAssistant.models import (
    Contact,
    KeyPoint,
    Preference,
    Rule,
    SocialAPI,
    Category,
    Email,
    Sender,
    CC_sender,
    BCC_sender,
    Picture,
    Attachment,
)
from base64 import urlsafe_b64encode
from bs4 import BeautifulSoup
from googleapiclient.http import BatchHttpRequest
import base64
import datetime
import json
import logging
import threading
import time
import urllib.parse
import requests
from collections import defaultdict
from urllib.parse import urlencode
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import UploadedFile
from django.utils.timezone import make_aware
from msal import ConfidentialClientApplication
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import View
from rest_framework.response import Response
from MailAssistant.ai_providers import claude
from MailAssistant.utils.tree_knowledge import Search
from MailAssistant.utils import security
from MailAssistant.utils.security import subscription
from MailAssistant.utils.serializers import (
    EmailDataSerializer,
    EmailScheduleDataSerializer,
)

from MailAssistant.email_providers.google import authentication as auth_google
from MailAssistant.email_providers.microsoft import authentication as auth_microsoft
from MailAssistant.utils import email_processing
from MailAssistant.constants import (
    FREE_PLAN,
    ADMIN_EMAIL_LIST,
    BASE_URL,
    DEFAULT_CATEGORY,
    EMAIL_NO_REPLY,
    ENCRYPTION_KEYS,
    GRAPH_URL,
    MAX_RETRIES,
    MICROSOFT_AUTHORITY,
    MICROSOFT_CLIENT_STATE,
    MICROSOFT_CONFIG,
    MICROSOFT_PROVIDER,
    MICROSOFT_SCOPES,
    REDIRECT_URI_LINK_EMAIL,
    REDIRECT_URI_SIGNUP,
)
from MailAssistant.models import (
    Category,
    Contact,
    Email,
    KeyPoint,
    MicrosoftListener,
    Preference,
    Rule,
    Sender,
    SocialAPI,
)
from MailAssistant.email_providers.google import (
    email_operations as email_operations_google,
)
from MailAssistant.email_providers.microsoft import (
    email_operations as email_operations_microsoft,
)


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


def email_to_db(user: User, id_email: str, social_api: SocialAPI) -> bool | str:
    """
    Saves email notifications from Microsoft Graph API listener to the database.

    Args:
    TODO clean
        email_provider (str): GOOGLE or MICROSOFT 
        user (User): The user object for whom the email is being saved.
        email (str): The email address associated with the notification.
        id_email (str): The ID of the email notification from Microsoft Graph API.

    Returns:
        bool | str: True if the email was successfully saved, False if there was an issue saving the email,
                    or an error message if an exception occurred.
    """
    type_api = social_api.type_api

    
    LOGGER.info(
        f"Starting the process of saving email from Microsoft Graph API to database for user ID: {user.id} and email ID: {id_email}"
    )

    if type_api == MICROSOFT:
        access_token = auth_microsoft.refresh_access_token(social_api)

        (
            subject,
            from_name,
            decoded_data,
            email_id,
            sent_date,
            has_attachments,
            is_reply,
        ) = get_mail_to_db(access_token, None, id_email)

        if Email.objects.filter(provider_id=email_id).exists():
            return True

        sender = Sender.objects.filter(email=from_name[1]).first()

        if not decoded_data:
            LOGGER.info(
                f"No decoded data retrieved from Microsoft Graph API for user ID: {user.id} and email ID: {id_email}"
            )
            return False

        category_dict = email_processing.get_db_categories(user)
        category = Category.objects.get(name=DEFAULT_CATEGORY, user=user)
        rules = Rule.objects.filter(sender=sender)
        rule_category = None

        if rules.exists():
            for rule in rules:
                if rule.block:
                    return True

                if rule.category:
                    category = rule.category
                    rule_category = True

        user_description = (
            social_api.user_description if social_api.user_description is not None else ""
        )
        language = Preference.objects.get(user=user).language

        if is_reply:
            # Summarize conversation with Search
            email_content = email_processing.preprocess_email(decoded_data)
            user_id = user.id
            search = Search(user_id)
            conversation_summary = search.summarize_conversation(
                subject, email_content, user_description, language
            )
        else:
            # Summarize single email with Search
            email_content = email_processing.preprocess_email(decoded_data)
            user_id = user.id
            search = Search(user_id)
            email_summary = search.summarize_email(
                subject, email_content, user_description, language
            )

        email_processed = claude.categorize_and_summarize_email(
            subject, decoded_data, category_dict, user_description, from_name[1]
        )

        priority: str = email_processed["importance"]
        topic: str = email_processed["topic"]
        answer: str = email_processed["response"]
        relevance: str = email_processed["relevance"]
        flags: dict = email_processed["flags"]
        spam: bool = flags["spam"]
        scam: bool = flags["scam"]
        newsletter: bool = flags["newsletter"]
        notification: bool = flags["notification"]
        meeting: bool = flags["meeting"]
        summary: dict = email_processed["summary"]
        short_summary: str = summary["short"]
        one_line_summary: str = summary["one_line"]

        if not rule_category:
            if topic in category_dict:
                category = Category.objects.get(name=topic, user=user)

        if not sender:
            sender_name, sender_email = from_name[0], from_name[1]
            if not sender_name:
                sender_name = sender_email

            sender = Sender.objects.filter(email=sender_email).first()
            if not sender:
                sender = Sender.objects.create(email=sender_email, name=sender_name)

        try:
            email_entry = Email.objects.create(
                social_api=social_api,
                provider_id=email_id,
                email_provider=MICROSOFT_PROVIDER,
                short_summary=short_summary,
                one_line_summary=one_line_summary,
                subject=subject,
                priority=priority,
                sender=sender,
                category=category,
                user=user,
                date=sent_date,
                has_attachments=has_attachments,
                answer=answer,
                relevance=relevance,
                spam=spam,
                scam=scam,
                newsletter=newsletter,
                notification=notification,
                meeting=meeting,
            )

            if is_reply:
                conversation_summary_category = conversation_summary["category"]
                conversation_summary_organization = conversation_summary["organization"]
                conversation_summary_topic = conversation_summary["topic"]
                keypoints: dict = conversation_summary["keypoints"]

                for index, keypoints_list in keypoints.items():
                    for keypoint in keypoints_list:
                        KeyPoint.objects.create(
                            is_reply=True,
                            position=index,
                            category=conversation_summary_category,
                            organization=conversation_summary_organization,
                            topic=conversation_summary_topic,
                            content=keypoint,
                            email=email_entry,
                        )

            else:
                email_summary_category = email_summary["category"]
                email_summary_organization = email_summary["organization"]
                email_summary_topic = email_summary["topic"]

                for keypoint in email_summary["keypoints"]:
                    KeyPoint.objects.create(
                        is_reply=False,
                        category=email_summary_category,
                        organization=email_summary_organization,
                        topic=email_summary_topic,
                        content=keypoint,
                        email=email_entry,
                    )

            contact_name, contact_email = from_name[0], from_name[1]
            Contact.objects.get_or_create(
                user=user, email=contact_email, username=contact_name
            )

            LOGGER.info(
                f"Email ID: {id_email} saved to database successfully for user ID: {user.id} using Microsoft Graph API"
            )
            return True

        except Exception as e:
            LOGGER.error(
                f"An error occurred when trying to create an email with ID {email_id} for user ID: {user.id}: {str(e)}"
            )
            return str(e)



    elif email_provider == GOOGLE:
        LOGGER.info(
            f"Starting the process of saving email from Google API to database for user ID: {user.id}"
        )

        email_user = social_api.email
        services = auth_google.authenticate_service(user, email_user)

        (
            subject,
            from_name,
            decoded_data,
            safe_html,
            email_id,
            sent_date,
            has_attachments,
            is_reply,
            cc_info,
            bcc_info,
            image_files,
            attachments,
        ) = get_mail_to_db(services)

        if Email.objects.filter(provider_id=email_id).exists():
            return True

        user_description = (
            social_api.user_description if social_api.user_description else ""
        )
        language = Preference.objects.get(user=user).language

        if not decoded_data:
            LOGGER.info(
                f"No decoded data retrieved from Google API for user ID: {user.id} and email ID: {email_id}"
            )
            return "No decoded data"

        sender = Sender.objects.filter(email=from_name[1]).first()
        category_dict = email_processing.get_db_categories(user)
        category = Category.objects.get(name=DEFAULT_CATEGORY, user=user)
        rules = Rule.objects.filter(sender=sender)
        rule_category = None

        if rules.exists():
            for rule in rules:
                if rule.block:
                    return True

                if rule.category:
                    category = rule.category
                    rule_category = True

        email_content = email_processing.preprocess_email(decoded_data)
        search = Search(user.id)

        if is_reply:
            conversation_summary = search.summarize_conversation(
                subject, email_content, user_description, language
            )
        else:
            email_summary = search.summarize_email(
                subject, email_content, user_description, language
            )

        email_processed = claude.categorize_and_summarize_email(
            subject, decoded_data, category_dict, user_description, from_name[1]
        )

        priority: str = email_processed["importance"]
        topic: str = email_processed["topic"]
        answer: str = email_processed["response"]
        relevance: str = email_processed["relevance"]
        flags: dict = email_processed["flags"]
        spam: bool = flags["spam"]
        scam: bool = flags["scam"]
        newsletter: bool = flags["newsletter"]
        notification: bool = flags["notification"]
        meeting: bool = flags["meeting"]
        summary: dict = email_processed["summary"]
        short_summary: str = summary["short"]
        one_line_summary: str = summary["one_line"]

        if not rule_category:
            category = Category.objects.get(name=topic, user=user)

        if not sender:
            sender_name, sender_email = from_name[0], from_name[1]
            if not sender_name:
                sender_name = sender_email

            sender = Sender.objects.filter(email=sender_email).first()
            if not sender:
                sender = Sender.objects.create(email=sender_email, name=sender_name)

        try:
            email_entry = Email.objects.create(
                social_api=social_api,
                provider_id=email_id,
                email_provider=GOOGLE_PROVIDER,
                short_summary=short_summary,
                one_line_summary=one_line_summary,
                html_content=safe_html,
                subject=subject,
                priority=priority,
                sender=sender,
                category=category,
                user=user,
                date=sent_date,
                has_attachments=has_attachments,
                answer=answer,
                relevance=relevance,
                spam=spam,
                scam=scam,
                newsletter=newsletter,
                notification=notification,
                meeting=meeting,
            )

            if is_reply:
                conversation_summary_category = conversation_summary["category"]
                conversation_summary_organization = conversation_summary["organization"]
                conversation_summary_topic = conversation_summary["topic"]
                keypoints: dict = conversation_summary["keypoints"]

                for index, keypoints_list in keypoints.items():
                    for keypoint in keypoints_list:
                        KeyPoint.objects.create(
                            is_reply=True,
                            position=index,
                            category=conversation_summary_category,
                            organization=conversation_summary_organization,
                            topic=conversation_summary_topic,
                            content=keypoint,
                            email=email_entry,
                        )
            else:
                email_summary_category = email_summary["category"]
                email_summary_organization = email_summary["organization"]
                email_summary_topic = email_summary["topic"]

                for keypoint in email_summary["keypoints"]:
                    KeyPoint.objects.create(
                        is_reply=False,
                        category=email_summary_category,
                        organization=email_summary_organization,
                        topic=email_summary_topic,
                        content=keypoint,
                        email=email_entry,
                    )

            contact_name, contact_email = from_name[0], from_name[1]
            Contact.objects.get_or_create(
                user=user, email=contact_email, username=contact_name
            )

            if cc_info:
                for email, name in cc_info:
                    CC_sender.objects.create(mail_id=email_entry, email=email, name=name)

            if bcc_info:
                for email, name in bcc_info:
                    BCC_sender.objects.create(mail_id=email_entry, email=email, name=name)

            if image_files:
                for image_path in image_files:
                    Picture.objects.create(mail_id=email_entry, picture=image_path)

            if attachments:
                for attachment in attachments:
                    Attachment.objects.create(
                        mail_id=email_entry,
                        name=attachment["attachmentName"],
                        id_api=attachment["attachmentId"],
                    )

            LOGGER.info(
                f"Email ID: {email_id} saved to database successfully for user ID: {user.id} using Google API"
            )
            return True

        except Exception as e:
            LOGGER.error(
                f"An error occurred when trying to create an email with ID {email_id} for user ID: {user.id}: {str(e)}"
            )
            return str(e)

    


def email_to_db(user: User, services, social_api: SocialAPI) -> bool | str:
    """
    Saves email notifications from Google listener to the database.

    Args:
        user (User): The user object for whom the email is being saved.
        services: The authenticated Google API services.
        social_api (SocialAPI): The SocialAPI instance associated with the user.

    Returns:
        bool | str: True if the email was successfully saved, False if there was an issue saving the email,
                    or an error message if an exception occurred.
    """
    ...
