from django.db import models
from chef.models import Chef
from category.models import Category
from dish.models import Dish

class Meal(models.Model):
    name = models.CharField(max_length=100)
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE, related_name='chef')
    categories = models.ManyToManyField(Category, blank=True, related_name='categories')
    dishes = models.ManyToManyField(Dish, blank=True, related_name='dishes')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']