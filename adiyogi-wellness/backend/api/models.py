from django.db import models
from django_mongodb_backend.fields import ObjectIdAutoField  # type: ignore


class Session(models.Model):
    """
    Therapy chat session.
    """
    id = ObjectIdAutoField(primary_key=True)
    session_id = models.CharField(max_length=100, unique=True)
    issue = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sessions"

    def __str__(self) -> str:
        return self.session_id


class Message(models.Model):
    """
    Single message/turn in a therapy session.
    """
    id = ObjectIdAutoField(primary_key=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=20)  # "user" or "assistant"
    text = models.TextField()
    emotion = models.CharField(max_length=50, blank=True)
    extra = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "messages"

    def __str__(self) -> str:
        return f"{self.role}: {self.text[:40]}"