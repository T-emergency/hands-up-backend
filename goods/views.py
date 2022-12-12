from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from .models import Goods
from user.models import User
from .serializers import GoodsSerializer

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
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'action' : self.action
        }

    def perform_create(self, serializer):
        serializer.save(seller_id = self.request.user.id)
