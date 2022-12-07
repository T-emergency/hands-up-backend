from django.urls import path
from . import views

urlpatterns = [
    path('', views.GoodsView.as_view(), name='goods_view'),
]
