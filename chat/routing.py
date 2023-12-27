from django.urls import path
from .consummers import ChatConsummer,DocumentConsummer

websocket_urlpatterns = [
    path('ws/chat/<str:room_id>/',ChatConsummer.as_asgi()),
    path('ws/doc/<str:room_id>/',DocumentConsummer.as_asgi())
]