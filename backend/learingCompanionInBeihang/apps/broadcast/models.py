from django.db import models


# Create your models here.

class Broadcast(models.Model):
    id = models.AutoField(primary_key=True)  # 主键
    sender = models.CharField(max_length=255, blank=True)  # 发件人名字
    sent_at = models.DateTimeField(auto_now_add=True)  # 发送时间
    content = models.TextField()  # 消息内容

