from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('chefs/', include('chef.urls')),
    path('categories/', include('category.urls')),
    path('meals/', include('meal.urls')),
    path('ingredients/', include('ingredient.urls')),
]
