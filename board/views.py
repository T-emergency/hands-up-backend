from django.shortcuts import get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ReportArticleSerializer,ReportArticleCommentSerializer
from django.shortcuts import get_object_or_404
from user.models import User
from .models import ReportArticle,ReportArticleComment

class ReportListArticleView(APIView):

    def get(self,request):
        articles = ReportArticle.objects.all()
        serializer = ReportArticleSerializer(articles,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        serializer = ReportArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({"message":'succees',"data":serializer.data},status=status.HTTP_201_CREATED)
        else:
            return Response('faild',status=status.HTTP_400_BAD_REQUEST)



class ReportArticleDetailView(APIView):

    def get(self,request,report_article_id):
        article=get_object_or_404(ReportArticle,id=report_article_id)
        serializer = ReportArticleSerializer(article)
        return Response({'get succees':serializer.data},status=status.HTTP_200_OK)

    def put(self,request,report_article_id):
        article=get_object_or_404(ReportArticle,id=report_article_id)
        serializer=ReportArticleSerializer(article, data=request.data,partial=True)
        if request.user==article.author:
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response({'put succees':serializer.data},status=status.HTTP_200_OK)
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

class ReportCommentAPIView(APIView):
    def get(self,request,report_article_id):
        comment=ReportArticleComment.objects.all()
        serializer=ReportArticleCommentSerializer(comment, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,report_article_id):
        article=get_object_or_404(ReportArticle,id=report_article_id)
        serializer = ReportArticleCommentSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save(author=request.user,article=article)
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