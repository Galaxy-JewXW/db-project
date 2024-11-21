from django.conf import settings
import os, django, json

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          '/Users/zhengguangyi/Desktop/数据库/大作业/db_project/backend/learingCompanionInBeihang/settings.py')
    django.setup()

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from learingCompanionInBeihang.apps.users.models import User
from learingCompanionInBeihang.apps.questions.models import Question, QuestionBank, QuestionDiscussion, QuestionComment
from learingCompanionInBeihang.apps.utils.views import encode_password, decode_jwt


class QuestionsTests(TestCase):
    def setUp(self):
        # 创建测试用户
        self.user1 = User(id=1, student_id='20373793', name='cyy', password_digest=encode_password('123456'),
                          user_role=2)
        self.user1.save()
        self.user2 = User(id=2, student_id='20373743', name='ccy', password_digest=encode_password('123456'),
                          user_role=2)
        self.user2.save()
        # 创建测试题目
        self.question = Question.objects.create(
            type='单项选择题',
            content='What is the answer to life, the universe, and everything?',
            subject='Philosophy',
            added_at='2024-11-20',
            difficulty='中等',
            tags=["Arithmetic"],
            answer='42',
            added_by=self.user1
        )

        # 创建讨论区
        self.discussion = QuestionDiscussion.objects.create(
            question=self.question,
            created_by=self.user1,
            content='这是一个讨论区。'
        )

        # 创建评论
        self.comment = QuestionComment.objects.create(
            discussion=self.discussion,
            created_by=self.user1,
            creator_avatar='https://randomuser.me/api/portraits/men/85.jpg',
            content='这道题很有趣！'
        )

        # 初始化 API 客户端
        self.client = APIClient()
        self.client.login(username='user1', password='password1')

    def test_upload_question(self):
        data = {
            "user_id": self.user1.id,
            "data": {
                "type": "单项选择题",
                "content": "What is 2+2?",
                "subject": "Math",
                "added_at": "2024-11-20",
                "difficulty": "简单",
                "tags": ["Arithmetic"],
                "answer": "4"
            }
        }
        response = self.client.post('/questions/upload_question', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('question_id', response.data)
        self.assertEqual(Question.objects.count(), 2)

    def test_complete_question(self):
        data = {
            "user_id": self.user1.id,
            "question_id": self.question.id,
            "is_correct": True
        }
        response = self.client.post('/questions/complete_question', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('record_id', response.data)

    def test_create_questionbank(self):
        data = {
            "user_id": self.user1.id,
            "data": {
                "subject": "Science",
                "estimated_time": 60,
                "description": "A test question bank",
                "question_ids": [self.question.id]
            }
        }
        response = self.client.post('/questions/create_questionbank', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('question_bank_id', response.data)
        self.assertEqual(QuestionBank.objects.count(), 1)

    def test_add_comment(self):
        data = {
            "user_id": self.user1.id,
            "question_id": self.question.id,
            "content": "这是一条新评论！"
        }
        response = self.client.post('/questions/add_comment', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('comment_id', response.data)
        self.assertEqual(QuestionComment.objects.count(), 2)

    def test_like_comment(self):
        data = {
            "user_id": self.user2.id,
            "comment_id": self.comment.id
        }
        response = self.client.post('/questions/like_comment', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue(response.data['liked'])
        self.assertEqual(self.comment.likes.count(), 1)

        # 再次点赞以取消点赞
        response = self.client.post('/questions/like_comment', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertFalse(response.data['liked'])
        self.assertEqual(self.comment.likes.count(), 0)

    def test_get_question_comments(self):
        data = {
            "user_id": self.user1.id,
            "question_id": self.question.id
        }
        response = self.client.post('/questions/get_question_comments', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data['comments']), 1)
        self.assertEqual(response.data['comments'][0]['content'], self.comment.content)
        self.assertEqual(response.data['comments'][0]['like_count'], 0)
        self.assertFalse(response.data['comments'][0]['liked_by_user'])
