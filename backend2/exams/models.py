from django.db import models
from users.models import User
from questions.models import Question


# Exam 模型
class Exam(models.Model):
    id = models.AutoField(primary_key=True)  # 主键
    title = models.CharField(max_length=255)  # 考试标题
    description = models.TextField(blank=True, null=True)  # 考试描述
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    start_time = models.DateTimeField()  # 考试开始时间
    duration = models.IntegerField(null=True, blank=True)  # 考试持续时间（分钟）
    end_time = models.DateTimeField()  # 考试结束时间
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_exams")  # 创建者（老师）

    students = models.ManyToManyField(User, related_name="enrolled_exams", blank=True)  # 报名考试的学生
    questions = models.ManyToManyField(Question, related_name="exams")  # 考试中的题目集合

    def __str__(self):
        return self.title

    def calculate_duration(self):
        """
        如果没有显式设置持续时间，则通过 start_time 和 end_time 动态计算
        """
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            return delta.total_seconds() // 60  # 持续时间以分钟为单位
        return None


# Exam 做题记录
class ExamRecord(models.Model):
    id = models.AutoField(primary_key=True)  # 主键
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="records")  # 所属考试
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="exam_records")  # 题目
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exam_records")  # 学生
    submitted_answer = models.TextField(blank=True, null=True)  # 学生提交的答案
    is_correct = models.BooleanField(null=True, blank=True)  # 是否答对（老师批改）

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
