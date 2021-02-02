from rest_framework.test import APITestCase
from .models import Meal
from chef.models import Chef
from category.models import Category
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse


class MealAPITest(APITestCase):
    def setUp(self):
         Category.objects.create(name="test")

        self.chef = Chef.objects.create(username="chef", password="chef")
        self.token = f"Bearer {str(RefreshToken.for_user(self.chef).access_token)}"

        for i in range(30):
           Meal.objects.create(chef=self.chef, category=self.category, name=f"Meal {i}")
        
        self.admin = User.objects.create(username="admin", password="admin", is_superuser=True)
        self.admin_token = f"Bearer {str(RefreshToken.for_user(self.admin).access_token)}"

    
    def test_get_meals_list(self):
        url = reverse('meal-list')

        response = self.client.get(url)