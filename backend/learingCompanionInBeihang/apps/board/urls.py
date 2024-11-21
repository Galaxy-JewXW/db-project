from django.urls import path
from learingCompanionInBeihang.apps.board import views

urlpatterns = [
    path('get_home_view', views.GetHomeView.as_view()),
]
