from django.urls import path
from .models import Meal
from .views import MealListView, MealDetailView, meal_calculate


urlpatterns = [
    path('', MealListView.as_view(), name='meal-list'),
    path('<int:pk>', MealDetailView.as_view(), name='meal-detail'),
    path('<int:pk>/calculate', meal_calculate, name='meal-calculate'),
]
