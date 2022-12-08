from django.urls import path
<<<<<<< HEAD

urlpatterns = [

=======
from . import views


urlpatterns = [
    path('<int:goods_id>/', views.ReviewAPIView.as_view(), name='review'),
    path('<int:user_id>/', views.ReviewListAPIView.as_view(), name='review_list'),
    # path('/', FreeListView.as_view(), name='free_list_view')
>>>>>>> cc4e5634de79e8a1305114c2a2b8555190aa64c5
]
