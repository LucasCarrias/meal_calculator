from django.urls import path
from .views import sign_up, login



urlpatterns = [
    path('sign_up', sign_up, name='sign_up'),
    path('login', login, name='login'),
]
