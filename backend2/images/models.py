# models.py

from django.db import models

class UserAvatar(models.Model):
    title = models.CharField(max_length=255)  # 文件标题（名称）
    avatar = models.FileField(upload_to='avatars/')  # 保存头像文件到本地
    created_at = models.DateTimeField(auto_now_add=True)  # 记录创建时间

    def __str__(self):
        return self.title
