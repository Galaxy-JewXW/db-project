from django.db import models
from learingCompanionInBeihang.apps.users.models import User


# Create your models here.
class Message(models.Model):
    id = models.AutoField(primary_key=True)  # 主键
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")  # 发件人
    sender_avatar = models.URLField(blank=True, null=True)  # 发件人头像
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")  # 收件人
    sent_at = models.DateTimeField(auto_now_add=True)  # 发送时间
    content = models.TextField()  # 消息内容
    is_read = models.BooleanField(default=False)  # 已读/未读
