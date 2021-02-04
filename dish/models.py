from django.db import models
from ingredient.models import Ingredient
from chef.models import Chef

class Dish(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Ingredient)
    portions = models.IntegerField()
    cooking_time = models.DurationField()
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    @property
    def total_cost(self):
        return sum([ingredient.cost for ingredient in self.ingredients.all()])