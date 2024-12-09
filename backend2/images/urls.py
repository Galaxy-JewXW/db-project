# urls.py

from django.urls import path
from .views import UploadAvatarView, UploadImageView

urlpatterns = [
    path('upload-avatar/', UploadAvatarView.as_view(), name='upload_avatar'),
    path('upload-image/', UploadImageView.as_view(), name='upload_image'),
]
