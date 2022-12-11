from django.urls import path
from goods import views

urlpatterns = [
    path('', views.GoodsView.as_view({'get' : 'list', 'post' : 'create'}), name='goods_list_view'),
    path('<int:pk>/', views.GoodsView.as_view({'get' : 'retrieve'})),
]
