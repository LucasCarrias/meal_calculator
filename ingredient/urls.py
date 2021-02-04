from django.urls import path
from .views import IngredientListView, IngredientDetailView, IngredientSearchView

urlpatterns = [
    path('', IngredientListView.as_view(), name="ingredient-list"),
    path('<int:pk>', IngredientDetailView.as_view(), name="ingredient-detail"),
    path('search', IngredientSearchView.as_view(), name='ingredient-search'),
]
