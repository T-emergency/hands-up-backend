from django.urls import path

from . import consumers#, read_only

websocket_urlpatterns = [
    path('auction/<int:goods_id>/', consumers.ChatConsumer.as_asgi()),
    path('chat/<int:goods_id>/', consumers.ChatConsumerDirect.as_asgi()),
    # path('chat/<int:goods_id>/', read_only.ChatConsumer.as_asgi()),
]