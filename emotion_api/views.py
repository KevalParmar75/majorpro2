from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from transformers import pipeline
from django.shortcuts import render

emotion_model = pipeline("sentiment-analysis", model="j-hartmann/emotion-english-distilroberta-base")

@api_view(['POST'])
def detect_emotion(request):
    text = request.data.get("text", "")
    result = emotion_model(text)[0]
    return Response(result)

@api_view(['POST'])
def analyze_emotion(request):
    text = request.data.get('text', '')
    if not text:
        return Response({'error': 'No text provided'}, status=400)

    result = emotion_model(text)[0]
    return Response({
        'emotion': result['label'],
        'score': round(result['score'], 3)
    })

def test_connection(request):
    return JsonResponse({"message": "Connection successful! React ↔ Django working ✅"})