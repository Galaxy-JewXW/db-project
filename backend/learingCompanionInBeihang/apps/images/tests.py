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
from learingCompanionInBeihang.apps.discussions.models import Discussion, Reply
from learingCompanionInBeihang.apps.utils.views import encode_password
from django.core.files.uploadedfile import SimpleUploadedFile


class UploadAvatarTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create(id=1, student_id="20373793", name="User1",
                                         password_digest=encode_password("password1"))

        # 初始化 API 客户端
        self.client = APIClient()

    def test_upload_avatar(self):
        # 模拟上传图片文件
        image_path = '/Users/zhengguangyi/Desktop/数据库/大作业/db_project/backend/learingCompanionInBeihang/apps/images/test_image.jpg'

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Test image not found at {image_path}")

        with open('/Users/zhengguangyi/Desktop/数据库/大作业/db_project/backend/learingCompanionInBeihang/apps/images/test_image.jpg', 'rb') as img_file:
            img = SimpleUploadedFile('test_image.jpg', img_file.read(), content_type='image/jpeg')

        data = {
            "user_id": self.user1.id,
            "img": img
        }

        response = self.client.post('/images/upload_avatar', data, format='multipart')
        print(response)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('avatar_url', response.data)
        print(response.data['avatar_url'])
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.avatar, response.data['avatar_url'])

    def test_upload_img(self):
        # 模拟上传图片文件
        image_path = '/Users/zhengguangyi/Desktop/数据库/大作业/db_project/backend/learingCompanionInBeihang/apps/images/test_image.jpg'

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Test image not found at {image_path}")

        with open('/Users/zhengguangyi/Desktop/数据库/大作业/db_project/backend/learingCompanionInBeihang/apps/images/test_image.jpg', 'rb') as img_file:
            img = SimpleUploadedFile('test_image.jpg', img_file.read(), content_type='image/jpeg')

        data = {
            "img": img
        }

        response = self.client.post('/images/upload_image', data, format='multipart')
        print(response)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('img_url', response.data)
        print(response.data['img_url'])
