from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from learingCompanionInBeihang.apps.users.models import User
from .models import Broadcast
from learingCompanionInBeihang.apps.utils.views import encode_password


class BroadcastTests(TestCase):
    def setUp(self):
        # 创建测试用户
        self.admin_user = User.objects.create(
            id=1, student_id='20373793', name='admin', password_digest=encode_password('123456'), user_role=1)
        self.regular_user = User.objects.create(
            id=2, student_id='20373743', name='regular_user', password_digest=encode_password('123456'), user_role=0)
        self.client = APIClient()

        # 创建广播
        self.broadcast1 = Broadcast.objects.create(
            sender="系统通知",
            title="公告1",
            content="这是公告1"
        )
        self.broadcast2 = Broadcast.objects.create(
            sender="系统通知",
            title="公告2",
            content="这是公告2"
        )

    # 测试发布广播
    def test_publish_broadcast(self):
        data = {
            "user_id": self.admin_user.id,
            "sender": "系统通知",
            "title": "新公告",
            "content": "这是一个新的公告内容"
        }
        response = self.client.post('/broadcast/publish_broadcast', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("broadcast_id", response.data)
        self.assertEqual(Broadcast.objects.count(), 3)  # 确保广播数增加

        # 权限不足的用户访问
        data = {
            "user_id": self.regular_user.id,
            "sender": "系统通知",
            "title": "新公告",
            "content": "这是一个新的公告内容"
        }
        response = self.client.post('/broadcast/publish_broadcast', data, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("权限不足", response.data['error'])

    # 测试编辑广播
    def test_edit_broadcast(self):
        data = {
            "user_id": self.admin_user.id,
            "broadcast_id": self.broadcast1.id,
            "title": "更新后的公告标题",
            "content": "更新后的公告内容"
        }
        response = self.client.post('/broadcast/edit_broadcast', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.broadcast1.refresh_from_db()
        self.assertEqual(self.broadcast1.title, "更新后的公告标题")
        self.assertEqual(self.broadcast1.content, "更新后的公告内容")

        # 权限不足的用户访问
        data = {
            "user_id": self.regular_user.id,
            "broadcast_id": self.broadcast1.id,
            "title": "非法修改的标题",
            "content": "非法修改的内容"
        }
        response = self.client.post('/broadcast/edit_broadcast', data, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("权限不足", response.data['error'])

    # 测试删除广播
    def test_delete_broadcast(self):
        data = {
            "user_id": self.admin_user.id,
            "broadcast_id": self.broadcast1.id
        }
        response = self.client.post('/broadcast/delete_broadcast', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(Broadcast.objects.count(), 1)  # 确保删除成功

        # 权限不足的用户访问
        data = {
            "user_id": self.regular_user.id,
            "broadcast_id": self.broadcast2.id
        }
        response = self.client.post('/broadcast/delete_broadcast', data, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("权限不足", response.data['error'])

    # 测试获取所有广播
    def test_get_all_broadcasts(self):
        data = {
            "user_id": self.admin_user.id,
        }
        response = self.client.post('/broadcast/get_all_broadcasts', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data['broadcasts']), 2)  # 确保返回了两个广播

        # 权限不足的用户尝试访问
        data = {
            "user_id": self.regular_user.id,
        }
        response = self.client.post('/broadcast/get_all_broadcasts', data, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("权限不足", response.data['error'])

    # 测试获取指定 ID 的广播
    def test_get_broadcast_by_id(self):
        data = {
            "user_id": self.admin_user.id,
            "broadcast_id": self.broadcast1.id
        }
        response = self.client.post('/broadcast/get_broadcast_by_id', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['broadcast_details']['title'], "公告1")

        # 权限不足的用户尝试访问
        data = {
            "user_id": self.regular_user.id,
            "broadcast_id": self.broadcast1.id
        }
        response = self.client.post('/broadcast/get_broadcast_by_id', data, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("权限不足", response.data['error'])

        # 获取不存在的广播
        data = {
            "user_id": self.admin_user.id,
            "broadcast_id": 9999  # 假定此广播不存在
        }
        response = self.client.post('/broadcast/get_broadcast_by_id', data, format='json')
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        self.assertIn("Broadcast not found", response.data['error'])
