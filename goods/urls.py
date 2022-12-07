from django.urls import path
from .views import GoodsAPI#,Test

urlpatterns = [
    path('',GoodsAPI.as_view(), name='goods_api'),
    # path('test/', Test.as_view(),name='test'),
]
