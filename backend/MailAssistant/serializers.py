from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message, Category, Email, BulletPoint, Rule, Preference, Sender

# link between data and API
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['text'] #get 'text' column

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        # Exclude the password or any other sensitive fields!

# Get categories name (GET)
class CategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)  # We only want the name field

# Get data from email (GET)
class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ('email_short_summary', 'content', 'subject', 'priority')

# Get all bullet points (GET)
class BulletPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulletPoint
        fields = '__all__'  # This will get all fields of BulletPoints

# Mark as read (POST)
class EmailReadUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ('read',)  # We only want the read field

# Mark as reply later (POST)
class EmailReplyLaterUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ('reply_later',)  # We only want the reply_later field

# Mark as blocked (POST)
class RuleBlockUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ('block',)  # We only want the block field

# Send mails (POST)
class EmailDataSerializer(serializers.Serializer):
    receiver_email = serializers.EmailField()
    cc = serializers.ListField(child=serializers.EmailField(), required=False)
    cci = serializers.ListField(child=serializers.EmailField(), required=False)
    subject = serializers.CharField(required=False)
    message = serializers.CharField()
    attachments = serializers.ListField(child=serializers.FileField(), required=False)

# GET background color
class PreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = ['bg_color']

# GET login from Users
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['login']

# Get Rules
class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ['info_AI', 'priority', 'block', 'category', 'user', 'sender']
        read_only_fields = ['user']

    def create(self, validated_data):
        # Extract the user from the context
        user = self.context.get('user')
        # Create the Rule instance with the user
        return Rule.objects.create(user=user, **validated_data)

class SenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sender
        fields = ['id', 'email', 'name']  # Include 'id' in the fields

class NewEmailAISerializer(serializers.Serializer):
    input_data = serializers.CharField()
    length = serializers.CharField()
    formality = serializers.CharField()

class EmailAIRecommendationsSerializer(serializers.Serializer):
    mail_content = serializers.CharField()
    user_recommendation = serializers.CharField()
    email_subject = serializers.CharField()

class EmailCorrectionSerializer(serializers.Serializer):
    email_subject = serializers.CharField(required=True, allow_blank=False)
    email_body = serializers.CharField(required=True, allow_blank=False)

    def validate(self, data):
        """
        Check that both email subject and body are provided.
        """
        if 'email_subject' not in data or not data['email_subject'].strip():
            raise serializers.ValidationError("Email subject is required.")
        if 'email_body' not in data or not data['email_body'].strip():
            raise serializers.ValidationError("Email body is required.")
        return data

class EmailCopyWritingSerializer(serializers.Serializer):
    email_subject = serializers.CharField(required=True, allow_blank=False)
    email_body = serializers.CharField(required=True, allow_blank=False)

    def validate(self, data):
        """
        Check that both email subject and body are provided.
        """
        if 'email_subject' not in data or not data['email_subject'].strip():
            raise serializers.ValidationError("Email subject is required.")
        if 'email_body' not in data or not data['email_body'].strip():
            raise serializers.ValidationError("Email body is required.")
        return data