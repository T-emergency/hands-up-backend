from django.db.models import Count, Sum, F, Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

from .models import GoodsImage, Goods

from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, permissions


from .models import Goods
from user.models import User
from .serializers import GoodsListSerializer, GoodsSerializer

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.pagination import PageNumberPagination
class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    비로그인 회원은 볼 수 만 있는 퍼미션, 수정과 삭제는 작성자만 가능
    """
    message = "작성자가 아닙니다."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.seller == request.user
class GoodsPagination(PageNumberPagination):
    page_size = 10
    
    def get_paginated_response(self, data):
        return Response(data)



class GoodsView(ModelViewSet):
    serializer_class = GoodsSerializer
    permission_classes = [IsAuthorOrReadOnly,]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    filterset_fields = ["category"]
    search_fields = ['title','content']
    pagination_class = GoodsPagination


    def get_queryset(self):
        status = {'null':None, 'true':True, 'false' : False}
        st = self.request.query_params.get('status', '')
        if st == '':
            queryset = Goods.objects.all().prefetch_related('like','goodsimage_set', 'auctionparticipant_set').select_related('seller', 'buyer')
        else:
            queryset = Goods.objects.filter(status=status[st]).prefetch_related('like','goodsimage_set', 'auctionparticipant_set').select_related('seller', 'buyer')
        return queryset


    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(),] # ()를 붙이는 이유는 super의 get_permissions를 보면 알 수 있다.
        return super(GoodsView, self).get_permissions()


    def get_serializer_context(self):
        print(self.request.data)
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'action' : self.action
        }

    def perform_create(self, serializer):
        serializer.save(seller_id = self.request.user.id)


    @action(detail=False, methods=['GET'])
    def recommend_goods(self, request):

        q = Q(status = True) | Q(status = None)
        recommend_goods = self.get_queryset().filter(q).annotate(participants_count = Count('auctionparticipant')).order_by('-participants_count')[:10]
        serializer = GoodsListSerializer(recommend_goods, many = True, context = self.get_serializer_context())

        return Response(data = serializer.data, status=status.HTTP_200_OK)


class UserGoodsView(ModelViewSet):
    serializer_class = GoodsSerializer
    permission_classes = [IsAuthorOrReadOnly,]
    lookup_field='user_id'

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(),]
        return super(UserGoodsView, self).get_permissions()

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'action' : self.action
        }

    def get_queryset(self):
        return Goods.objects.prefetch_related('like','goodsimage_set',).select_related('seller', 'buyer').filter(seller_id=self.kwargs['user_id'])

    def perform_create(self, serializer):
        serializer.save(seller_id = self.request.user.id)


class GoodsLike(APIView):
    
    def get(self, request, goods_id):
        user = request.user
        goods = get_object_or_404(Goods, pk=goods_id)

        if goods.like.filter(pk=user.id).exists():
            print('unlike')
            goods.like.remove(user)
        else:
            print('like')
            goods.like.add(user)
        return Response(status=status.HTTP_200_OK)
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



