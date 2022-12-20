from django.urls import path
from . import views


urlpatterns = [
    path('', views.ReviewAPIView.as_view(), name='review'),
]
