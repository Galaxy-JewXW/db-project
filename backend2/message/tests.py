from django.conf import settings
import os, django, json

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          '/Users/zhengguangyi/Desktop/数据库/大作业/db_project/backend/learingCompanionInBeihang/settings.py')
    django.setup()
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from message.models import Message
from users.models import User
from utils.views import encode_password, decode_jwt


class MessageViewTests(TestCase):
    def setUp(self):
        # 创建测试用户
        user1=User(id=1, student_id='20373793', name='cyy', password_digest=encode_password('123456'), user_role=2)
        user1.save()
        user2 =User(id=2, student_id='20373743', name='ccy', password_digest=encode_password('123456'), user_role=2)
        user2.save()
        self.sender = User.objects.get(id=1)
        self.receiver = User.objects.get(id=2)
        # 创建测试消息
        self.message1 = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Hello Receiver!',
            is_read=False
        )
        self.message2 = Message.objects.create(
            sender=self.receiver,
            receiver=self.sender,
            content='Hello Sender!',
            is_read=False
        )
        self.message3 = Message.objects.create(
            sender=self.receiver,
            receiver=self.sender,
            content='Hello Sender2!',
            is_read=False
        )
        # 初始化API客户端
        self.client = APIClient()

    def test_get_all_messages(self):
        # 测试获取未读消息
        url = '/message/get_messages'
        data = {
            "user_id": "1",
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        print(response.data['messages'])
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['message'], 'success')
        self.assertEqual(len(response.data['messages']), 2)
        self.assertEqual(response.data['messages'][0]['content'], 'Hello Sender2!')

    def test_mark_message_as_read(self):
        # 测试标记消息为已读
        url = '/message/read_message'
        data = {
            "user_id": "2",
            "message_id": "1"
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.message1.refresh_from_db()
        self.assertTrue(self.message1.is_read)

    def test_send_message(self):
        # 测试发送消息
        url = '/message/send_message'
        data = {
            'sender_id': self.sender.id,
            'receiver_id': self.receiver.id,
            'content': 'New message content'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('message_id', response.data)
        new_message = Message.objects.get(id=response.data['message_id'])
        self.assertEqual(new_message.content, 'New message content')
        self.assertFalse(new_message.is_read)

    def test_send_system_message(self):
        # 测试发送系统消息
        url = '/message/send_sys_message'
        data = {
            'receiver_id': self.receiver.id,
            'content': 'System message content'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('message_id', response.data)
        new_message = Message.objects.get(id=response.data['message_id'])
        self.assertEqual(new_message.content, 'System message content')
        self.assertIsNone(new_message.sender)
        self.assertFalse(new_message.is_read)

