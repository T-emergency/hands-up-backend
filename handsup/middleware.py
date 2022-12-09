from user.models import User
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
# from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from django.db import close_old_connections
from urllib.parse import parse_qs
from jwt import decode as jwt_decode
from django.conf import settings

@database_sync_to_async
def get_user(validated_token):
    try:
        user = get_user_model().objects.get(id=validated_token["user_id"])
        print("user: ", user)
        return user
    except User.DoesNotExist:
        print("user: x",)
        return AnonymousUser()


class JwtAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        close_old_connections()
        print(parse_qs(scope["query_string"]))
        
        try:
            token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
            print("token: ",token)
            UntypedToken(token)
        except:
            scope["user"] = AnonymousUser()
        else:
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            scope["user"] = await get_user(validated_token=decoded_data)
        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))

# class JwtAuthMiddleware(BaseMiddleware):
#     def __init__(self, inner):
#         self.inner = inner

#     async def __call__(self, scope, receive, send):
#         close_old_connections()
#         print(parse_qs(scope["query_string"]))
#         token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
#         print("token: ",token)
#         try:
#             UntypedToken(token)
#         except (InvalidToken, TokenError) as e:
#             return None
#         else:
#             decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#             scope["user"] = await get_user(validated_token=decoded_data)
#         return await super().__call__(scope, receive, send)


# def JwtAuthMiddlewareStack(inner):
#     return JwtAuthMiddleware(AuthMiddlewareStack(inner))