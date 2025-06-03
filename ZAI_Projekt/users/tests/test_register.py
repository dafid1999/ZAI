from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from django.urls import reverse

class UserRegisterTest(TestCase):
    def setUp(self):
        Group.objects.create(name='user')
        self.client = APIClient()

    def test_user_can_register_and_is_in_user_group(self):
        url = reverse('register')
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(User.objects.filter(username="testuser").exists())

        user = User.objects.get(username="testuser")
        self.assertTrue(user.groups.filter(name='user').exists())
