from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from board.serializers import (FreeCreateSerializer, FreeListSerializer, FreeDetailSerializer, 
FreeCommentSerializer)
from .models import FreeArticle, FreeArticleComment

#자유게시판 전체 리스트
class FreeListView(APIView):
    def get(self, request):
        freearticle = FreeArticle.objects.all()
        serializer = FreeListSerializer(freearticle, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#자유게시판 등록
class FreeCreateView(APIView):
    def post(self, request):
        serializer = FreeCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#자유게시판 상세
class FreeDetailView(APIView):
    def get(self, request, free_article_id):
        free_article = get_object_or_404(FreeArticle, id=free_article_id)
        if request.user == free_article.author:
            serializer = FreeDetailSerializer(free_article)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)

#자유게시판 수정
    def put(self, request, free_article_id):        
        free_article = get_object_or_404(FreeArticle, id=free_article_id)
        if request.user == free_article.author:
            serializer = FreeCreateSerializer(free_article, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)

#자유게시판 삭제
    def delete(self, request, free_article_id):        
        freearticle = get_object_or_404(FreeArticle, id=free_article_id)
        if request.user == freearticle.author:
            freearticle.delete()
            return Response({"message":"게시글 삭제"}, status=status.HTTP_200_OK)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)

#자유게시판 댓글 조회
class FreeCommentListView(APIView):
    def get(self, request, free_article_id):
        freearticle = get_object_or_404(FreeArticle, id=free_article_id)
        comments = freearticle.comment.all()
        serializer = FreeCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#자유게시판 댓글 작성
    def post(self, request, free_article_id):
        serializer = FreeCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, free_article_id=free_article_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#자유게시판 댓글 수정
class FreeCommentDetailView(APIView):
    def get(self, request, free_article_id, free_comment_id):
        comment = get_object_or_404(FreeArticleComment, article_id=free_article_id, id=free_comment_id)
        serializer = FreeCommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, free_article_id, free_comment_id):
        comment = get_object_or_404(FreeArticleComment, article_id=free_article_id, id=free_comment_id)
        if request.user == comment.user:
            serializer = FreeCommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, free_article_id=free_article_id)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)

#자유게시판 댓글 삭제
    def delete(self, request, free_article_id, free_comment_id):
        comment= get_object_or_404(FreeArticleComment, id=free_comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response({"message":"댓글 삭제 완료"},status=status.HTTP_200_OK)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)
