from django.test import TestCase
import json
import os
import django
from django.conf import settings

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          '/Users/zhengguangyi/Desktop/数据库/大作业/db_project/backend/learingCompanionInBeihang/settings.py')
    django.setup()

from rest_framework.test import APITestCase

from learingCompanionInBeihang.apps.users.models import User
from learingCompanionInBeihang.apps.utils.views import encode_password, decode_jwt


# Create your tests here.

class UserAPITestCase(APITestCase):
    def setUp(self):
        User.objects.bulk_create([
            User(id=1, student_id='20373743', name='ccy', password_digest=encode_password('123456'), user_role=2,
                 ),
            User(id=2, student_id='20373043', name='lsz', password_digest=encode_password('123456'), user_role=0,
                 ),
            User(id=3, student_id='20373044', name='xyy', password_digest=encode_password('123456'), user_role=1,
                 ),
            User(id=4, student_id='20373045', name='xxx', password_digest=encode_password('123456'), user_role=1,
                 ),
            User(id=5, student_id='20373046', name='yyy', password_digest=encode_password('123456'), user_role=1,
                 ),
            User(id=6, student_id='20373001', name='1', password_digest=encode_password('123456'), user_role=0,
                 ),
            User(id=7, student_id='20373002', name='2', password_digest=encode_password('123456'), user_role=0,
                 ),
            User(id=8, student_id='20373003', name='3', password_digest=encode_password('123456'), user_role=0,
                 ),
        ])

    def test_login_admin(self, password="123456"):
        url = '/user/user_login'
        data = {
            "student_id": "20373743",
            "password": password
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        print(response.data)
        print(response.data['data']['jwt'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'login success!')
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(response.data['data']['role'], 2)
        self.assertTrue(decode_jwt(response.data['data']['jwt'])[0])
        return response.data['data']['jwt']

    def test_login_student2(self):
        url = '/user/user_login'
        data = {
            "student_id": "20373043",
            "password": "123456"
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'login success!')
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(response.data['data']['role'], 0)
        self.assertTrue(decode_jwt(response.data['data']['jwt'])[0])
        return response.data['data']['jwt']

    def _student_login_6(self):
        response = self.client.post('/user/user_login', {'student_id': '20373001', 'password': '123456'})
        return response.data['data']['jwt']

    def _student_login_7(self):
        response = self.client.post('/user/user_login', {'student_id': '20373002', 'password': '123456'})
        return response.data['data']['jwt']

    def test_password_modify(self):
        # 1
        jwt_token = self.test_login_admin("123456")
        url = '/user/password_modify'
        data = {
            "jwt": jwt_token,
            "password_old": "123456",
            "password_new": "111111"
        }
        print(jwt_token + "here test")
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'modify password successfully!')
        self.assertEqual(response.data['code'], 0)
        # login
        url2 = '/user/user_login'
        data2 = {
            "student_id": "20373743",
            "password": "111111"
        }
        response = self.client.post(url2, data=json.dumps(data2), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'login success!')
        self.assertEqual(response.data['code'], 0)
        # 3
        url = '/user/password_modify'
        data = {
            "jwt": jwt_token,
            "password_old": "111111",
            "password_new": "123456"
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'modify password successfully!')
        self.assertEqual(response.data['code'], 0)
