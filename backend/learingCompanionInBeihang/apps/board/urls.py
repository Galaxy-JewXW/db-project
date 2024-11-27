from django.urls import path
from board import views

urlpatterns = [
    path('get_home_view', views.GetHomeView.as_view()),
]
