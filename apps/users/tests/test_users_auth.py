from rest_framework.test import APITestCase
from django.urls import reverse
from apps.users.models import User

class UserAuthTest(APITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123",
            "role": "job_seeker"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(email="testuser@example.com").exists())

    def test_user_jwt_login(self):
        user = User.objects.create_user(
            username="testuser", email="testlogin@example.com", password="testpass123", role="job_seeker"
        )
        url = reverse('token_obtain_pair')
        data = {
            "email": "testlogin@example.com",
            "password": "testpass123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())
