from django.db import models

# Create your models here.
# TO TEST THE API
class Message(models.Model):
    text = models.CharField(max_length=200)