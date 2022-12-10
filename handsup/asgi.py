import os

# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
# from django.core.asgi import get_asgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "handsup.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
# django_asgi_app = get_asgi_application()

# import chat.routing

# application = ProtocolTypeRouter(
#     {
#         "http": django_asgi_app,
#         "websocket": AllowedHostsOriginValidator(
#             AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))
#         ),
#     }
# )

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
from django.core.asgi import get_asgi_application

from .middleware import JwtAuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'handsup.settings')
# 클라이언트와 Channels 개발 서버가 연결 될 때, 어느 protocol 타입의 연결인지
application = ProtocolTypeRouter({
    # (http->django views is added by default)
  	# 만약에 websocket protocol 이라면, AuthMiddlewareStack
    'http': get_asgi_application(),
    'websocket': JwtAuthMiddlewareStack(
        # URLRouter 로 연결, 소비자의 라우트 연결 HTTP path를 조사
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
