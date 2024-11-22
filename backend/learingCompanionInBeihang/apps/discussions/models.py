from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from learingCompanionInBeihang.apps.message.models import Message
from learingCompanionInBeihang.apps.users.models import User


class Discussion(models.Model):
    SUBJECT_CHOICES = [
        ("工科数学分析（上）", "工科数学分析（上）"),
        ("工科数学分析（下）", "工科数学分析（下）"),
        ("工科高等代数", "工科高等代数"),
        ("离散数学（信息类）", "离散数学（信息类）"),
        ("基础物理学A", "基础物理学A"),
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)  # 讨论帖标题
    content = models.TextField()  # 主帖内容，支持 Markdown
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="published_discussions")  # 发帖者
    avatar = models.URLField(blank=True, null=True)  # 发帖者头像
    publish_time = models.DateTimeField(default=now)  # 发布时间
    last_updated = models.DateTimeField(auto_now=True)  # 最后更新时间
    tag = models.CharField(max_length=100, choices=SUBJECT_CHOICES, blank=True, null=True)  # 标签，学科相关
    subscribers = models.ManyToManyField(User, related_name="subscribed_discussions", blank=True)  # 订阅用户
    likes = models.ManyToManyField(User, related_name="liked_discussions", blank=True)  # 点赞的用户

    def notify_subscribers(self, update_content):
        """通知订阅者更新"""
        for subscriber in self.subscribers.all():
            Message.objects.create(
                sender=None,  # 系统消息
                receiver=subscriber,
                content=f"您关注的帖子《{self.title}》更新了: {update_content[:50]}",
                is_read=False,
            )

    def __str__(self):
        return f"{self.title} - {self.publisher.username}"


class Reply(models.Model):
    id = models.AutoField(primary_key=True)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name="replies")  # 所属主帖
    content = models.TextField()  # 回复内容
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="published_replies")  # 回复者
    avatar = models.URLField(blank=True, null=True)  # 回复者头像
    publish_time = models.DateTimeField(default=now)  # 回复时间
    last_updated = models.DateTimeField(auto_now=True)  # 最后更新时间
    likes = models.ManyToManyField(User, related_name="liked_replies", blank=True)  # 点赞的用户

    def notify_publisher(self):
        """通知发帖人有新回复"""
        Message.objects.create(
            sender=self.publisher,  # 回复者
            receiver=self.discussion.publisher,  # 收帖人是主帖发布者
            content=f"您发布的帖子《{self.discussion.title}》收到新回复: {self.content[:50]}...",
            is_read=False,
        )

    def __str__(self):
        return f"Reply by {self.publisher.username} on {self.discussion.title}"

