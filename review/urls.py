from django.urls import path
from . import views


urlpatterns = [
    path('<int:goods_id>/', views.ReviewAPIView.as_view(), name='review'),
    path('list/<int:user_id>/', views.UserInfoAPIView.as_view(), name='review_list'),
]
