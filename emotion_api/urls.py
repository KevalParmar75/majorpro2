from django.urls import path
from . import views
from .views import detect_emotion, analyze_emotion

urlpatterns = [
    path('detect/', detect_emotion),
    path('test/', views.test_connection, name='test_connection'),
    path('analyze/', analyze_emotion, name='analyze_emotion'),
]
