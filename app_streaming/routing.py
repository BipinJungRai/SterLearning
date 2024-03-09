from django.urls import path
from . import consumers

ws_urlpatterns = [
    path('ws/quiz-stream', consumers.QuizConsumer.as_asgi()),
]
