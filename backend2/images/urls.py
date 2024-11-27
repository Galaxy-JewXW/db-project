from django.urls import path
from images import views

urlpatterns = [
    path('upload/', views.UploadImage.as_view()),
]
