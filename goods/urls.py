from django.urls import path
from . import views

urlpatterns = [
    path('', views.GoodsView.as_view({'get' : 'list', 'post' : 'create'}), name='goods_view'),
    path('<int:pk>/', views.GoodsView.as_view({'get' : 'retrieve'})),
    path('user/<int:pk>/', views.UserGoodsView.as_view({'get' : 'list'}), name='user_goods_view'),
# path('', views.GoodsView.as_view(), name='goods_view'),
]