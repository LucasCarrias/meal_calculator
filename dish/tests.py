from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from ingredient.models import Ingredient
from .models import Dish
from chef.models import Chef
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import timedelta


PAGINATION_LIMIT = 25

class DishAPITest(APITestCase):
    def setUp(self):
        self.chef = Chef.objects.create(username="chef", password="chef")
        self.token = f"Bearer {str(RefreshToken.for_user(self.chef).access_token)}"

        for i in range(1,6):
           ingredient = Ingredient.objects.create(chef=self.chef, name=f"ingredient {i}", cost=i)
           ingredient.save()

        ingredients = Ingredient.objects.all()
        for i in range(30):
            dish = Dish.objects.create(chef=self.chef, name=f"dish {i}", portions=2, cooking_time=timedelta(minutes=i))
            dish.ingredients.set(ingredients[:3])
            dish.save()

        self.admin = User.objects.create(username="admin", password="admin", is_superuser=True)
        self.admin_token = f"Bearer {str(RefreshToken.for_user(self.admin).access_token)}"

    def test_list_dishes(self):
        url = reverse('dish-list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), PAGINATION_LIMIT)


    def test_create_dishes(self):
        url = reverse('dish-list')
        payload = {
            "name":"new",
            "cost":123,
            "portions":1,
            "cooking_time":"00:30:00",
            "ingredients": [1,2,3]
        }
        response = self.client.post(url, data=payload, HTTP_AUTHORIZATION=self.token)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "new")

    def test_create_dish_list_as_anon(self):
        url = reverse('dish-list')
        payload = {}

        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, 403)

    def test_get_dish_detail(self):
        url = reverse('dish-detail', kwargs={'pk':1})

        response = self.client.get(url, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 200)
        self.assertIn(reverse('chef-detail', kwargs={'pk': self.chef.id}), response.data["chef"])

    def test_get_dish_as_anon(self):
        url = reverse('dish-detail', kwargs={'pk':1})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(reverse('chef-detail', kwargs={'pk': self.chef.id}), response.data["chef"])

    def test_put_dish_detail(self):
        url = reverse('dish-detail', kwargs={'pk':1})
        payload = {
            "name":"NEW",
            "cost":123,
            "portions":1,
            "cooking_time":"00:30:00",
            "ingredients": [1,2,3]
        }

        response = self.client.put(url, data=payload, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "NEW")

    def test_put_dish_as_anon(self):
        url = reverse('dish-detail', kwargs={'pk':1})

        response = self.client.put(url, data={"name":"NEW"})

        self.assertEqual(response.status_code, 403)

    def test_put_dish_detail_of_another_chef(self):
        chef = Chef.objects.create(username="chef2", password="chef")
        token = f"Bearer {str(RefreshToken.for_user(chef).access_token)}"

        url = reverse('dish-detail', kwargs={'pk':1})

        response = self.client.put(url, data={"name":"NEW"}, HTTP_AUTHORIZATION=token)

        self.assertEqual(response.status_code, 403)

    def test_patch_dish_detail(self):
        url = reverse('dish-detail', kwargs={'pk':1})

        response = self.client.patch(url, data={"name":"NEW"}, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "NEW")

    def test_patch_dish_as_anon(self):
        url = reverse('dish-detail', kwargs={'pk':1})

        response = self.client.patch(url, data={"name":"NEW"})

        self.assertEqual(response.status_code, 403)

    def test_patch_dish_detail_of_another_chef(self):
        chef = Chef.objects.create(username="chef2", password="chef")
        token = f"Bearer {str(RefreshToken.for_user(chef).access_token)}"

        url = reverse('dish-detail', kwargs={'pk':1})

        response = self.client.patch(url, data={"name":"NEW"}, HTTP_AUTHORIZATION=token)

        self.assertEqual(response.status_code, 403)

    def test_delete_dish_detail(self):
        url = reverse('dish-detail', kwargs={'pk':1})

        response = self.client.delete(url, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 204)

    def test_delete_dish_as_anon(self):
        url = reverse('dish-detail', kwargs={'pk':1})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 403)

    def test_delete_dish_detail_of_another_chef(self):
        chef = Chef.objects.create(username="chef2", password="chef")
        token = f"Bearer {str(RefreshToken.for_user(chef).access_token)}"

        url = reverse('dish-detail', kwargs={'pk':1})

        response = self.client.delete(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(response.status_code, 403)


class DishCalculateTest(APITestCase):
    def setUp(self):
        self.chef = Chef.objects.create(username="chef", password="chef")

        for i in range(1,6):
           ingredient = Ingredient.objects.create(chef=self.chef, name=f"ingredient {i}", cost=i)
           ingredient.save()

        ingredients = Ingredient.objects.all()
        self.dish = Dish.objects.create(chef=self.chef, name=f"dish", portions=2, cooking_time=timedelta(minutes=i))
        self.dish.ingredients.set(ingredients[:])
        self.dish.save()

    def test_calculate_dish_cost(self):
        self.assertEqual(self.dish.total_cost, sum(range(1,6)))