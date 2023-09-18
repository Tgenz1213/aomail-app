from rest_framework import serializers
from .models import Message

# link between data and API
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['text'] #get 'text' column
