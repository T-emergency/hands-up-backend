from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from channels.layers import get_channel_layer
from .consumers import ChatConsumer
from asgiref.sync import async_to_sync
from rest_framework.response import Response
import json

from goods.models import Goods
from .models import TradeMessage
from .serializers import TradeMessageSerializer
# Create your views here.


    
class ChatRoomView(APIView):
    def get(self, request, goods_id):
        goods = get_object_or_404(Goods, id=goods_id)
        is_trade_room = goods.trade_room_id
        buyer = goods.buyer
        seller = goods.seller
        
        trade_message = TradeMessage.objects.filter(trade_room_id=is_trade_room)
        serializer = TradeMessageSerializer(trade_message,many=True)
        
        if is_trade_room and (request.user == buyer or request.user == seller):
            print("test: ", buyer, seller,request.user)
            return Response({'message': "입장", "data":serializer.data})
            
        else:
            return Response({'message': "접근 권한이 없습니다"})
