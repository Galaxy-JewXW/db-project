from django.urls import path
from learingCompanionInBeihang.apps.broadcast import views

urlpatterns = [
    path('publish_broadcast', views.PublishBroadcast.as_view()),
]
