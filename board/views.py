from django.shortcuts import get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FreeArticle

#자유게시판 전체 리스트
class FreeListView(APIView):
    def get(self, request):
        freearticle = FreeArticle.objects.filter(user=request.user.id)
        serializer = FreeArticleSerializer(freearticle, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)