from rest_framework.test import APITestCase
from .models import Ingredient
from chef.models import Chef
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse


PAGINATION_LIMIT = 25

class IngredientAPITest(APITestCase):
    def setUp(self):
        self.chef = Chef.objects.create(username="chef", password="chef")
        self.token = f"Bearer {str(RefreshToken.for_user(self.chef).access_token)}"

        for i in range(30):
           ingredient = Ingredient.objects.create(chef=self.chef, name=f"ingredient {i}")
           ingredient.save()

        self.admin = User.objects.create(username="admin", password="admin", is_superuser=True)
        self.admin_token = f"Bearer {str(RefreshToken.for_user(self.admin).access_token)}"

    def test_get_ingredient_list(self):
        url = reverse('ingredient-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), PAGINATION_LIMIT)

    