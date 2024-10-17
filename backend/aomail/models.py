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
    subscription_id = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_trial = models.BooleanField(default=True)


class Statistics(models.Model):
    """Model for storing statistical data about emails received."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Email categories
    nb_emails_received = models.IntegerField(default=0)
    nb_emails_important = models.IntegerField(default=0)
    nb_emails_informative = models.IntegerField(default=0)
    nb_emails_useless = models.IntegerField(default=0)

    # Token usage
    nb_tokens_input = models.IntegerField(default=0)
    nb_tokens_output = models.IntegerField(default=0)

    # Answer
    nb_answer_required = models.IntegerField(default=0)
    nb_might_require_answer = models.IntegerField(default=0)
    nb_no_answer_required = models.IntegerField(default=0)

    # Relevance
    nb_highly_relevant = models.IntegerField(default=0)
    nb_possibly_relevant = models.IntegerField(default=0)
    nb_not_relevant = models.IntegerField(default=0)

    # Flags
    nb_spam = models.IntegerField(default=0)
    nb_scam = models.IntegerField(default=0)
    nb_newsletter = models.IntegerField(default=0)
    nb_notification = models.IntegerField(default=0)
    nb_meeting = models.IntegerField(default=0)


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
    username = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider_id = models.CharField(max_length=320, null=True)


class Category(models.Model):
    """Model for storing category information."""

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Preference(models.Model):
    """Model for storing user preferences."""

    timezone = models.CharField(max_length=50, default="UTC")
    theme = models.CharField(max_length=50, default="light")
    language = models.CharField(max_length=50, default="american")
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class SocialAPI(models.Model):
    """Table that contains email credentials."""

    type_api = models.CharField(max_length=50)
    email = models.CharField(max_length=524, unique=True)
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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_emails")
    social_api = models.ForeignKey(
        SocialAPI, on_delete=models.CASCADE, related_name="social_api_emails", null=True
    )
    provider_id = models.CharField(max_length=200, unique=True)
    email_provider = models.CharField(max_length=50)
    short_summary = models.CharField(max_length=1000)
    one_line_summary = models.CharField(max_length=200)
    html_content = models.TextField(default="")
    subject = models.CharField(max_length=400)
    priority = models.CharField(max_length=50)
    read = models.BooleanField(default=False)
    read_date = models.DateTimeField(null=True, default=None)
    archive = models.BooleanField(default=False)
    answer_later = models.BooleanField(default=False)
    sender = models.ForeignKey(
        Sender, on_delete=models.CASCADE, related_name="related_emails"
    )
    date = models.DateTimeField(null=True, blank=True)
    has_attachments = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    answer = models.CharField(max_length=50)
    relevance = models.CharField(max_length=50)
    spam = models.BooleanField(default=False)
    scam = models.BooleanField(default=False)
    newsletter = models.BooleanField(default=False)
    notification = models.BooleanField(default=False)
    meeting = models.BooleanField(default=False)


class Filter(models.Model):
    """Model for storing filter information"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    social_api = models.ForeignKey(SocialAPI, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    important = models.BooleanField(default=False)
    informative = models.BooleanField(default=False)
    useless = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    spam = models.BooleanField(default=False)
    scam = models.BooleanField(default=False)
    newsletter = models.BooleanField(default=False)
    notification = models.BooleanField(default=False)
    meeting = models.BooleanField(default=False)
    relevance = models.CharField(max_length=50, null=True)
    answer = models.CharField(max_length=50, null=True)


class Label(models.Model):
    """Model for storing shipping label information."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_labels")
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=300)
    platform = models.CharField(max_length=50)
    carrier = models.CharField(max_length=50)
    label_name = models.CharField(max_length=250)
    postage_deadline = models.DateTimeField()


class Attachment(models.Model):
    """Model for storing email attachment information."""

    email = models.ForeignKey(
        Email, on_delete=models.CASCADE, related_name="attachments"
    )
    name = models.CharField(max_length=200)
    id_api = models.CharField(max_length=500)


class CC_sender(models.Model):
    """Model for storing CC sender information."""

    email_object = models.ForeignKey(
        Email, on_delete=models.CASCADE, related_name="cc_senders"
    )
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=200)


class BCC_sender(models.Model):
    """Model for storing BCC sender information."""

    email_object = models.ForeignKey(
        Email, on_delete=models.CASCADE, related_name="bcc_senders"
    )
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=200)


class Picture(models.Model):
    """Model for storing pictures sender of a mail"""

    email = models.ForeignKey(
        Email, on_delete=models.CASCADE, related_name="picture_mail"
    )
    path = models.TextField()


class KeyPoint(models.Model):
    """Model for storing keypoints needed by Ao for knowledge search."""

    is_reply = models.BooleanField()
    position = models.IntegerField(null=True, default=None)
    category = models.TextField(max_length=50)
    organization = models.TextField(max_length=50)
    topic = models.TextField(max_length=50)
    content = models.TextField(max_length=50)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
