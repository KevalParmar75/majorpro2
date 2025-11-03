from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('emotion_api/', include('emotion_api.urls')),
    # path('emotion_api/', include('emotion_api.urls')),
]
