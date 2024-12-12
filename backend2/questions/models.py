from django.db import models
from users.models import User


class QuestionBank(models.Model):
    SUBJECT_CHOICES = [
        ("工科数学分析（上）", "工科数学分析（上）"),
        ("工科数学分析（下）", "工科数学分析（下）"),
        ("工科高等代数", "工科高等代数"),
        ("离散数学（信息类）", "离散数学（信息类）"),
        ("基础物理学A", "基础物理学A"),
    ]

    id = models.AutoField(primary_key=True)  # 主键
    name = models.CharField(max_length=100, default="")
    subject = models.CharField(max_length=100, choices=SUBJECT_CHOICES)  # 所属科目，限制为可选科目
    estimated_time = models.IntegerField()  # 预计用时（分钟）
    created_at = models.DateTimeField(auto_now_add=True)  # 创建日期
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_question_banks")  # 创建者
    description = models.TextField(blank=True, null=True)  # 题库描述
    question_count = models.IntegerField(default=0)  # 题目数量（可定期更新）

    def __str__(self):
        return f"{self.subject} - {self.id} - {self.question_count} questions"


class Question(models.Model):
    TYPE_CHOICES = [
        ("单项选择题", "单项选择题"),
        ("多项选择题", "多项选择题"),
        ("判断题", "判断题"),
        ("填空题", "填空题"),
        ("解答题", "解答题"),
    ]

    DIFFICULTY_CHOICES = [
        ("简单", "简单"),
        ("中等", "中等"),
        ("困难", "困难"),
    ]

    SUBJECT_CHOICES = [
        ("工科数学分析（上）", "工科数学分析（上）"),
        ("工科数学分析（下）", "工科数学分析（下）"),
        ("工科高等代数", "工科高等代数"),
        ("离散数学（信息类）", "离散数学（信息类）"),
        ("基础物理学A", "基础物理学A"),
    ]

    id = models.AutoField(primary_key=True)  # 题目ID
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)  # 题目类型
    content = models.TextField()  # 题目内容（Markdown 格式）
    subject = models.CharField(max_length=100, choices=SUBJECT_CHOICES)  # 所属科目，限制为可选科目
    added_at = models.DateField()  # 添加时间
    source = models.CharField(max_length=100, blank=True, null=True)  # 题目来源
    tags = models.JSONField()  # JSON 格式

    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)  # 难度
    answer = models.TextField(blank=True, null=True)  # 答案内容
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="added_questions")  # 创建者
    question_banks = models.ManyToManyField(QuestionBank, related_name="questions")  # 题库关系
    option_count = models.IntegerField(default=0)  # 选项数量，默认 0

    def is_single_choice(self):
        return self.type == "单项选择题"

    def is_multiple_choice(self):
        return self.type == "多项选择题"

    def is_true_false(self):
        return self.type == "判断题"

    def get_user_status(self, user):
        """
        获取用户对该题目的做题状态：
        - 未做过
        - 已做对
        - 做错
        """
        try:
            record = self.user_records.get(user=user)
            if record.is_correct is None:
                return "未做过"
            return "已做对" if record.is_correct else "做错"
        except UserQuestionRecord.DoesNotExist:
            return "未做过"

    def __str__(self):
        return f"{self.type} - {self.subject} - {self.id}"

    def save(self, *args, **kwargs):
        """
        根据题目类型设置默认的选项数量。
        """
        if self.type in ["单项选择题", "多项选择题"] and self.option_count == 0:
            self.option_count = 4  # 默认设置为 4 个选项
        elif self.type not in ["单项选择题", "多项选择题"]:
            self.option_count = 0  # 其他类型默认设置为 0
        super().save(*args, **kwargs)


# 用户与题目之间的做题记录
class UserQuestionRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="question_records")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="user_records")
    question_subject = models.CharField(max_length=100, choices=Question.SUBJECT_CHOICES,
                                        default="工科数学分析（上）")  # 题目科目
    is_correct = models.BooleanField(null=True, blank=True)  # 是否做对
    attempted_at = models.DateTimeField(auto_now_add=True)  # 做题时间

    class Meta:
        unique_together = ('user', 'question')  # 确保同一个用户对每个题目只有一条记录
        verbose_name = "用户做题记录"
        verbose_name_plural = "用户做题记录"

    def __str__(self):
        return f"User {self.user.id} - Question {self.question.id} - {'Correct' if self.is_correct else 'Incorrect'}"


class QuestionDiscussion(models.Model):
    id = models.AutoField(primary_key=True)  # 主键
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name="discussion")  # 关联的题目
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_discussions")  # 发布者
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    content = models.TextField()  # 讨论内容

    def __str__(self):
        return f"QuestionDiscussion for Question {self.question.id} by {self.created_by.name}"


# 评论
class QuestionComment(models.Model):
    id = models.AutoField(primary_key=True)  # 主键
    discussion = models.ForeignKey(QuestionDiscussion, on_delete=models.CASCADE, related_name="comments")  # 所属讨论
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_comments")  # 发布者
    creator_avatar = models.URLField(blank=True, null=True)  # 发件人头像
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    content = models.TextField()  # 评论内容
    likes = models.ManyToManyField(User, related_name="liked_comments", blank=True)  # 点赞的用户

    def like_count(self):
        return self.likes.count()

    def __str__(self):
        return f"QuestionComment by {self.created_by.name} on QuestionDiscussion {self.discussion.id}"
