from django.urls import path
from .views import sign_up, login, ChefListView, ChefDetailView
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    # Auth
    path('sign_up', sign_up, name='sign_up'),
    path('login', login, name='login'),
    path('verify', TokenVerifyView.as_view(), name='verify'),
    # Crud
    path('', ChefListView.as_view(), name='chef-list'),
    path('<int:pk>/', ChefDetailView.as_view(), name='chef-detail'),
]
