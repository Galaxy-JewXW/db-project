from django.urls import path
from .views import login_view, register_view

urlpatterns = [
    path('login/', login_view, name='login'),         # 登录接口
    path('register/', register_view, name='register'), # 注册接口
]
