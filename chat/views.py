from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet, ViewSet
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


class GoodsPagination(PageNumberPagination):
    page_size = 10
    
    def get_paginated_response(self, data):
        return Response(data)


class IsTrader(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.id in [obj.seller_id, obj.buyer_id]

from django.db.models import Prefetch, F

class ChatViewSet(ViewSet):
    """
    리스트 'list' 요청이 오면 채팅방 리스트를 보내줍니다.
    특정 방의 요청이 'retrive' 오면 채팅방의 채팅들을 보내줍니다.
    """
    permission_classes = [IsTrader,]
    
    def get_permissions(self):
        if self.action == 'list':
            return [permissions.IsAuthenticated(),]
        return super(ChatViewSet, self).get_permissions()

    def list(self, request):
        user_id = self.request.user.id
        queryset = Goods.objects.filter(status=False, buyer__isnull=False) \
                                .filter( Q(buyer_id=user_id) | Q(seller_id=user_id)) \
                                .annotate(updated_at=F("trade_room__updated_at")).order_by('-updated_at') \
                                .select_related('seller', 'buyer', 'trade_room') \
                                .prefetch_related('trade_room__trademessage_set', 'goodsimage_set')
        serializer = TradeInfoSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None): # pk = goods_id
        goods = get_object_or_404(Goods, pk=pk)
        self.check_object_permissions(request, goods)
        TradeMessage.objects.filter(trade_room_id=goods.trade_room.id).exclude(author_id = request.user.id).update(
            is_read=True
        )
        queryset = TradeMessage.objects.filter(trade_room_id=goods.trade_room.id).select_related('author').order_by('created_at')
        serializer = TradeMessageSerializer(queryset, many=True)
        
        return Response(serializer.data)


# class ChatView(APIView):

#     def get(self, reqeust):
#         layer = get_channel_layer()
#         print(dir(layer), layer)
#         print(layer.receive_event_loop, layer.receive_count, layer.connection(0))
#         # async_to_sync(layer.group_send)(f'alram_9', {'type': 'chat_message', 'response': json.dumps({'response_type' : 'alram', 'message': 'hi'})})
#         # async_to_sync(layer.send)(f'alram_9', {'type': 'chat_message', 'response': json.dumps({'response_type' : 'alram', 'message': 'hi'})})

#         return Response('연결 성공')