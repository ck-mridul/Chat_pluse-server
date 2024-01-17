from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/peerchat/<int:userId>/', consumers.ChatConsumer.as_asgi()),
]