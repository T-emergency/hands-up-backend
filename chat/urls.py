from django.urls import path
from chat import views

urlpatterns = [
    path('<int:goods_id>/', views.ChatView.as_view()),
    # path('/', FreeListView.as_view(), name='free_list_view')
]