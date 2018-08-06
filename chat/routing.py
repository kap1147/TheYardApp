# chat/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r'^ws/chat/<str:room_name>/', consumers.ChatConsumer),
]
