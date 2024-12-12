from django.urls import path
from .views import GetHomeView,GetStudentExams

urlpatterns = [
    path('', GetHomeView.as_view(), name='get_home'),  # 定义路由
    path('date/', GetStudentExams.as_view(),name='date')
]
