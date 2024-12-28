"""
Handles serialization for various models in API interactions.

A serializer is an object that requires specific parameters and is used to check if the input data is valid (preprocessing).
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from aomail.models import (
    Message,
    Category,
    Email,
    Rule,
    Sender,
    Contact,
    Filter,
    Signature,
)


# ----------------------- EMAIL SERIALIZER -----------------------#
class EmailDataSerializer(serializers.Serializer):
    """Serializer for sending emails (POST request)."""

    to = serializers.ListField(child=serializers.EmailField(), required=True)
    subject = serializers.CharField(required=True)
    message = serializers.CharField(required=False, allow_blank=True)
    cc = serializers.ListField(child=serializers.EmailField(), required=False)
    bcc = serializers.ListField(child=serializers.EmailField(), required=False)
    attachments = serializers.ListField(child=serializers.FileField(), required=False)


class EmailScheduleDataSerializer(serializers.Serializer):
    """Serializer for scheduling emails (POST request)."""

    to = serializers.ListField(child=serializers.EmailField(), required=True)
    subject = serializers.CharField(required=True)
    message = serializers.CharField(required=False, allow_blank=True)
    cc = serializers.ListField(child=serializers.EmailField(), required=False)
    bcc = serializers.ListField(child=serializers.EmailField(), required=False)
    attachments = serializers.ListField(child=serializers.FileField(), required=False)
    datetime = serializers.DateTimeField(required=True)


class EmailCorrectionSerializer(serializers.Serializer):
    """Serializer for handling email correction data."""

    subject = serializers.CharField(required=True, allow_blank=False)
    body = serializers.CharField(required=True, allow_blank=False)

    def validate(self, data):
        """Validate method to check that both email subject and body are provided."""
        if "subject" not in data or not data["subject"].strip():
            raise serializers.ValidationError("Subject is required.")
        if "body" not in data or not data["body"].strip():
            raise serializers.ValidationError("Body is required.")
        return data


class EmailCopyWritingSerializer(serializers.Serializer):
    """Serializer for handling email copywriting data."""

    subject = serializers.CharField(required=True, allow_blank=False)
    body = serializers.CharField(required=True, allow_blank=False)

    def validate(self, data):
        """Validate method to check that both email subject and body are provided."""
        if "subject" not in data or not data["subject"].strip():
            raise serializers.ValidationError("Subject is required.")
        if "body" not in data or not data["email_body"].strip():
            raise serializers.ValidationError("Body is required.")
        return data


class EmailProposalAnswerSerializer(serializers.Serializer):
    """Serializer for handling answer mail proposal data."""

    subject = serializers.CharField()
    body = serializers.CharField()


class EmailGenerateAnswer(serializers.Serializer):
    """Serializer for handling generated email answer data."""

    subject = serializers.CharField()
    body = serializers.CharField()
    keyword = serializers.CharField()


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
        fields = ("block",)


class SenderSerializer(serializers.ModelSerializer):
    """Serializer for handling 'Sender' model data in API interactions."""

    class Meta:
        model = Sender
        fields = ["id", "email", "name"]


class NewEmailAISerializer(serializers.Serializer):
    """Serializer for handling data required for new AI email processing."""

    inputData = serializers.CharField()
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


# ----------------------- FILTER SERIALIZER -----------------------#
class FilterSerializer(serializers.ModelSerializer):
    """Base serializer for Filter model."""

    social_api = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    relevance = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    answer = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Filter
        fields = (
            "user",
            "name",
            "category",
            "social_api",
            "important",
            "informative",
            "useless",
            "read",
            "spam",
            "scam",
            "newsletter",
            "notification",
            "meeting",
            "relevance",
            "answer",
        )


class SignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signature
        fields = ['id', 'user', 'social_api', 'signature_content']
        read_only_fields = ['id', 'user']
