from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import GoodsPostSerializer,GoodImageSerializer
from .models import GoodsImage, Goods

class GoodsPostView(APIView):

    def post(self, request):
        print('post views실행')
        user = request.user
        image={
            "image" : request.data.get('image'),
        }
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
        serialize_image = GoodImageSerializer(data = image)
        serialize_post = GoodsPostSerializer(data = data, context={'request':request}) #request받기
        # 유효성 검사
        print('vaild 직전')
        if serialize_post.is_valid():
            serialize_post.save(seller = user)
            return Response(serialize_post.data)
        print(serialize_post.errors)
        return Response(serialize_post.errors)

    def get(self, request):
        image = GoodsImage.objects.get(id=1)
        post = Goods.objects.get(id = 8)

        post_data = GoodsPostSerializer(post)
        image_data = GoodImageSerializer(image)

        data ={
            "post":post_data.data,
            "image":image_data.data
        }
        return Response(data)


