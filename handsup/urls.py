from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('goods/', include('goods.urls')),
    path('board/', include('board.urls')),
    path('chat/', include('chat.urls')),
    path('review/', include('review.urls')),
    path('user/', include('user.urls')),
    # path('', include('.urls')),
]
