from channels.db import database_sync_to_async
from urllib.parse import parse_qs
from django.db import close_old_connections


@database_sync_to_async
def get_user_from_token(token):
    from django.contrib.auth.models import AnonymousUser
    from rest_framework_simplejwt.tokens import AccessToken
    from .models import User
    try:
        access_token = AccessToken(token)
        user = access_token.payload.get('user_id')
        return User.objects.get(id=user)
    except Exception:
        return AnonymousUser()
    
class TokenAuthMiddleWare:
    def __init__(self, app):
        self.app = app
 
    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"]
        query_params = query_string.decode()
        query_dict = parse_qs(query_params)
        token = query_dict["token"][0]
        user = await get_user_from_token(token)
        scope["user"] = user
        close_old_connections()
        return await self.app(scope, receive, send)