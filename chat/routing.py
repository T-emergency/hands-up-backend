from django.urls import path

from . import consumers#, read_only

websocket_urlpatterns = [
    path('ws/auction/<int:goods_id>/', consumers.ChatConsumer.as_asgi()),
    path('ws/chat/<int:goods_id>/', consumers.ChatConsumerDirect.as_asgi()),
    path('ws/alram/<int:user_id>/', consumers.AlramConsumer.as_asgi()),
    # path('chat/<int:goods_id>/', read_only.ChatConsumer.as_asgi()),
]