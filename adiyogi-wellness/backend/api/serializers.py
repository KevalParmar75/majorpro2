from rest_framework import serializers
from .models import Session, Message


class SessionSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)  # ObjectId as string

    class Meta:
        model = Session
        fields = ["id", "session_id", "issue", "created_at"]


class MessageSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)      # ObjectId as string
    session = serializers.CharField(read_only=True) # session ObjectId as string

    class Meta:
        model = Message
        fields = [
            "id",
            "session",
            "role",
            "text",
            "emotion",
            "extra",
            "created_at",
        ]


class CreateMessageInputSerializer(serializers.Serializer):
    """
    Input contract for POST /api/message/
    """
    session_id = serializers.CharField(max_length=100)
    issue = serializers.CharField(max_length=100, required=False, allow_blank=True)
    user_message = serializers.CharField()
