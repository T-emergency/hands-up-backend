from django.urls import path
from . import views

urlpatterns = [
    path('<int:goods_id>/',views.ChatRoomView.as_view(), name='chat_room'),
    path('list/',views.ChatRoomList.as_view(), name='chat_list'),
    path('<int:goods_id>/check_msg/<int:user_id>/',views.ChatMessageChek.as_view(), name='chat_msg'),
    path('wait_msg/<int:goods_id>/',views.ChatMessageWaitCount.as_view(), name='chat_wait_msg'),
    
]
