from django.urls import path
from . import views

urlpatterns = [
    path('report_articles/', views.ReportListArticleView.as_view(), name='report_articles_list'),
    path('report_articles/<int:report_article_id>/', views.ReportArticleDetailView.as_view(), name='report_article_detail'),
    path('report_articles/<int:report_article_id>/comment/', views.ReportCommentAPIView.as_view(), name='ReportCommentAPI'),
    path('report_articles/<int:report_article_id>/comment/<int:report_article_comment_id>/', views.ReportCommentAPIView.as_view(), name='reportcomment'),
]
