from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Goods, BidPrice, GoodsImage
from user.models import User
from .serializers import GoodsSerializer, GoodsImageSerializer,BidPriceSerializer
from chat.serializers import AuctionChatRoom

class GoodsAPI(APIView):
    def get(self, request):
        goods = Goods.objects.all()
        serializer = GoodsSerializer(goods, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        auction_room = AuctionChatRoom.objects.create()
        serializer = GoodsSerializer(data=request.data, context={'auction_room':auction_room})
        
        if serializer.is_valid():
            serializer.save(seller=request.user)
            
            return Response(serializer.data)
        else:
            return Response({'message': serializer.errors})