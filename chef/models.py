from django.db import models
from django.contrib.auth.models import User


class Chef(User):
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-id']
    