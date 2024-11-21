from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    urls = models.URLField(max_length=200, blank=True, null=True)  # 新增的 urls 属性

    def __str__(self):
        return self.user.username
