from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import permissions
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet

from .models import Goods
from user.models import User
from .serializers import GoodsSerializer

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    비로그인 회원은 볼 수 만 있는 퍼미션, 수정과 삭제는 작성자만 가능
    """
    message = "작성자가 아닙니다."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.seller == request.user

class GoodsView(ModelViewSet):
    queryset = Goods.objects.prefetch_related('like','goodsimage_set').select_related('seller', 'buyer').all()
    serializer_class = GoodsSerializer
    permission_classes = [IsAuthorOrReadOnly,]


    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(),] # ()를 붙이는 이유는 super의 get_permissions를 보면 알 수 있다.
        return super(GoodsView, self).get_permissions()


    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'action' : self.action
        }


    def perform_create(self, serializer):
        serializer.save(seller_id = self.request.user.id)


class UserGoodsView(ModelViewSet):
    serializer_class = GoodsSerializer
    permission_classes = [IsAuthorOrReadOnly,]

    # def get_permissions(self):
    #     if self.action == 'create':
    #         return [permissions.IsAuthenticated(),] # ()를 붙이는 이유는 super의 get_permissions를 보면 알 수 있다.
    #     return super(GoodsView, self).get_permissions()

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'action' : self.action
        }

    def get_queryset(self):
        queryset = Goods.objects.prefetch_related('like','goodsimage_set').select_related('seller', 'buyer').all()
        return queryset.filter(seller_id=self.kwargs['pk'])

    def perform_create(self, serializer):
        serializer.save(seller_id = self.request.user.id)



# #############
# class GoodsView(APIView):

#     def get(self, request):
#         goods = Goods.objects.all()
#         serializer = GoodsSerializer(goods, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = GoodsSerializer(data=request.data, context={'request':request})

#         if serializer.is_valid():
#             serializer.save(seller=request.user)

#             return Response(serializer.data)
#         else:
#             return Response({'message': serializer.errors})
#     def perform_create(self, serializer):
#         serializer.save(seller_id = self.request.user.id)




# from rest_framework import status
# class GoodsView(APIView):

#     def get(self, request):
#         goods = Goods.objects.all()
#         serializer = GoodsSerializer(goods, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = GoodsSerializer(data=request.data, context={'request':request})
        
#         if serializer.is_valid():
#             serializer.save(seller=request.user)
            
#             return Response(serializer.data)
#         else:
#             return Response({'message': serializer.errors})
        
        
# class GoodsDetailView(APIView):
#     def get(self, request, goods_id):
#         goods = get_object_or_404(Goods, pk=goods_id)
#         serializer = GoodsSerializer(goods)
#         return Response(serializer.data)
    
#     def put(self, request, goods_id):
#         goods = get_object_or_404(Goods, pk=goods_id)
#         if request.user == goods.seller:
#             serializer = GoodsSerializer(goods, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save(seller=request.user)
#                 return Response(serializer.data)
#             else:
#                 return Response({'message':serializer.errors})
    
#     def delete(self, request, goods_id):
#         goods = get_object_or_404(Goods, pk=goods_id)
#         if request.user == goods.seller:
#             goods.delete()
#             return Response({"message": "삭제 완료"})
#         else:
#             return Response({"message":"권한이 없습니다"})


# class GoodsLike(APIView):
    
#     def get(self, request, goods_id):
#         user = request.user
#         goods = get_object_or_404(Goods, pk=goods_id)

#         if goods.like.filter(pk=user.id).exists():
#             print('unlike')
#             goods.like.remove(user)
#         else:
#             print('like')
#             goods.like.add(user)

#         return Response(status=status.HTTP_200_OK)
        serializer.save(seller_id = self.request.user.id)
