# myapp/urls.py

from django.urls import path
from .views import AuthView

urlpatterns = [
    path('auth/', AuthView.as_view(), name='auth'),  # 合并后的登录和注册接口
]