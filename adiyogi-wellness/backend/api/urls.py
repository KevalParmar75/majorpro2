from django.urls import path
from .views import create_message, get_session_messages, health_check

urlpatterns = [
    path("health/", health_check, name="health"),
    path("message/", create_message, name="create_message"),
    path("session/<str:session_id>/messages/", get_session_messages, name="session_messages"),
]
