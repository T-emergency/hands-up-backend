from django.urls import path
from . import views

urlpatterns = [
    # path('<int:goods_id>/',views.ChatRoomView.as_view(), name='chat_room'),
    # path('list/',views.ChatRoomList.as_view(), name='chat_list'),
    # path('<int:goods_id>/check_msg/<int:user_id>/',views.ChatMessageChek.as_view(), name='chat_msg'),
    # path('wait_msg/<int:goods_id>/',views.ChatMessageWaitCount.as_view(), name='chat_wait_msg'),
    # 맨 처음 리스트만 가져옴 - 읽지 않은 것 또한 포함 시켜서?
    # 방 클릭시 리스트들 가져옴
    path('',views.ChatViewSet.as_view({'get' : 'list'}), name='chat_room_list'),
    path('goods/<int:pk>/',views.ChatViewSet.as_view({'get' : 'retrieve'}), name='chat_room_list'),

]
