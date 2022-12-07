from django.urls import path
from . import views

urlpatterns = [
    path('', views.GoodsPostView.as_view(), name='goods_post_view'),
]
