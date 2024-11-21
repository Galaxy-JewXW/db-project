from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),           # 管理后台
    path('api/', include('myapp2.urls')),   # 引入应用的路由
]