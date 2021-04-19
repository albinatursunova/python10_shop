from django.contrib.auth.views import LogoutView
from django.urls import path

from account.views import (RegistrationView, SuccessRegistrationView, ActivationView, SigninView)

urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('successful_registration/', SuccessRegistrationView.as_view(), name='successful-registration'),
    path('activation/', ActivationView.as_view(), name='activation'),
    path('login/', SigninView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
