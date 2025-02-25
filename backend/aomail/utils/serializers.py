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
    Agent,
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

    subject = serializers.CharField(required=True, allow_blank=True)
    body = serializers.CharField(required=True, allow_blank=False)

    def validate(self, data):
        """Validate method to check that both email subject and body are provided."""
        if "subject" not in data:
            raise serializers.ValidationError("Subject is required.")
        if "body" not in data or not data["body"].strip():
            raise serializers.ValidationError("Body is required.")
        return data


class EmailCopyWritingSerializer(serializers.Serializer):
    """Serializer for handling email copywriting data."""

    subject = serializers.CharField(required=True, allow_blank=True)
    body = serializers.CharField(required=True, allow_blank=False)

    def validate(self, data):
        """Validate method to check that both email subject and body are provided."""
        if "subject" not in data:
            raise serializers.ValidationError("Subject is required.")
        if "body" not in data or not data["body"].strip():
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
    signature = serializers.CharField()


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
    """Serializer for Rule model with validation."""

    # Make all fields optional by default
    domains = serializers.ListField(required=False, allow_null=True)
    sender_emails = serializers.ListField(required=False, allow_null=True)
    has_attachements = serializers.BooleanField(required=False, allow_null=True)
    categories = serializers.ListField(required=False, allow_null=True)
    priorities = serializers.ListField(required=False, allow_null=True)
    answers = serializers.ListField(required=False, allow_null=True)
    relevances = serializers.ListField(required=False, allow_null=True)
    flags = serializers.ListField(required=False, allow_null=True)
    email_deal_with = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )

    action_transfer_recipients = serializers.ListField(required=False, allow_null=True)
    action_set_flags = serializers.ListField(required=False, allow_null=True)
    action_mark_as = serializers.ListField(required=False, allow_null=True)
    action_delete = serializers.BooleanField(required=False, allow_null=True)
    action_set_category = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    action_set_priority = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    action_set_relevance = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    action_set_answer = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    action_reply_prompt = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )

    class Meta:
        model = Rule
        fields = [
            "id",
            "user",
            "logical_operator",
            # Email triggers
            "domains",
            "sender_emails",
            "has_attachements",
            # AI processing triggers
            "categories",
            "priorities",
            "answers",
            "relevances",
            "flags",
            # AI triggers
            "email_deal_with",
            # Actions
            "action_transfer_recipients",
            "action_set_flags",
            "action_mark_as",
            "action_delete",
            "action_set_category",
            "action_set_priority",
            "action_set_relevance",
            "action_set_answer",
            "action_reply_prompt",
        ]
        read_only_fields = ["id", "user"]

    def validate(self, data):
        """
        Validate the rule data.
        Ensure at least one trigger and one action is specified.
        """
        # Check if at least one trigger is specified
        trigger_fields = [
            "domains",
            "sender_emails",
            "has_attachements",
            "categories",
            "priorities",
            "answers",
            "relevances",
            "flags",
            "email_deal_with",
        ]

        has_trigger = any(data.get(field) for field in trigger_fields)
        if not has_trigger:
            raise serializers.ValidationError(
                "At least one trigger condition must be specified"
            )

        # Check if at least one action is specified
        action_fields = [
            "action_transfer_recipients",
            "action_set_flags",
            "action_mark_as",
            "action_delete",
            "action_set_category",
            "action_set_priority",
            "action_set_relevance",
            "action_set_answer",
            "action_reply_prompt",
        ]

        has_action = any(data.get(field) for field in action_fields)
        if not has_action:
            raise serializers.ValidationError("At least one action must be specified")

        return data

    def create(self, validated_data):
        """Create a new rule with the validated data."""
        user = self.context["user"]
        validated_data["user"] = user

        # Get the category instance if action_set_category is provided
        if (
            "action_set_category" in validated_data
            and validated_data["action_set_category"]
        ):
            category_name = validated_data["action_set_category"]
            category = Category.objects.get(user=user, name=category_name)
            validated_data["action_set_category"] = category

        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context["user"]

        if (
            "action_set_category" in validated_data
            and validated_data["action_set_category"]
        ):
            category_name = validated_data["action_set_category"]
            category = Category.objects.get(user=user, name=category_name)
            validated_data["action_set_category"] = category
        return super().update(instance, validated_data)


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
        fields = ["id", "user", "social_api", "signature_content"]
        read_only_fields = ["id", "user"]


class AgentSerializer(serializers.ModelSerializer):
    """Serializer for the Agent model."""

    class Meta:
        model = Agent
        fields = [
            "id",
            "agent_name",
            "agent_ai_model",
            "ai_template",
            "email_example",
            "length",
            "formality",
            "language",
            "last_used",
            "picture",
            "icon_name",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        user = self.context["request"].user
        return Agent.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
