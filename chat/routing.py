# from django.conf.urls import url
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('/auction/<int:goods_id>/', consumers.ChatConsumer.as_asgi()),
]