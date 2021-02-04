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

    def test_create_ingredient(self):
        url = reverse('ingredient-list')
        payload = {
            "name": "new",
            "cost": 10.0
        }

        response = self.client.post(url, payload, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["chef"], self.chef.id)

    def test_create_ingredient_list_as_anon(self):
        url = reverse('ingredient-list')
        payload = {}

        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, 403)

    def test_get_ingredient_detail(self):
        url = reverse('ingredient-detail', kwargs={'pk':1})

        response = self.client.get(url, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["chef"], self.chef.id)

    def test_get_ingredient_as_anon(self):
        url = reverse('ingredient-detail', kwargs={'pk':1})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["chef"], self.chef.id)

    def test_put_ingredient_detail(self):
        url = reverse('ingredient-detail', kwargs={'pk':1})

        response = self.client.put(url, data={"name":"NEW"}, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "NEW")

    def test_put_ingredient_as_anon(self):
        url = reverse('ingredient-detail', kwargs={'pk':1})

        response = self.client.put(url, data={"name":"NEW"})

        self.assertEqual(response.status_code, 403)

    def test_put_ingredient_detail_of_another_chef(self):
        chef = Chef.objects.create(username="chef2", password="chef")
        token = f"Bearer {str(RefreshToken.for_user(chef).access_token)}"

        url = reverse('ingredient-detail', kwargs={'pk':1})

        response = self.client.put(url, data={"name":"NEW"}, HTTP_AUTHORIZATION=token)

        self.assertEqual(response.status_code, 403)

    def test_patch_ingredient_detail(self):
        url = reverse('ingredient-detail', kwargs={'pk':1})

        response = self.client.patch(url, data={"name":"NEW"}, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "NEW")

    def test_patch_ingredient_as_anon(self):
        url = reverse('ingredient-detail', kwargs={'pk':1})

        response = self.client.patch(url, data={"name":"NEW"})

        self.assertEqual(response.status_code, 403)

    def test_patch_ingredient_detail_of_another_chef(self):
        chef = Chef.objects.create(username="chef2", password="chef")
        token = f"Bearer {str(RefreshToken.for_user(chef).access_token)}"

        url = reverse('ingredient-detail', kwargs={'pk':1})

        response = self.client.patch(url, data={"name":"NEW"}, HTTP_AUTHORIZATION=token)

        self.assertEqual(response.status_code, 403)

    def test_delete_ingredient_detail(self):
        url = reverse('ingredient-detail', kwargs={'pk':1})

        response = self.client.delete(url, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 204)

    def test_delete_ingredient_as_anon(self):
        url = reverse('ingredient-detail', kwargs={'pk':1})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 403)

    def test_delete_ingredient_detail_of_another_chef(self):
        chef = Chef.objects.create(username="chef2", password="chef")
        token = f"Bearer {str(RefreshToken.for_user(chef).access_token)}"

        url = reverse('ingredient-detail', kwargs={'pk':1})

        response = self.client.delete(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(response.status_code, 403)

    def test_ingredient_list_ordering_desc(self):
        url = reverse('ingredient-list')

        response = self.client.get(url+"?ord=DESC")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 25)
        self.assertEqual(response.data["results"][0]["id"], 10)
        self.assertEqual(response.data["results"][0]["name"], "ingredient 9")

    
    def test_ingredient_list_with_invalid_filter(self):
        url = reverse('ingredient-list')

        response = self.client.get(url+"?filter=BAD")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 25)
        self.assertEqual(response.data["results"][0]["id"], 1)
        self.assertEqual(response.data["results"][0]["name"], "ingredient 0")


    def test_ingredient_search(self):
        url = reverse('ingredient-search')

        response = self.client.get(url+"?q=0")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 3)
        self.assertEqual(response.data["results"][0]["id"], 1)
        self.assertEqual(response.data["results"][0]["name"], "ingredient 0")