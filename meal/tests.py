from rest_framework.test import APITestCase
from .models import Meal
from chef.models import Chef
from category.models import Category
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.urls import reverse


class MealAPITest(APITestCase):
    def setUp(self):
        category = Category.objects.create(name="test")

        self.chef = Chef.objects.create(username="chef", password="chef")
        self.token = f"Bearer {str(RefreshToken.for_user(self.chef).access_token)}"

        for i in range(30):
           meal = Meal.objects.create(chef=self.chef, name=f"Meal {i}")
           meal.category.set((category,))
           meal.save()
        
        self.admin = User.objects.create(username="admin", password="admin", is_superuser=True)
        self.admin_token = f"Bearer {str(RefreshToken.for_user(self.admin).access_token)}"

    
    def test_get_meals_list(self):
        url = reverse('meal-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 25)

    def test_create_meal(self):
        url = reverse('meal-list')

        response = self.client.post(url, data={"name": "new"}, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["chef"], self.chef.id)
        

    def test_create_meal_as_anon(self):
        url = reverse('meal-list')

        response = self.client.post(url, data={"name": "new"})

        self.assertEqual(response.status_code, 403)

    def test_get_meal_detail(self):
        url = reverse('meal-detail', kwargs={'pk':1})

        response = self.client.get(url, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["chef"], self.chef.id)

    def test_get_meal_as_anon(self):
        url = reverse('meal-detail', kwargs={'pk':1})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["chef"], self.chef.id)

    def test_put_meal_detail(self):
        url = reverse('meal-detail', kwargs={'pk':1})

        response = self.client.put(url, data={"name":"NEW"}, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "NEW")

    def test_put_meal_as_anon(self):
        url = reverse('meal-detail', kwargs={'pk':1})

        response = self.client.put(url, data={"name":"NEW"})

        self.assertEqual(response.status_code, 403)

    def test_put_meal_detail_of_another_chef(self):
        chef = Chef.objects.create(username="chef2", password="chef")
        token = f"Bearer {str(RefreshToken.for_user(chef).access_token)}"

        url = reverse('meal-detail', kwargs={'pk':1})

        response = self.client.put(url, data={"name":"NEW"}, HTTP_AUTHORIZATION=token)

        self.assertEqual(response.status_code, 403)

    def test_patch_meal_detail(self):
        url = reverse('meal-detail', kwargs={'pk':1})

        response = self.client.patch(url, data={"name":"NEW"}, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "NEW")

    def test_patch_meal_as_anon(self):
        url = reverse('meal-detail', kwargs={'pk':1})

        response = self.client.patch(url, data={"name":"NEW"})

        self.assertEqual(response.status_code, 403)

    def test_patch_meal_detail_of_another_chef(self):
        chef = Chef.objects.create(username="chef2", password="chef")
        token = f"Bearer {str(RefreshToken.for_user(chef).access_token)}"

        url = reverse('meal-detail', kwargs={'pk':1})

        response = self.client.patch(url, data={"name":"NEW"}, HTTP_AUTHORIZATION=token)

        self.assertEqual(response.status_code, 403)

    def test_delete_meal_detail(self):
        url = reverse('meal-detail', kwargs={'pk':1})

        response = self.client.delete(url, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 204)

    def test_delete_meal_as_anon(self):
        url = reverse('meal-detail', kwargs={'pk':1})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 403)

    def test_delete_meal_detail_of_another_chef(self):
        chef = Chef.objects.create(username="chef2", password="chef")
        token = f"Bearer {str(RefreshToken.for_user(chef).access_token)}"

        url = reverse('meal-detail', kwargs={'pk':1})

        response = self.client.delete(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(response.status_code, 403)