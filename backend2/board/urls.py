from django.urls import path
from .views import get_notices

urlpatterns = [
    path('', get_notices, name='get_notices'),
]