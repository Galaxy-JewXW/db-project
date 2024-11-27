from django.urls import path
from users import views

urlpatterns = [
    path('user_login', views.UserLogin.as_view()),
    path('user_logout', views.UserLogout.as_view()),
    path('password_modify', views.PasswordModify.as_view()),

    path('modify_user_info', views.ModifyUserInfo.as_view()),
    path('get_user_info', views.GetUserInfo.as_view()),
]
