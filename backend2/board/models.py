from django.db import models
class Notice(models.Model):
    title = models.CharField(max_length=200)         # 公告标题
    publisher = models.CharField(max_length=100)     # 发布者
    releaseTime = models.DateTimeField()            # 发布时间
    content = models.TextField()                     # 公告内容

    def __str__(self):
        return self.title
