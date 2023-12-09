from django.urls import path
from .consummers import VideoCallConsummer

websocket_urlpatterns = [
    path('ws/videocall/<str:room_id>/',VideoCallConsummer.as_asgi())
]