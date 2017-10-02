from django.test import TestCase

from django.core.urlresolvers import reverse

from rest_framework.test import APIClient
from rest_framework import status

from .models import Comment


class CommentTestCase(TestCase):
    fixtures = ['init_comment.yaml']

    def setUp(self):
        # do something
        self.require_message = "This field is required."
        self.full_comment = {
            "email": "aaa@ku.th",
            "message": "very good website"
        }

        self.miss_email_comment = {
            "message": "very good website"
        }

        self.miss_message_comment = {
            "email": "aaa@ku.th"
        }

        self.client = APIClient()

    def test_list_data_from_database_api(self):
        """Test data from api and database must be equally"""
        response = self.client.get(
            reverse('comment-list'),
            format="json"
        )
        resp_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        db_comments = Comment.objects.all()
        comments = [None] * len(db_comments)
        i = 0
        for data in resp_data:
            comments[i] = Comment(**data)
            i += 1
        self.assertCountEqual(db_comments, comments)

    def test_data_on_list_api(self):
        """Test column that get from list api"""
        response = self.client.get(
            reverse('comment-list'),
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data[0])
        self.assertTrue('email' in response.data[0])
        self.assertTrue('message' in response.data[0])

    def test_creator_miss_email_api(self):
        """Test creator with incomplete data (email)"""
        response = self.client.post(
            reverse('comment-creator'),
            self.miss_email_comment,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('email')[0], self.require_message)

    def test_creator_miss_message_api(self):
        """Test creator with incomplete data (message)"""
        response = self.client.post(
            reverse('comment-creator'),
            self.miss_message_comment,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message')[0], self.require_message)

    def test_creator_succussful_api(self):
        """Test creator must create new comment"""
        response = self.client.post(
            reverse('comment-creator'),
            self.full_comment,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        resp_data = response.data

        db_c = Comment.objects.get(id=resp_data.get('id'))

        self.assertEqual(db_c.email, resp_data.get("email"))
        self.assertEqual(db_c.message, resp_data.get("message"))
