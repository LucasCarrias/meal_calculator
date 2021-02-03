from django.db import models
from chef.models import Chef
from category.models import Category

class Meal(models.Model):
    name = models.CharField(max_length=100)
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE, related_name='chef')
    category = models.ManyToManyField(Category, blank=True, related_name='categories')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']