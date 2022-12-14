from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from .models import ReportArticle,ReportArticleComment,FreeArticle, FreeArticleComment
from rest_framework.pagination import PageNumberPagination
from .serializers import (
    ReportArticleSerializer,
    ReportArticleCommentSerializer, 
    FreeCreateSerializer, 
    FreeListSerializer, 
    FreeDetailSerializer, 
    FreeCommentSerializer,
)


class ReportListArticleView(APIView,PageNumberPagination):
    page_size=12
    def get(self,request):
        articles = ReportArticle.objects.all()
        print(articles)
        results = self.paginate_queryset(articles, request, view=self)
        serializer = ReportArticleSerializer(results,many=True)
        return self.get_paginated_response(serializer.data)

    def post(self,request):
        serializer = ReportArticleSerializer(data=request.data)
        print(request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response('faild',status=status.HTTP_400_BAD_REQUEST)



class ReportArticleDetailView(APIView):

    def get(self,request,report_article_id):
        article=get_object_or_404(ReportArticle,id=report_article_id)
        serializer = ReportArticleSerializer(article)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,report_article_id):
        article=get_object_or_404(ReportArticle,id=report_article_id)
        serializer=ReportArticleSerializer(article, data=request.data,partial=True)
        if request.user==article.author:
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({"Message": serializer.errors})
        else:        
            return Response('권한이 없습니다',status=status.HTTP_403_FORBIDDEN)

    def delete(self,request,report_article_id):
        article=get_object_or_404(ReportArticle,id=report_article_id)
        if request.user==article.author:
            article.delete()
            return Response('delete seccees',status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('권한이 없습니다',status=status.HTTP_403_FORBIDDEN)



class ReportCommentAPIView(APIView,PageNumberPagination):
    page_size=5
    def get(self,request,report_article_id):
        comment=ReportArticleComment.objects.filter(article=report_article_id)
        results = self.paginate_queryset(comment, request, view=self)
        serializer=ReportArticleCommentSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self,request,report_article_id):
        # article=get_object_or_404(ReportArticle,id=report_article_id)
        serializer = ReportArticleCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user,article_id=report_article_id)
            return Response({'message':'succees create','data':serializer.data})
        else:
            return Response({"Message": serializer.errors})



    def put(self,request,report_article_id,report_article_comment_id):
        article=get_object_or_404(ReportArticle,id=report_article_id)
        comment=get_object_or_404(ReportArticleComment,id=report_article_comment_id,article_id=report_article_id)
        serializer=ReportArticleCommentSerializer(comment,data=request.data,partial=True)
        if serializer.is_valid():
           serializer.save(author=request.user,article=article)
           return Response({'succees':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response('권한이 없습니다',status=status.HTTP_403_FORBIDDEN)

    def delete(self,request,report_article_id,report_article_comment_id):
        comment=get_object_or_404(ReportArticleComment,id=report_article_comment_id,article_id=report_article_id)
        if request.user==comment.author:
            comment.delete()
            return Response('seccees',status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('권한이 없습니다',status=status.HTTP_403_FORBIDDEN)



#자유게시판 전체 리스트
class FreeListView(APIView, PageNumberPagination):
    page_size = 12
    def get(self, request):
        freearticle = FreeArticle.objects.all()
        results = self.paginate_queryset(freearticle, request, view=self)
        serializer = FreeListSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


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
        try:
            free_article.hits = free_article.hits+1
            free_article.save()
        except:
            pass
        serializer = FreeDetailSerializer(free_article)
        return Response(serializer.data, status=status.HTTP_200_OK)


#자유게시판 수정
    def put(self, request, free_article_id):        
        free_article = get_object_or_404(FreeArticle, id=free_article_id)
        if request.user == free_article.author:
            serializer = FreeDetailSerializer(free_article, data=request.data, partial=True)
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
class FreeCommentView(APIView, PageNumberPagination):
    page_size=5
    def get(self, request, free_article_id):
        free_article_comment = FreeArticleComment.objects.filter(article=free_article_id)
        results = self.paginate_queryset(free_article_comment, request, view=self)
        serializer = FreeCommentSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

#자유게시판 댓글 작성
    def post(self, request, free_article_id):
        serializer = FreeCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, article_id=free_article_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#자유게시판 댓글 수정

    def put(self, request, free_article_id, free_comment_id):
        comment = get_object_or_404(FreeArticleComment, article_id=free_article_id, id=free_comment_id)
        if request.user == comment.author:
            serializer = FreeCommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, article_id=free_article_id)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)

#자유게시판 댓글 삭제
    def delete(self, request, free_article_id, free_comment_id):
        comment= get_object_or_404(FreeArticleComment, id=free_comment_id)
        if request.user == comment.author:
            comment.delete()
            return Response({"message":"댓글 삭제 완료"},status=status.HTTP_200_OK)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)
