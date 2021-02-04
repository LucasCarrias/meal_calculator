from rest_framework.test import APITestCase
from .models import Meal
from chef.models import Chef
from category.models import Category
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.urls import reverse
from ingredient.models import Ingredient
from dish.models import Dish
from datetime import timedelta


class MealAPITest(APITestCase):
    def setUp(self):
        category = Category.objects.create(name="test")

        self.chef = Chef.objects.create(username="chef", password="chef")
        self.token = f"Bearer {str(RefreshToken.for_user(self.chef).access_token)}"

        for i in range(1,6):
           ingredient = Ingredient.objects.create(chef=self.chef, name=f"ingredient {i}", cost=i)
           ingredient.save()

        ingredients = Ingredient.objects.all()
        for i in range(1,6):
            dish = Dish.objects.create(chef=self.chef, name=f"dish {i}", portions=2, cooking_time=timedelta(minutes=i))
            dish.ingredients.set(ingredients[:])
            dish.save()

        dishes = Dish.objects.all()
        for i in range(30):
           meal = Meal.objects.create(chef=self.chef, name=f"Meal {i}")
           meal.categories.set((category,))
           meal.dishes.set(dishes)
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
        self.assertIn(reverse('chef-detail', kwargs={'pk': self.chef.id}), response.data["chef"])

    def test_get_meal_as_anon(self):
        url = reverse('meal-detail', kwargs={'pk':1})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(reverse('chef-detail', kwargs={'pk': self.chef.id}), response.data["chef"])

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

    def test_meal_calculation(self):
        url = reverse('meal-calculate', kwargs={"pk": 1})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Meal 0")
        self.assertEqual(response.data["total_cost"], sum(range(1,6))*5)
        self.assertEqual(response.data["cooking_time"], timedelta(minutes=(sum(range(1,6)))/2))
        self.assertEqual(response.data["total_portions"], 2)

    def test_meal_list_ordering_desc(self):
        url = reverse('meal-list')

        response = self.client.get(url+"?ord=DESC")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 25)
        self.assertEqual(response.data["results"][0]["id"], 10)
        self.assertEqual(response.data["results"][0]["name"], "Meal 9")

    
    def test_meal_list_with_invalid_filter(self):
        url = reverse('meal-list')

        response = self.client.get(url+"?filter=BAD")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 25)
        self.assertEqual(response.data["results"][0]["id"], 1)
        self.assertEqual(response.data["results"][0]["name"], "Meal 0")


    def test_meal_search(self):
        url = reverse('meal-search')

        response = self.client.get(url+"?q=0")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 3)
        self.assertEqual(response.data["results"][0]["id"], 1)
        self.assertEqual(response.data["results"][0]["name"], "Meal 0")

class MealCalculateTest(APITestCase):
    def setUp(self):
        self.chef = Chef.objects.create(username="chef", password="chef")

        for i in range(1,6):
           ingredient = Ingredient.objects.create(chef=self.chef, name=f"ingredient {i}", cost=i)
           ingredient.save()

        ingredients = Ingredient.objects.all()
        for i in range(1,6):
            dish = Dish.objects.create(chef=self.chef, name=f"dish {i}", portions=2, cooking_time=timedelta(minutes=i))
            dish.ingredients.set(ingredients[:])
            dish.save()

        dishes = Dish.objects.all()
        self.meal = Meal.objects.create(chef=self.chef, name=f"Meal")
        self.meal.dishes.set(dishes)

    def test_calculate_meal_cost(self):
        self.assertEqual(self.meal.total_cost, sum(range(1,6))*5)

    def test_calculate_cooking_time(self):
        self.assertEqual(self.meal.cooking_time, timedelta(minutes=(sum(range(1,6)))/2))

    def test_calculate_total_portions(self):
        self.assertEqual(self.meal.total_portions, 2)