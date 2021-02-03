from django.urls import path
from .views import DishListView, DishDetailView


urlpatterns = [
    path("", DishListView.as_view(), name="dish-list"),
    path("<int:pk>", DishDetailView.as_view(), name="dish-detail"),
]
