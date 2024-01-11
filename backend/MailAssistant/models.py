from django.db import models
from django.contrib.auth.models import User

# class User(models.Model):
#     login = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)  # renamed from 'paswd' for clarity

class Message(models.Model):
    text = models.CharField(max_length=200)

class Sender(models.Model):
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Preference(models.Model):
    theme = models.CharField(max_length=50)
    bg_color = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class SocialAPI(models.Model):
    type_api = models.CharField(max_length=50)
    access_token = models.CharField(max_length=500, null=True)
    refresh_token = models.CharField(max_length=500, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class CredsAPI(models.Model):
    social_api = models.ForeignKey(SocialAPI, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)

class Rule(models.Model):
    info_AI = models.TextField(blank=True)
    priority = models.CharField(max_length=50, blank=True)
    block = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.ForeignKey(Sender, on_delete=models.CASCADE)

class Email(models.Model):
    provider_id = models.CharField(max_length=200, unique=True)
    email_provider = models.CharField(max_length=50)
    email_short_summary = models.CharField(max_length=200)
    content = models.TextField()
    subject = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    read = models.BooleanField()
    answer_later = models.BooleanField()
    sender = models.ForeignKey(Sender, on_delete=models.CASCADE, related_name='related_emails')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_emails')

class BulletPoint(models.Model):
    content = models.TextField()
    email = models.ForeignKey(Email, on_delete=models.CASCADE)  # renamed from 'id_email'

class CC(models.Model):
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    email_reference = models.ForeignKey(Email, on_delete=models.CASCADE)  # 'id_email' is renamed