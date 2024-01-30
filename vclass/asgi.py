"""
ASGI config for vclass project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import os
import django
django.setup()
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from videoCalling import routing as videocallRouter
from chat import routing as chatRouter
from peerChat import routing as peerChat
from authentication.middleware import TokenAuthMiddleWare


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vclass.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket':
TokenAuthMiddleWare(
 #       AllowedHostsOriginValidator(
            URLRouter(
        videocallRouter.websocket_urlpatterns +
        chatRouter.websocket_urlpatterns +
        peerChat.websocket_urlpatterns
    )
       )
  #  )
})
