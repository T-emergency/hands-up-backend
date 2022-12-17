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
from goods.serializers import GoodsSerializer
from django.db.models import Q
# Create your views here.


class ChatView(APIView):

    def get(self, reqeust,goods_id):
        layer = get_channel_layer()
        # print(dir(layer), layer)
        async_to_sync(layer.group_send)(f'chat_{goods_id}', {'type': 'chat_message', 'response': json.dumps({'response_type': 'message', 'message': 'hi'})})
    
        return Response('연결 성공')

    
class ChatRoomView(APIView):
    def get(self, request, goods_id):
        goods = get_object_or_404(Goods, id=goods_id)
        is_trade_room = goods.trade_room_id
        buyer = goods.buyer
        seller = goods.seller
        
        trade_message = TradeMessage.objects.filter(trade_room_id=is_trade_room)
        serializer = TradeMessageSerializer(trade_message,many=True)
        
        if is_trade_room and (request.user == buyer or request.user == seller):
            # print("test: ", buyer, seller,request.user)
            return Response({'message': "입장", "data":serializer.data})
            
        else:
            return Response({'message': "접근 권한이 없습니다"})


class ChatRoomList(APIView):
    def get(self, request):
        user = request.user
        goods = Goods.objects.filter(status = False).filter(Q(buyer_id=user.id)|Q(seller_id=user.id) & Q(trade_room__isnull=False) )

        context = {
            "request": request,
            "action": "list"
        }
        serializer = GoodsSerializer(goods,many=True, context=context)
        
        return Response(serializer.data)
    


class ChatMessageChek(APIView):
    
    # def get(self, request, goods_id,user_id):
    #     messages = 
    #     serializer = TradeMessageSerializer()
    
    def post(self, request, goods_id,user_id):
        
        if user_id == None:
            return Response("읽을 메세지가 없습니다")
        
        goods = Goods.objects.get(id=goods_id)
        message_list = TradeMessage.objects.filter(author_id=user_id, trade_room_id=goods.trade_room_id)
        
        for message in message_list:
            message.is_read = request.data["is_read"]
            message.save()
        return Response("메세지 읽기 성공")
    
    
class ChatMessageWaitCount(APIView):
    def get(self, request, goods_id):

        goods = get_object_or_404(Goods, id=goods_id)
        messages = TradeMessage.objects.filter(trade_room_id=goods.trade_room_id, is_read=0).exclude(author_id=request.user.id)

        serializer = TradeMessageSerializer(messages,many=True)
        
        return Response(serializer.data)