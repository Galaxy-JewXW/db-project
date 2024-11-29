from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),           # 管理后台
    path('api/myapp2/', include('myapp2.urls')),   # 引入应用的路由
    path('user/', include('users.urls')),
    path('images/', include('images.urls')),
    path('message/', include('message.urls')),
    path('questions/', include('questions.urls')),
    path('broadcast/', include('broadcast.urls')),
    path('api/board/', include('board.urls')),
]