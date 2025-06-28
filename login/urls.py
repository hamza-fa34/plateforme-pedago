from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),  # Page de connexion
    path('signup/', views.signup, name='signup'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
]