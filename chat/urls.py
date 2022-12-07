from django.urls import path
from .views import AuctionChatRoomView,AuctionChatRoomDetailView

urlpatterns = [
    path('', AuctionChatRoomView.as_view(), name='auction_chatroom'),
    path('<int:room_id>/', AuctionChatRoomDetailView.as_view(), name='auction_chatroom_id'),
    
]
