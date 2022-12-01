from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import GoodsPostSerializer
from .models import GoodsImage, Goods

class GoodsPostView(APIView):
    def post(self, request):
        print('post views실행')
        user = request.user

        serialize_post = GoodsPostSerializer(data = request.data, context={'request':request}) #request받기
        # 유효성 검사
        print('vaild 직전')
        if serialize_post.is_valid():
            serialize_post.save(seller = user)
            print('저장완료?')
            # print(serialize_post.data['image'])
            # if serialize_post.data['image']:
            #     pass
            # GoodsImage.objects.create(
            # goods = Goods.objects.get(id = serialize_post.data['id']),
            # image = request.data['image']
            # )
            return Response(serialize_post.data)
        print(serialize_post.errors)
        return Response(serialize_post.errors)


