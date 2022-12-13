from django.urls import path
from . import views

urlpatterns = [
    path('<int:goods_id>/',views.ChatRoomView.as_view(), name='chat_room'),
    path('list/',views.ChatRoomList.as_view(), name='chat_list'),
]
