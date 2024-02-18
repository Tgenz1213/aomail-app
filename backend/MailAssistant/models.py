"""
Database Models with Security Measures.

Each model corresponds to a database table, storing data and implementing security measures against SQL injection attacks.
"""
from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    """Model for storing text messages."""
    text = models.CharField(max_length=200)


class Sender(models.Model):
    """Model for storing sender information."""
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # null=True for debugging


class Language(models.Model):
    language = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Contact(models.Model):
    """Stores contacts of an email account"""
    email = models.CharField(max_length=320, null=True)
    username = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Category(models.Model):
    """Model for storing category information."""
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Preference(models.Model):
    """Model for storing user preferences."""
    theme = models.CharField(max_length=50)
    bg_color = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class SocialAPI(models.Model):
    """Table that contains email credentials."""
    type_api = models.CharField(max_length=50)
    email = models.CharField(max_length=320, null=True)
    access_token = models.CharField(max_length=3000, null=True)
    refresh_token = models.CharField(max_length=2000, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Rule(models.Model):
    """Model for storing rule information."""
    info_AI = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=50, blank=True, null=True)
    block = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.ForeignKey(Sender, on_delete=models.CASCADE)


class Email(models.Model):
    """Model for storing email information."""
    provider_id = models.CharField(max_length=200, unique=True)
    email_provider = models.CharField(max_length=50)
    email_short_summary = models.CharField(max_length=500)
    content = models.TextField()
    subject = models.CharField(max_length=100)
    priority = models.CharField(max_length=50)
    read = models.BooleanField()
    answer_later = models.BooleanField()
    sender = models.ForeignKey(Sender, on_delete=models.CASCADE, related_name='related_emails')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_emails')


class BulletPoint(models.Model):
    """Model for storing bullet points."""
    content = models.TextField()
    email = models.ForeignKey(Email, on_delete=models.CASCADE)  # renamed from 'id_email'


class CC(models.Model):
    """Model for storing CC (Carbon Copy) information."""
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    email_reference = models.ForeignKey(Email, on_delete=models.CASCADE)  # 'id_email' is renamed