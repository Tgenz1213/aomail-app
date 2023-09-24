from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# TO TEST THE API
# BDD class - table // parameter = column
# POSTGRESQL MAKEMIGRATION
class Message(models.Model):
    text = models.CharField(max_length=200)





class Senders(models.Model):
    id_sender = models.AutoField(primary_key=True)
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

##### COMMENTED FOR SECURITY REASON => Better to use the default User class from Django which secure by default 
'''
class Users(models.Model):
    id_user = models.AutoField(primary_key=True)
    login = models.CharField(max_length=50)
    paswd = models.CharField(max_length=50)'''
#####

class Categories(models.Model):
    id_category = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Preferences(models.Model):
    id_preferences = models.AutoField(primary_key=True)
    theme = models.CharField(max_length=50)
    bg_color = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Rules(models.Model):
    id_rule = models.AutoField(primary_key=True)
    info_AI = models.TextField()
    priority = models.CharField(max_length=50)
    block = models.BooleanField()
    # ForeignKeys
    id_category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    id_sender = models.ForeignKey(Senders, on_delete=models.CASCADE)

class Email(models.Model):
    id_email = models.AutoField(primary_key=True)
    email_short_summary = models.CharField(max_length=200)
    content = models.TextField()
    subject = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    read = models.BooleanField()
    answer_later = models.BooleanField()
    # ForeignKey relation to the Email model
    # id_sender = models.ForeignKey(Senders, on_delete=models.CASCADE)
    id_sender = models.ForeignKey(Senders, on_delete=models.CASCADE, related_name='related_emails')
    id_category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='related_user_emails', null=True) # TO CHECK true

class BulletPoints(models.Model):
    id_bullet_point = models.AutoField(primary_key=True)
    content = models.TextField()
    # ForeignKey relation to the Email model
    id_email = models.ForeignKey(Email, on_delete=models.CASCADE)

class CC(models.Model):
    id_cc = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    # ForeignKey relation to the Email model
    id_email = models.ForeignKey(Email, on_delete=models.CASCADE)