from django.db import models
from learingCompanionInBeihang.apps.users.models import User


class Question(models.Model):
    TYPE_CHOICES = [
        ("单项选择题", "单项选择题"),
        ("多项选择题", "多项选择题"),
        ("填空题", "填空题"),
        ("问答题", "问答题"),
    ]

    DIFFICULTY_CHOICES = [
        ("简单", "简单"),
        ("中等", "中等"),
        ("困难", "困难"),
    ]

    id = models.AutoField(primary_key=True)  # 题目ID
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)  # 题目类型
    content = models.TextField()  # 题目内容（Markdown 格式）
    subject = models.CharField(max_length=100)  # 所属学科
    added_at = models.DateField()  # 添加时间
    source = models.CharField(max_length=100, blank=True, null=True)  # 题目来源
    tags = models.JSONField()  # JSON 格式
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)  # 难度
    answer = models.TextField(blank=True, null=True)  # 答案内容
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="added_questions")  # 创建者
    question_banks = models.ManyToManyField('QuestionBank', related_name="questions")  # 题库关系

    def __str__(self):
        return f"{self.type} - {self.subject} - {self.id}"


# 用户与题目之间的做题记录
class UserQuestionRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="question_records")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="user_records")
    is_correct = models.BooleanField()  # 是否做对
    attempted_at = models.DateTimeField(auto_now_add=True)  # 做题时间

    class Meta:
        unique_together = ('user', 'question')  # 确保同一个用户对每个题目只有一条记录
        verbose_name = "用户做题记录"
        verbose_name_plural = "用户做题记录"

    def __str__(self):
        return f"User {self.user.id} - Question {self.question.id} - {'Correct' if self.is_correct else 'Incorrect'}"


class QuestionBank(models.Model):
    id = models.AutoField(primary_key=True)  # 主键
    subject = models.CharField(max_length=100)  # 所属科目
    estimated_time = models.IntegerField()  # 预计用时（分钟）
    created_at = models.DateTimeField(auto_now_add=True)  # 创建日期
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_question_banks")  # 创建者
    description = models.TextField(blank=True, null=True)  # 题库描述
    question_count = models.IntegerField(default=0)  # 题目数量（可定期更新）

    def __str__(self):
        return f"{self.subject} - {self.id} - {self.question_count} questions"
