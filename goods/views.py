from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import GoodsPostSerializer,GoodsImageSerializer
from .models import GoodsImage, Goods

class GoodsPostView(APIView):

    def post(self, request):
        user = request.user
       
        data={
        "title" : request.data.get('title'),
        "category" : request.data.get('category'),
        "start_date" : request.data.get('dateControl'),
        "start_time" : request.data.get('timeControl'),
        "content" : request.data.get('content'),
        "auction_room" : request.data.get('auction_room'),
        "predict_price" :request.data.get('predict_price'),
        "trade_room" : request.data.get('trade_room'),
        "start_price":request.data.get('start_price'),
        }

        print(data)
       
        serialize_post = GoodsPostSerializer(data = data, context={'request':request})
        if serialize_post.is_valid():
            serialize_post.save(seller = user)
            return Response(serialize_post.data)
        print(serialize_post.errors)
        return Response(serialize_post.errors)

    def get(self, request):
        
        posts = Goods.objects.all()
        
        data = GoodsPostSerializer(posts, many=True).data
        return Response(data)


