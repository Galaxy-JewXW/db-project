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


class DiscussionTests(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create(id=1, student_id="20373793", name="User1",
                                         password_digest=encode_password("password1"))
        self.user2 = User.objects.create(id=2, student_id="20373794", name="User2",
                                         password_digest=encode_password("password2"))

        # Create a discussion
        self.discussion = Discussion.objects.create(
            title="Test Discussion",
            content="This is a test discussion.",
            publisher=self.user1,
            avatar="https://randomuser.me/api/portraits/women/85.jpg",
            tag="Test Tag"
        )

        # Create a reply
        self.reply = Reply.objects.create(
            discussion=self.discussion,
            content="This is a test reply.",
            publisher=self.user2,
            avatar="https://randomuser.me/api/portraits/men/45.jpg"
        )

        # Initialize API client
        self.client = APIClient()

    def test_create_discussion(self):
        data = {
            "user_id": self.user1.id,
            "title": "New Discussion",
            "content": "This is a new discussion.",
            "tag": "New Tag"
        }

        response = self.client.post('/discussions/create_discussion', data, format='json')
        print(response)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('discussion_id', response.data)
        self.assertEqual(Discussion.objects.count(), 2)

    def test_like_discussion(self):
        data = {
            "user_id": self.user2.id,
            "discussion_id": self.discussion.id
        }
        response = self.client.post('/discussions/like_discussion', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue(response.data['liked'])

        # Unlike the discussion
        response = self.client.post('/discussions/like_discussion', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertFalse(response.data['liked'])

    def test_subscribe_discussion(self):
        data = {
            "user_id": self.user2.id,
            "discussion_id": self.discussion.id
        }
        response = self.client.post('/discussions/subscribe_discussion', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue(response.data['subscribed'])

        # Unsubscribe
        response = self.client.post('/discussions/subscribe_discussion', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertFalse(response.data['subscribed'])

    def test_create_reply(self):
        data = {
            "user_id": self.user2.id,
            "discussion_id": self.discussion.id,
            "content": "This is another reply."
        }
        response = self.client.post('/discussions/create_reply', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('reply_id', response.data)
        self.assertEqual(Reply.objects.count(), 2)

    def test_edit_discussion(self):
        data = {
            "user_id": self.user1.id,
            "discussion_id": self.discussion.id,
            "content": "Updated discussion content."
        }
        response = self.client.post('/discussions/edit_discussion', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.discussion.refresh_from_db()
        self.assertEqual(self.discussion.content, "Updated discussion content.")

    def test_edit_reply(self):
        data = {
            "user_id": self.user2.id,
            "reply_id": self.reply.id,
            "content": "Updated reply content."
        }
        response = self.client.post('/discussions/edit_reply', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.reply.refresh_from_db()
        self.assertEqual(self.reply.content, "Updated reply content.")

    def test_get_all_discussions(self):
        response = self.client.post('/discussions/get_all_discussions', {}, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data['discussions']), 1)

    def test_get_discussion_replies(self):
        data = {
            "user_id": self.user1.id,
            "discussion_id": self.discussion.id
        }
        response = self.client.post('/discussions/get_discussion_replies', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data['replies']), 1)
        self.assertEqual(response.data['replies'][0]['content'], "This is a test reply.")

    def test_get_discussion_by_id(self):
        data = {
            "user_id": self.user1.id,
            "discussion_id": self.discussion.id
        }
        response = self.client.post('/discussions/get_discussion', data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['discussion']['title'], "Test Discussion")
        self.assertEqual(len(response.data['replies']), 1)

    
