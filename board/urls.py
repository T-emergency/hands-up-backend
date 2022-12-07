from django.urls import path

from . import views

urlpatterns = [
    #자유게시판 url
    path('', views.FreeListView.as_view(), name='free_list_view'),
    path('free_articles/', views.FreeCreateView.as_view(), name='free_create_view'),
    path('detail/<int:free_article_id>/', views.FreeDetailView.as_view(), name='free_detail_view'),
]
