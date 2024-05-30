"""
Database Models with Security Measures.

Each model corresponds to a database table, storing data and implementing security measures against SQL injection attacks.
"""

from django.db import models
from django.contrib.auth.models import User


class Subscription(models.Model):
    # UNDER DEVELOPMENT
    """Model for storing subscription information."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=50)
    stripe_subscription_id = models.CharField(
        max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)
    billing_interval = models.CharField(max_length=10, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="EUR")


class Message(models.Model):
    """Model for storing text messages."""

    text = models.CharField(max_length=200)


class Sender(models.Model):
    """Model for storing sender information."""

    email = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)


class Contact(models.Model):
    """Stores contacts of an email account"""

    email = models.CharField(max_length=320, null=True)
    username = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider_id = models.CharField(max_length=320, null=True)


class Category(models.Model):
    """Model for storing category information."""

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=300)  # PLEASE DO NOT CHANGE
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Preference(models.Model):
    """Model for storing user preferences."""

    theme = models.CharField(max_length=50, default="light")
    language = models.CharField(max_length=50, default="en")
    bg_color = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class SocialAPI(models.Model):
    """Table that contains email credentials."""

    type_api = models.CharField(max_length=50)
    email = models.CharField(max_length=320, unique=True)
    access_token = models.CharField(max_length=3000)
    refresh_token = models.CharField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_description = models.CharField(max_length=200, default="")


class Rule(models.Model):
    """Model for storing rule information."""

    info_AI = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=50, blank=True, null=True)
    block = models.BooleanField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.OneToOneField(Sender, on_delete=models.CASCADE)


class MicrosoftListener(models.Model):
    """Stores information about Microsoft subscriptions"""

    subscription_id = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=320)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class GoogleListener(models.Model):
    """Stores information about Google subscriptions"""

    last_modified = models.DateTimeField(null=True)
    social_api = models.ForeignKey(
        SocialAPI,
        on_delete=models.CASCADE,
        related_name="social_api_google_listener",
        null=True,
    )


class Email(models.Model):
    """Model for storing email information."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_emails")
    social_api = models.ForeignKey(
        SocialAPI, on_delete=models.CASCADE, related_name="social_api_emails", null=True
    )
    provider_id = models.CharField(max_length=200, unique=True)
    web_link = models.CharField(max_length=200, null=True)
    email_provider = models.CharField(max_length=50)
    email_short_summary = models.CharField(max_length=500)
    content = models.TextField()
    html_content = models.TextField(default="")  # quick fix
    subject = models.CharField(max_length=400)
    priority = models.CharField(max_length=50)
    read = models.BooleanField()
    read_date = models.DateTimeField(null=True)
    answer_later = models.BooleanField()
    sender = models.ForeignKey(
        Sender, on_delete=models.CASCADE, related_name="related_emails"
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    has_attachments = models.BooleanField(default=False)
    answer = models.CharField(max_length=50, default="")
    relevance = models.CharField(max_length=50, default="")


class CC_sender(models.Model):
    """Model for storing CC sender information."""

    mail_id = models.ForeignKey(
        Email, on_delete=models.CASCADE, related_name="cc_senders"
    )
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=200)


class BCC_sender(models.Model):
    """Model for storing BCC sender information."""

    mail_id = models.ForeignKey(
        Email, on_delete=models.CASCADE, related_name="bcc_senders"
    )
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=200)


class Picture(models.Model):
    """Model for storing pictures sender of a mail"""

    mail_id = models.ForeignKey(
        Email, on_delete=models.CASCADE, related_name="picture_mail"
    )
    picture = models.TextField()


class BulletPoint(models.Model):
    """Model for storing bullet points."""

    content = models.TextField()
    email = models.ForeignKey(Email, on_delete=models.CASCADE)


class KeyPoint(models.Model):
    """Model for storing keypoints needed by Ao for knowledge search."""

    is_reply = models.BooleanField()
    position = models.IntegerField(null=True, default=None)
    category = models.TextField(max_length=50)
    organization = models.TextField(max_length=50)
    topic = models.TextField(max_length=50)
    content = models.TextField(max_length=50)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
