from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Session, Message
from .serializers import (
    MessageSerializer,
    SessionSerializer,
    CreateMessageInputSerializer,
)

# Import the real ML function from the ML project.
# If this import ever fails, Django should crash so the issue is visible.
from run_therapy.therapy_turn import run_therapy_turn  # type: ignore


@api_view(["GET"])
def health_check(request):
    """
    Simple health check for monitoring / frontend.
    """
    return Response({"status": "ok"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_message(request):
    """
    Create or reuse a Session and append user + assistant messages.

    Expected JSON:
    {
        "session_id": "string",
        "issue": "anxiety",
        "user_message": "I can't sleep at night"
    }
    """
    input_serializer = CreateMessageInputSerializer(data=request.data)
    if not input_serializer.is_valid():
        return Response(
            {"errors": input_serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    validated = input_serializer.validated_data
    session_id = validated["session_id"]
    issue = validated.get("issue", "")
    user_message = validated["user_message"]

    session, _created = Session.objects.get_or_create(
        session_id=session_id,
        defaults={"issue": issue},
    )

    user_msg = Message.objects.create(
        session=session,
        role="user",
        text=user_message,
        emotion="",
        extra=None,
    )

    # Call real ML turn
    ml_result = run_therapy_turn(issue or session.issue, session_id, user_message)

    assistant_msg = Message.objects.create(
        session=session,
        role="assistant",
        text=ml_result.get("assistant_text", ""),
        emotion=ml_result.get("emotion", ""),
        extra=ml_result.get("extra", {}),
    )

    session_data = SessionSerializer(session).data
    messages_data = MessageSerializer([user_msg, assistant_msg], many=True).data

    return Response(
        {
            "session": session_data,
            "messages": messages_data,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
def get_session_messages(request, session_id: str):
    """
    Get all messages for a given session_id.
    """
    try:
        session = Session.objects.get(session_id=session_id)
    except Session.DoesNotExist:
        return Response(
            {"detail": "Session not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    messages = session.messages.order_by("created_at")
    serializer = MessageSerializer(messages, many=True)
    session_data = SessionSerializer(session).data

    return Response(
        {
            "session": session_data,
            "messages": serializer.data,
        },
        status=status.HTTP_200_OK,
    )
