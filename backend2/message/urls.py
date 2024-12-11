from django.urls import path
from message import views

urlpatterns = [
    path('get_messages/', views.GetAllMessage.as_view()),
    path('read_message/', views.MarkMessageAsRead.as_view()),
    path('send_message/', views.SendMessage.as_view()),
    path('send_sys_message/', views.SendSystemMessage.as_view()),
    path('read_all_message/', views.MarkAllMessagesAsRead.as_view()),
    path('unread_message/', views.MarkMessageAsUnread.as_view()),
    path('get_read_messages/', views.GetAllReadMessages.as_view()),
]
