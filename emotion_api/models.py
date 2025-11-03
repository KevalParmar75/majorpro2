# Create your models here.
from django.db import models

class MoodLog(models.Model):
    user = models.CharField(max_length=100)
    emotion = models.CharField(max_length=50)
    confidence = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
