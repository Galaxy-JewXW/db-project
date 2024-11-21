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
from learingCompanionInBeihang.apps.questions.models import Question, QuestionBank, QuestionDiscussion, QuestionComment, UserQuestionRecord
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
            subject='基础物理学A',
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
                "subject": "工科高等代数",
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
                "subject": "离散数学（信息类）",
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

class ExtendedQuestionsTests(TestCase):
    def setUp(self):
        # 创建更多的测试用户
        self.user1 = User.objects.create(id=1, student_id='20373793', name='cyy', password_digest=encode_password('123456'), user_role=2)
        self.user2 = User.objects.create(id=2, student_id='20373743', name='ccy', password_digest=encode_password('123456'), user_role=2)
        self.user3 = User.objects.create(id=3, student_id='20373744', name='wxy', password_digest=encode_password('123456'), user_role=2)

        # 创建多个题目
        self.question1 = Question.objects.create(
            type='单项选择题',
            content='What is the answer to life, the universe, and everything?',
            subject='基础物理学A',
            added_at='2024-11-20',
            difficulty='中等',
            tags=["Arithmetic"],
            answer='42',
            added_by=self.user1
        )

        self.question2 = Question.objects.create(
            type='多项选择题',
            content='What is 2 + 2?',
            subject='工科高等代数',
            added_at='2024-11-21',
            difficulty='简单',
            tags=["Arithmetic"],
            answer='4',
            added_by=self.user2
        )

        self.question3 = Question.objects.create(
            type='填空题',
            content='The capital of France is ____.',
            subject='离散数学（信息类）',
            added_at='2024-11-22',
            difficulty='简单',
            tags=["Geography"],
            answer='Paris',
            added_by=self.user1
        )

        # 创建题库
        self.question_bank = QuestionBank.objects.create(
            subject='工科高等代数',
            estimated_time=60,
            creator=self.user2,
            description='A test question bank',
        )

        self.question_bank.questions.add(self.question1, self.question2)

        # 初始化 API 客户端
        self.client = APIClient()

    def test_upload_multiple_questions(self):
        # 上传多个题目
        data = {
            "user_id": self.user1.id,
            "data": {
                "type": "单项选择题",
                "content": "What is the capital of Japan?",
                "subject": "基础物理学A",
                "added_at": "2024-11-20",
                "difficulty": "简单",
                "tags": ["Geography"],
                "answer": "Tokyo"
            }
        }
        response = self.client.post('/questions/upload_question', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(Question.objects.count(), 4)  # 题库中题目数量增加

    def test_complete_question_multiple_times(self):
        # 多次提交做题记录
        data1 = {
            "user_id": self.user1.id,
            "question_id": self.question1.id,
            "is_correct": True
        }
        response1 = self.client.post('/questions/complete_question', data1, format='json')
        self.assertEqual(response1.status_code, HTTP_200_OK)

        data2 = {
            "user_id": self.user2.id,
            "question_id": self.question1.id,
            "is_correct": False
        }
        response2 = self.client.post('/questions/complete_question', data2, format='json')
        self.assertEqual(response2.status_code, HTTP_200_OK)

        # 检查题目做题记录
        records = UserQuestionRecord.objects.all()
        self.assertEqual(records.count(), 2)  # 两个不同用户的做题记录

    def test_create_questionbank_with_multiple_questions(self):
        # 创建题库并关联多个题目
        data = {
            "user_id": self.user1.id,
            "data": {
                "subject": "工科数学分析（下）",
                "estimated_time": 90,
                "description": "Test Question Bank for Science",
                "question_ids": [self.question1.id, self.question2.id, self.question3.id]
            }
        }
        response = self.client.post('/questions/create_questionbank', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(QuestionBank.objects.count(), 2)  # 新题库被创建
        self.assertEqual(QuestionBank.objects.get(id=response.data['question_bank_id']).questions.count(), 3)  # 题库中有三个题目

    def test_user_status_for_multiple_questions(self):
        # 用户对多个题目的做题状态
        data1 = {
            "user_id": self.user1.id,
            "question_id": self.question1.id,
            "is_correct": True
        }
        response1 = self.client.post('/questions/complete_question', data1, format='json')
        self.assertEqual(response1.status_code, HTTP_200_OK)

        data2 = {
            "user_id": self.user2.id,
            "question_id": self.question2.id,
            "is_correct": False
        }
        response2 = self.client.post('/questions/complete_question', data2, format='json')
        self.assertEqual(response2.status_code, HTTP_200_OK)

        # 获取某一科目的所有题目并验证用户状态
        response3 = self.client.post('/questions/get_questions_by_subject', {'user_id': self.user1.id, 'subject': '基础物理学A'}, format='json')
        self.assertEqual(response3.status_code, HTTP_200_OK)
        self.assertEqual(response3.data['questions'][0]['user_status'], '已做对')

        response4 = self.client.post('/questions/get_questions_by_subject', {'user_id': self.user2.id, 'subject': '工科高等代数'}, format='json')
        self.assertEqual(response4.status_code, HTTP_200_OK)
        self.assertEqual(response4.data['questions'][0]['user_status'], '做错')

    def test_get_all_questions_and_check_user_status(self):
        # 获取所有问题，并检查用户状态

        data1 = {
            "user_id": self.user1.id,
            "question_id": self.question1.id,
            "is_correct": True
        }
        response1 = self.client.post('/questions/complete_question', data1, format='json')

        data2 = {
            "user_id": self.user2.id,
            "question_id": self.question2.id,
            "is_correct": False
        }
        response2 = self.client.post('/questions/complete_question', data2, format='json')

        data1 = {
            "user_id": self.user1.id,
        }
        response1 = self.client.post('/questions/get_all_questions', data1, format='json')
        self.assertEqual(response1.status_code, HTTP_200_OK)
        self.assertEqual(len(response1.data['questions']), 3)  # 确认有3个问题
        print(response1.data['questions'])
        self.assertEqual(response1.data['questions'][0]['user_status'], '已做对')  # 确认用户状态

        data2 = {
            "user_id": self.user2.id,
        }
        response2 = self.client.post('/questions/get_all_questions', data2, format='json')
        self.assertEqual(response2.status_code, HTTP_200_OK)
        self.assertEqual(len(response2.data['questions']), 3)  # 确认有3个问题
        print(response2.data['questions'])
        self.assertEqual(response2.data['questions'][1]['user_status'], '做错')  # 确认用户状态
