from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import permissions

from .models import Goods
from user.models import User
from .serializers import GoodsSerializer
from rest_framework.pagination import PageNumberPagination

class GoodsView(APIView):

    def get(self, request):
        goods = Goods.objects.all()
        serializer = GoodsSerializer(goods, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = GoodsSerializer(data=request.data, context={'request':request})
        
        if serializer.is_valid():
            serializer.save(seller=request.user)
            
            return Response(serializer.data)
        else:
            return Response({'message': serializer.errors})
        g
        
class GoodsDetailView(APIView):
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
