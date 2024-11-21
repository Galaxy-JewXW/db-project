from django.urls import path
from learingCompanionInBeihang.apps.images import views

urlpatterns = [
    path('upload/', views.UploadImage.as_view()),
]
