from django.urls import path
from .models import Meal
from .views import MealListView, MealDetailView


urlpatterns = [
    path('', MealListView.as_view(), name='meal-list'),
    path('<int:pk>', MealDetailView.as_view(), name='meal-detail'),
]
