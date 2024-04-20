"""
Database Models with Security Measures.

Each model corresponds to a database table, storing data and implementing security measures against SQL injection attacks.
"""

from django.db import models
from django.contrib.auth.models import User


class Subscription(models.Model):
    """Model for storing subscription information."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=50)
    stripe_subscription_id = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)
    billing_interval = models.CharField(max_length=10, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="EUR")


class BillingInfo(models.Model):
    """Model for storing billing information."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    billing_address = models.CharField(max_length=500)
    billing_email = models.CharField(max_length=500)
    name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=100)


class Message(models.Model):
    """Model for storing text messages."""

    text = models.CharField(max_length=200)


class Sender(models.Model):
    """Model for storing sender information."""

    email = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)


class Language(models.Model):
    """Stores language of users"""

    language = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class MicrosoftListener(models.Model):
    """Stores information about Microsoft subscriptions"""

    subscription_id = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=320)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


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

    theme = models.CharField(max_length=50)
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


class Email(models.Model):
    """Model for storing email information."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_emails")
    social_api = models.ForeignKey(
        SocialAPI, on_delete=models.CASCADE, related_name="social_api_emails", null=True
    )
    provider_id = models.CharField(max_length=200, unique=True)
    web_link = models.CharField(max_length=200, null=True)
    email_provider = models.CharField(max_length=50)
    email_short_summary = models.CharField(max_length=500)
    content = models.TextField()
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


class BulletPoint(models.Model):
    """Model for storing bullet points."""

    content = models.TextField()
    email = models.ForeignKey(Email, on_delete=models.CASCADE)


'''class CC(models.Model):
    """Model for storing CC (Carbon Copy) information."""

    email = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    email_reference = models.ForeignKey(Email, on_delete=models.CASCADE)'''
