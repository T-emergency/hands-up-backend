from django.urls import path
from .views import GoodsAPI

urlpatterns = [
    path('',GoodsAPI.as_view(), name='goods_api'),
]
