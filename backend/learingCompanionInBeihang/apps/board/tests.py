from django.conf import settings
import os, django, json

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          '/Users/zhengguangyi/Desktop/数据库/大作业/db_project/backend/learingCompanionInBeihang/settings.py')
    django.setup()

from django.test import TestCase
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK
from users.models import User
from questions.models import Question, UserQuestionRecord
from message.models import Message
from broadcast.models import Broadcast


class BoardViewTests(TestCase):
    def setUp(self):
        # 创建测试用户
        self.user = User.objects.create(
            id=1,
            student_id='20373793',
            name='cyy',
            password_digest='123456',
            user_role=2
        )
        self.other_user = User.objects.create(
            id=2,
            student_id='20373743',
            name='ccy',
            password_digest='123456',
            user_role=2
        )

        # 创建公告
        self.broadcast1 = Broadcast.objects.create(sender="Admin", content="First Announcement")
        self.broadcast2 = Broadcast.objects.create(sender="System", content="Second Announcement")
        self.broadcast3 = Broadcast.objects.create(sender="System", content="Third Announcement")
        self.broadcast4 = Broadcast.objects.create(sender="System", content="Fourth Announcement")

        # 创建题目
        self.question1 = Question.objects.create(
            type="单项选择题",
            content="What is 2 + 2?",
            subject="工科数学分析（上）",
            added_at="2024-11-20",
            difficulty="简单",
            tags=["Arithmetic"],
            answer="4",
            added_by=self.user
        )
        self.question2 = Question.objects.create(
            type="填空题",
            content="What is the capital of France?",
            subject="基础物理学A",
            added_at="2024-11-21",
            difficulty="中等",
            tags=["Geography"],
            answer="Paris",
            added_by=self.other_user
        )
        self.question3 = Question.objects.create(
            type="单项选择题",
            content="What is 2 + 2?",
            subject="工科数学分析（上）",
            added_at="2024-11-20",
            difficulty="简单",
            tags=["Arithmetic"],
            answer="4",
            added_by=self.user
        )
        self.question4 = Question.objects.create(
            type="填空题",
            content="What is the capital of France?",
            subject="基础物理学A",
            added_at="2024-11-21",
            difficulty="中等",
            tags=["Geography"],
            answer="Paris",
            added_by=self.other_user
        )
        self.question5 = Question.objects.create(
            type="单项选择题",
            content="What is 2 + 2?",
            subject="工科数学分析（上）",
            added_at="2024-11-20",
            difficulty="简单",
            tags=["Arithmetic"],
            answer="4",
            added_by=self.user
        )
        self.question6 = Question.objects.create(
            type="填空题",
            content="What is the capital of France?",
            subject="基础物理学A",
            added_at="2024-11-21",
            difficulty="中等",
            tags=["Geography"],
            answer="Paris",
            added_by=self.other_user
        )

        # 创建做题记录
        UserQuestionRecord.objects.create(user=self.user, question=self.question1, question_subject="工科数学分析（上）", is_correct=False)
        UserQuestionRecord.objects.create(user=self.user, question=self.question2, question_subject="基础物理学A", is_correct=True)

        # 创建消息
        self.message1 = Message.objects.create(sender=self.other_user, receiver=self.user, content="Message 1", is_read=False)
        self.message2 = Message.objects.create(sender=self.user, receiver=self.other_user, content="Message 2", is_read=False)
        self.message3 = Message.objects.create(sender=self.user, receiver=self.user, content="Message 3", is_read=False)
        self.message4 = Message.objects.create(sender=self.other_user, receiver=self.user, content="Message 4", is_read=True)
        self.message5 = Message.objects.create(sender=self.other_user, receiver=self.user, content="Message 5",
                                               is_read=True)
        # 初始化 API 客户端
        self.client = APIClient()

    def test_get_home_view(self):
        url = '/board/get_home_view'
        data = {
            "user_id": self.user.id,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)

        data = response.data['data']
        print(data)
        # 验证公告部分
        self.assertEqual(len(data['notices']), 3)  # 最多返回 3 条公告
        self.assertEqual(data['notices'][0]['content'], "Fourth Announcement")  # 最近的公告在最前

        # 验证消息部分
        self.assertEqual(len(data['messages']), 2)  # 最多返回 3 条未读消息
        self.assertEqual(data['messages'][0]['content'], "Message 3")  # 最近的未读消息在最前

        # 验证进度部分
        self.assertIn("工科数学分析（上）", data['progress'])
        self.assertEqual(data['progress']["工科数学分析（上）"]['user_question_count'], 1)
        self.assertEqual(data['progress']["工科数学分析（上）"]['total_question_count'], 3)

        self.assertIn("基础物理学A", data['progress'])
        self.assertEqual(data['progress']["基础物理学A"]['user_question_count'], 1)
        self.assertEqual(data['progress']["基础物理学A"]['total_question_count'], 3)

        # 验证推荐题目部分
        self.assertEqual(len(data['recommendedExercises']), 5)  # 总推荐题目数为 5
        self.assertTrue(any(id == self.question1.id for id in data['recommendedExercises']))
