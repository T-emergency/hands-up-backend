from django.urls import path
from . import views


urlpatterns = [
    path('<int:goods_id>/', views.ReviewAPIView.as_view(), name='review'),
    # path('<int:user_id>/', views.ReviewListAPIView.as_view(), name='review_list'),
    # path('/', FreeListView.as_view(), name='free_list_view')
]
