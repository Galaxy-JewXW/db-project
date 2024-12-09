from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),           # 管理后台
    path('api/myapp2/', include('myapp2.urls')),   # 引入应用的路由
    path('user/', include('users.urls')),
    path('api/images/', include('images.urls')),
    path('api/message/', include('message.urls')),
    path('api/discussions/', include('discussions.urls')),
    path('api/questions/', include('questions.urls')),
    path('api/broadcast/', include('broadcast.urls')),
    path('api/board/', include('board.urls')),
]