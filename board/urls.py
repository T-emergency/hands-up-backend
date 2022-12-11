from django.urls import path
from . import views


urlpatterns = [
    #자유게시판 게시글 url
    path('', views.FreeListView.as_view(), name='free_list_view'),
    path('free_articles/', views.FreeCreateView.as_view(), name='free_create_view'),
    path('detail/<int:free_article_id>/', views.FreeDetailView.as_view(), name='free_detail_view'),
    #자유게시판 댓글 url
    path('free_articles/<int:free_article_id>/comment/', views.FreeCommentView.as_view(), name='free_comment'),
    path('free_articles/<int:free_article_id>/comment/<int:free_article_comment_id>/', views.FreeCommentView.as_view(), name='free_comment_detail'),
    #제보게시판 게시글 url
    path('report_articles/', views.ReportListArticleView.as_view(), name='report_articles_list'),
    path('report_articles/<int:report_article_id>/', views.ReportArticleDetailView.as_view(), name='report_article_detail'),
    #제보게시판 댓글 url
    path('report_articles/<int:report_article_id>/comment/', views.ReportCommentAPIView.as_view(), name='ReportCommentAPI'),
    path('report_articles/<int:report_article_id>/comment/<int:report_article_comment_id>/', views.ReportCommentAPIView.as_view(), name='reportcomment'),
]
