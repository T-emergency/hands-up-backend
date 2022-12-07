from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

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
        serializer = GoodsSerializer(data=request.data)
        
        if serializer.is_valid():
            auction_room = AuctionChatRoom.objects.create()
            serializer.save(seller=request.user, auction_room=auction_room)
            
            return Response(serializer.data)
        else:
            return Response({'message': serializer.errors})
        
        
class GoodsDetailViewAPI(APIView):
    def get(self, request, goods_id):
        goods = get_object_or_404(Goods, pk=goods_id)
        serializer = GoodsSerializer(goods)
        return Response(serializer.data)
    
    def put(self, request, goods_id):
        goods = get_object_or_404(Goods, pk=goods_id)
        if request.user == goods.seller:
            serializer = GoodsSerializer(goods, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(seller=request.user)
                return Response(serializer.data)
            else:
                return Response({'message':serializer.errors})
    
    def delete(self, request, goods_id):
        goods = get_object_or_404(Goods, pk=goods_id)
        if request.user == goods.seller:
            goods.delete()
            return Response({"message": "삭제 완료"})
        else:
            return Response({"message":"권한이 없습니다"})
        
        

# from datetime import date, datetime, timedelta
# import pytz

# class Test(APIView):
#     def get(self,request):
#         today = date.today()
#         start_time = datetime.now().time().strftime('%H:%M')
#         print("start_time: ",start_time)
#         auction_start_list = Goods.objects.filter(start_date=date.today(), start_time=start_time)
#         print(auction_start_list)
#         if auction_start_list.exists():
#             for goods in auction_start_list:
#                 goods.status = True
#                 goods.save()
        
#         end_time = (datetime.now() - timedelta(minutes=20)).time().strftime('%H:%M')
#         print("end_time: ",end_time)
#         auction_end_list = Goods.objects.filter(status=True, start_date=date.today(), start_time=end_time)
#         print(auction_end_list)
#         if auction_end_list.exists():
#             for goods in auction_end_list:
#                 goods.status = False
#                 goods.save()
            
#         serializer1 = GoodsSerializer(auction_start_list,many=True)
#         serializer2 = GoodsSerializer(auction_end_list,many=True)
#         data = {
#             'start': serializer1.data,
#             'end': serializer2.data,
#         }
        
#         return Response({"mesaage":"정보","data":data})