from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination

from channels.layers import get_channel_layer
from .consumers import ChatConsumer
from asgiref.sync import async_to_sync
from rest_framework.response import Response
import json

from goods.models import Goods
from .models import TradeChatRoom, TradeMessage
from .serializers import TradeMessageSerializer
from goods.serializers import GoodsSerializer, TradeInfoSerializer
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
class GoodsPagination(PageNumberPagination):
    page_size = 10
    
    def get_paginated_response(self, data):
        return Response(data)


class IsTrader(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user in [obj.goods.seller, obj.goods.buyer]
from django.db.models import Prefetch
# 리스트 일 때는 자기의 방리스트(업데이트 순)와 읽지 않은 메시지 개수와 상품의 정보를 받아야함
    # 1. Goods의 경매 상태가 끝났으며 buyer가 비어있지 않는다.
    # 2. 그리고 내가 판매자거나 낙찰자인경우의 trade_room
    # 3. 업데이트 순으로 정렬
# 특정 채팅방을 클릭 시에는 거래 채팅 방의 id를 가지고 판별
    # - 퍼미션의 경우에는 tradecahtroom의 상품 정보의 판매자 혹은 구매자
    # 1. 방에 해당하는 메시지들이 쿼리 셋이 된다
    # 2. 모두 읽음 처리를 해준다. - 이것은 실시간으로 어떻게 할까 결정
class ChatViewSet(ModelViewSet):
    """
    리스트 'list' 요청이 오면 채팅방 리스트를 보내줍니다.
    특정 방의 요청이 'retrive' 오면 채팅방의 채팅들을 보내줍니다.
    """
    permission_classes = [IsTrader,]
    # queryset = TradeMessage.objects.all().select_related('author', 'trade_room')
    def get_permissions(self):
        if self.action == 'list':
            return [permissions.IsAuthenticated(),]
        return super(ChatViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return TradeInfoSerializer
        elif self.action == 'retrive':
            return TradeMessageSerializer
        else:
            return None
    def get_serializer_context(self):
        # print(self.request.data)
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'action' : self.action
        }
    def get_queryset(self):
        print(dir(Goods.objects.first()))
        user_id = self.request.user.id
        if self.action == 'list':
            goods = Goods.objects.filter(status = False, buyer__isnull=False).filter( Q(buyer_id = user_id) | Q(seller_id = user_id)).select_related('seller', 'buyer', 'trade_room').prefetch_related('trade_room__trademessage')
            return goods
        elif self.action == 'retrive':
            return TradeChatRoom.objects.all()
        else:
            return None