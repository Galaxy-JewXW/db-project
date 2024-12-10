from datetime import timedelta

from django.db import models
from users.models import User
from questions.models import Question


# Exam 模型
class Exam(models.Model):

    SUBJECT_CHOICES = [
        ("工科数学分析（上）", "工科数学分析（上）"),
        ("工科数学分析（下）", "工科数学分析（下）"),
        ("工科高等代数", "工科高等代数"),
        ("离散数学（信息类）", "离散数学（信息类）"),
        ("基础物理学A", "基础物理学A"),
    ]

    id = models.AutoField(primary_key=True)  # 主键
    title = models.CharField(max_length=255)  # 考试标题
    subject = models.CharField(max_length=100, choices=SUBJECT_CHOICES, default="工科数学分析（上）")  # 所属科目，限制为可选科目
    description = models.TextField(blank=True, null=True)  # 考试描述
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    start_time = models.DateTimeField()  # 考试开始时间
    duration = models.IntegerField(null=False, default=60)  # 考试持续时间（分钟）
    end_time = models.DateTimeField(null=True, blank=True)  # 考试结束时间
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_exams")  # 创建者（老师）
    is_published = models.BooleanField(default=False)
    is_checked = models.BooleanField(default=False)

    students = models.ManyToManyField(User, related_name="enrolled_exams", blank=True)  # 报名考试的学生
    questions = models.ManyToManyField(Question, related_name="exams")  # 考试中的题目集合

    def __str__(self):
        return self.title

    def calculate_end_time(self):
        """
        如果没有显式设置持续时间，则通过 start_time 和 end_time 动态计算
        """
        if self.start_time and self.duration:
            self.end_time = self.start_time + timedelta(minutes=self.duration)


# Exam 做题记录
class ExamRecord(models.Model):
    id = models.AutoField(primary_key=True)  # 主键
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="records")  # 所属考试
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="exam_records")  # 题目
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exam_records")  # 学生
    submitted_answer = models.TextField(blank=True, null=True)  # 学生提交的答案
    is_correct = models.BooleanField(null=True, blank=True)  # 是否答对（老师批改）
    is_checked = models.BooleanField(default=False)

    submitted_at = models.DateTimeField(auto_now=True)  # 提交时间

    class Meta:
        unique_together = ('exam', 'question', 'student')  # 确保每个学生在每次考试的每道题只有一条记录

    def __str__(self):
        return f"Exam {self.exam.id} - Question {self.question.id} - Student {self.student.id}"

    def has_submitted(self):
        """
        判断学生是否提交了该题的答案
        """
        return self.submitted_answer is not None
