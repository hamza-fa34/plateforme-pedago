from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('login_view/', views.login_view, name='login_view'),
    path('no_access/', lambda request: render(request, 'no_access.html'), name='no_access'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
]