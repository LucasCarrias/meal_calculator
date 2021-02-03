from django.db import models
from chef.models import Chef

class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)
    cost = models.FloatField(default=0)
    currency = models.CharField(max_length=10, default='BRL')
    amount_unit = models.CharField(max_length=10, default='UN')
    chef = models.ForeignKey(Chef, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']