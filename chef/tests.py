from rest_framework.test import APITestCase
from .models import Chef
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken


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

    def test_invalid_token(self):
        url = reverse('verify')
        response = self.client.post(url, {"token": "bad_token"})

        self.assertEqual(response.status_code, 401)


class ChefViewsTest(APITestCase):
    def setUp(self):
        for i in range(1, 30):
            chef = Chef(username=f"test_chef_{i}", email=f"chef{i}@chef.com")
            chef.set_password("12334678")
            chef.save()
        self.chef = Chef.objects.first()
        self.token = f"Bearer {str(RefreshToken.for_user(self.chef).access_token)}"



    def test_get_chefs_list(self):
        url = reverse('chef-list')

        response = self.client.get(url, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 25)

    def test_get_unauthenticated_chefs_list(self):
        url = reverse('chef-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_get_chef_details(self):
        url = reverse('chef-detail', kwargs={'pk': 1})

        response = self.client.get(url, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 200)

    def test_get_unauthenticated_chefs_detail(self):
        url = reverse('chef-detail', kwargs={'pk': 1})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_update_chef(self):
        url = reverse('chef-detail', kwargs={'pk': 1})

        response = self.client.put(url, data={
                                   "username": "CHEF", "email": "chef@chef.com"}, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], "CHEF")

    def test_update_unauthenticated_chef(self):
        url = reverse('chef-detail', kwargs={'pk': 1})

        response = self.client.put(url, data={})

        self.assertEqual(response.status_code, 401)

    def test_update_not_owned_chef(self):
        url = reverse('chef-detail', kwargs={'pk': 2})

        response = self.client.put(url, data={}, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 403)

    def test_update_rating(self):
        url = reverse('chef-detail', kwargs={'pk': 1})

        response = self.client.patch(
            url, data={'rating': 123}, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['rating'], 123)

    def test_update_chef_as_admin(self):
        admin = Chef(username=f"admin", email=f"admin@admin.com", is_superuser=True)
        admin.set_password("admin")
        admin.save()
        admin_token = f"Bearer {str(RefreshToken.for_user(admin).access_token)}"

        url = reverse('chef-detail', kwargs={'pk': 2})

        response = self.client.put(url, data={
                                   "username": "CHEF", "email": "chef@chef.com"
                                   }, HTTP_AUTHORIZATION=admin_token)

        self.assertEqual(response.status_code, 200)
