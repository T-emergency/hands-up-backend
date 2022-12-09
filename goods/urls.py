from django.urls import path
from .views import GoodsView


goods_list = GoodsView.as_view({
    'get': 'list',
    'post': 'create'
})

goods_detail = GoodsView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns =[
    path('', goods_list),
    path('<int:pk>/', goods_detail),
]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.GoodsView.as_view(), name='goods_view'),
#     path('<int:goods_id>/like', views.GoodsLike.as_view(), name='goods_like'),
    
# ]