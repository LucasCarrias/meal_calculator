from django.db import models
from chef.models import Chef
from category.models import Category
from dish.models import Dish
from datetime import timedelta

class Meal(models.Model):
    name = models.CharField(max_length=100)
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE, related_name='chef')
    categories = models.ManyToManyField(Category, blank=True, related_name='categories')
    dishes = models.ManyToManyField(Dish, blank=True, related_name='dishes')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']

    @property
    def total_cost(self):
        return sum([dish.total_cost for dish in self.dishes.all()])

    @property
    def total_portions(self):
        return sum([dish.portions for dish in self.dishes.all()])/self.dishes.count()

    @property
    def cooking_time(self):
        return sum([dish.cooking_time for dish in self.dishes.all()], timedelta(minutes=0))/2