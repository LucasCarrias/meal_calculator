from django.db import models
from ingredient.models import Ingredient


class Dish(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Ingredient)
    portions = models.IntegerField()
    cooking_time = models.DurationField()
