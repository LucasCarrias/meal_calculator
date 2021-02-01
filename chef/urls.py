from django.urls import path
from .views import sign_up, login
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    path('sign_up', sign_up, name='sign_up'),
    path('login', login, name='login'),
    path('verify', TokenVerifyView.as_view(), name='verify'),
]
