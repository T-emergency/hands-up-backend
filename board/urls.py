from django.urls import path

from . import views

urlpatterns = [
    #자유게시판 url
    path('free_articles/', FreeListView.as_view(), name='free_list_view')

]
