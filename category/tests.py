from rest_framework.test import APITestCase
from .models import Category
from chef.models import Chef
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

class CategoryAPITest(APITestCase):
    def setUp(self):
        for i in range(30):
            Category.objects.create(name=f"Category {i}")
        
        self.chef = Chef.objects.create(username="chef", password="chef")
        self.token = f"Bearer {str(RefreshToken.for_user(self.chef).access_token)}"

        self.admin = User.objects.create(username="admin", password="admin", is_superuser=True)
        self.admin_token = f"Bearer {str(RefreshToken.for_user(self.admin).access_token)}"

    def test_get_category_list_as_admin(self):
        url = reverse('category-list')

        response = self.client.get(url, HTTP_AUTHORIZATION=self.admin_token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 25)

    def test_get_category_list_as_chef(self):
        url = reverse('category-list')

        response = self.client.get(url, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 25)

    def test_get_category_list_as_anon(self):
        url = reverse('category-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 25)

    def test_create_category_as_admin(self):
        url = reverse('category-list')

        response = self.client.post(url, data={"name":"test"}, HTTP_AUTHORIZATION=self.admin_token)

        self.assertEqual(response.status_code, 201)

    def test_create_category_as_chef(self):
        url = reverse('category-list')

        response = self.client.post(url, data={"name":"test"}, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 403)

    def test_get_category_as_admin(self):
        url = reverse('category-detail', kwargs={'pk':1})

        response = self.client.get(url, HTTP_AUTHORIZATION=self.admin_token)

        self.assertEqual(response.status_code, 200)

    def test_get_category_as_chef(self):
        url = reverse('category-detail', kwargs={'pk':1})

        response = self.client.get(url, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 403)

    def test_put_category_as_admin(self):
        url = reverse('category-detail', kwargs={'pk':1})

        response = self.client.put(url, data={'name':'new'}, HTTP_AUTHORIZATION=self.admin_token)

        self.assertEqual(response.status_code, 200)

    def test_put_category_as_chef(self):
        url = reverse('category-detail', kwargs={'pk':1})

        response = self.client.put(url, data={'name':'new'}, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 403)
    
    def test_patch_category_as_admin(self):
        url = reverse('category-detail', kwargs={'pk':1})

        response = self.client.patch(url, data={'name':'new'}, HTTP_AUTHORIZATION=self.admin_token)

        self.assertEqual(response.status_code, 200)

    def test_patch_category_as_chef(self):
        url = reverse('category-detail', kwargs={'pk':1})

        response = self.client.patch(url, data={'name':'new'}, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 403)
    
    def test_delete_category_as_admin(self):
        url = reverse('category-detail', kwargs={'pk':1})

        response = self.client.delete(url, HTTP_AUTHORIZATION=self.admin_token)

        self.assertEqual(response.status_code, 204)

    def test_delete_category_as_chef(self):
        url = reverse('category-detail', kwargs={'pk':1})

        response = self.client.delete(url, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 403)

    
