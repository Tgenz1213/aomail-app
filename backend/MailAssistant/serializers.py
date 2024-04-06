"""
Handles serialization for various models in API interactions.

A serializer is an object that requires specific parameters and is used to check if the input data is valid (preprocessing).
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Message,
    Category,
    Email,
    BulletPoint,
    Rule,
    Preference,
    Sender,
    Contact,
)


# ----------------------- EMAIL SERIALIZER -----------------------#
class EmailDataSerializer(serializers.Serializer):
    """Serializer for sending emails (POST request)."""

    to = serializers.ListField(required=True)
    subject = serializers.CharField(required=True)
    message = serializers.CharField(required=False, allow_blank=True)
    cc = serializers.ListField(required=False)
    cci = serializers.ListField(required=False)
    attachments = serializers.ListField(child=serializers.FileField(), required=False)


class EmailReadUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating the 'read' status of an email through a POST request."""

    class Meta:
        model = Email
        fields = ("read",)  # Update the 'read' field only


class EmailReplyLaterUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating the 'reply later' status of an email through a POST request."""

    class Meta:
        model = Email
        fields = ("answer_later",)  # Update the 'reply later' field only


class EmailCorrectionSerializer(serializers.Serializer):
    """Serializer for handling email correction data."""

    email_subject = serializers.CharField(required=True, allow_blank=False)
    email_body = serializers.CharField(required=True, allow_blank=False)

    def validate(self, data):
        """Validate method to check that both email subject and body are provided."""
        if "email_subject" not in data or not data["email_subject"].strip():
            raise serializers.ValidationError("Email subject is required.")
        if "email_body" not in data or not data["email_body"].strip():
            raise serializers.ValidationError("Email body is required.")
        return data


class EmailCopyWritingSerializer(serializers.Serializer):
    """Serializer for handling email copywriting data."""

    email_subject = serializers.CharField(required=True, allow_blank=False)
    email_body = serializers.CharField(required=True, allow_blank=False)

    def validate(self, data):
        """Validate method to check that both email subject and body are provided."""
        if "email_subject" not in data or not data["email_subject"].strip():
            raise serializers.ValidationError("Email subject is required.")
        if "email_body" not in data or not data["email_body"].strip():
            raise serializers.ValidationError("Email body is required.")
        return data


class EmailProposalAnswerSerializer(serializers.Serializer):
    """Serializer for handling answer mail proposal data."""

    email_subject = serializers.CharField()
    email_content = serializers.CharField()


class EmailGenerateAnswer(serializers.Serializer):
    """Serializer for handling generated email answer data."""

    email_subject = serializers.CharField()
    email_content = serializers.CharField()
    response_type = serializers.CharField()


# ----------------------- USER  SERIALIZER -----------------------#
class PreferencesSerializer(serializers.ModelSerializer):
    """Serializer for handling 'Preferences' model data in API interactions."""

    class Meta:
        model = Preference
        fields = ["bg_color"]


class UserLoginSerializer(serializers.ModelSerializer):
    """Serializer for retrieving user login data through a GET request."""

    class Meta:
        model = User
        fields = ["login"]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "email", "username", "provider_id"]


# ----------------------- RULE  SERIALIZER -----------------------#
class RuleSerializer(serializers.ModelSerializer):
    """Serializer for handling 'Rule' model data in API interactions."""

    class Meta:
        model = Rule
        fields = ["id", "info_AI", "priority", "block", "category", "user", "sender"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        """Create method for handling the creation of a new 'Rule' instance."""
        user = self.context.get("user")
        category = validated_data.get("category")

        if category is None or category == "":
            validated_data.pop("category", None)

        return Rule.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        """Update method for handling the update of an existing 'Rule' instance."""
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


class RuleBlockUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ("block",)  # We only want the block field


class SenderSerializer(serializers.ModelSerializer):
    """Serializer for handling 'Sender' model data in API interactions."""

    class Meta:
        model = Sender
        fields = ["id", "email", "name"]


class NewEmailAISerializer(serializers.Serializer):
    """Serializer for handling data required for new AI email processing."""

    input_data = serializers.CharField()
    length = serializers.CharField()
    formality = serializers.CharField()


class EmailAIRecommendationsSerializer(serializers.Serializer):
    """Serializer for handling AI recommendations for email content."""

    mail_content = serializers.CharField()
    user_recommendation = serializers.CharField()
    email_subject = serializers.CharField(allow_blank=True)


# ----------------------- EMAIL SERIALIZER -----------------------#
class MessageSerializer(serializers.ModelSerializer):
    """Serializer for the 'Message' model to handle API data."""

    class Meta:
        model = Message
        fields = ["text"]


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the 'User' model to handle API data."""

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")


class CategoryNameSerializer(serializers.ModelSerializer):
    """Serializer for retrieving category names and descriptions (GET request)."""

    class Meta:
        model = Category
        fields = ("name", "description")


class NewCategorySerializer(serializers.ModelSerializer):
    """Serializer for creating a new category, including 'name', 'description', and 'user'."""

    class Meta:
        model = Category
        fields = ("name", "description", "user")


class UserEmailSerializer(serializers.ModelSerializer):
    """Serializer for retrieving user email data through a GET request."""

    class Meta:
        model = Email
        fields = ("email_short_summary", "content", "subject", "priority")


class BulletPointSerializer(serializers.ModelSerializer):
    """Serializer for retrieving all bullet points through a GET request."""

    class Meta:
        model = BulletPoint
        fields = "__all__"  # Retrieve all fields of BulletPoints
