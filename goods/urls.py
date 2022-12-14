from django.urls import path
from goods import views

urlpatterns = [
    path('', views.GoodsView.as_view({'get' : 'list', 'post' : 'create'}), name='goods_view'),
    path('<int:pk>/', views.GoodsView.as_view({'get' : 'retrieve'})),

    path('recommend/', views.GoodsView.as_view({'get' : 'recommend_goods'})),
    path('like/<int:goods_id>/', views.GoodsLike.as_view()),

    path('user/<int:user_id>/', views.UserGoodsView.as_view({'get' : 'list'}), name='user_goods_view'),
    path('like/<int:goods_id>/', views.GoodsLike.as_view()),
# path('', views.GoodsView.as_view(), name='goods_view'),
]
