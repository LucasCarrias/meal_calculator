from rest_framework.test import APITestCase, force_authenticate
from .models import Chef
from django.contrib.auth.models import User
from django.urls import reverse


class ChefAuthenticationTest(APITestCase):
    def setUp(self):
        chef = Chef(username="test_chef", email="chef@chef.com")
        chef.set_password("12334678")
        chef.save()

    def test_sing_up(self):
        payload = {
            "username": "test",
            "email": "test@test.com",
            "password": "12345678"
        }
        url = reverse('sign_up')
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, 201)

    def test_invalid_sign_up(self):
        payload = {
            "username": "test",
            "email": "test",
            "password": "12345678"
        }
        url = reverse('sign_up')
        response = self.client.post(url, payload)

    def test_duplicated_chef_sign_up(self):
        payload = {
            "username": "test_chef",
            "email": "chef@chef.com",
            "password": "12345678"
        }
        url = reverse('sign_up')
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, 403)

    def test_login_and_generate_valid_token(self):
        payload = {
            "username": "test_chef",
            "password": "12334678"
        }

        url = reverse('login')
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], payload['username'])
        self.assertIsNotNone(response.data.get('token'))

        url = reverse('verify')
        response = self.client.post(url, {"token": response.data.get('token')})

        self.assertEqual(response.status_code, 200)

    def test_invalid_login_payload(self):
        payload = {
            "username": "test_chef"
        }

        url = reverse('login')
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, 400)

    def test_invalid_login_credentails(self):
        payload = {
            "username": "test_chef",
            "password": "bad_pass"
        }

        url = reverse('login')
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, 401)


