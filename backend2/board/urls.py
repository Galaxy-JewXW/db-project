from django.urls import path
from .views import GetHomeView

urlpatterns = [
    path('', GetHomeView.as_view(), name='get_home'),  # 定义路由
]
