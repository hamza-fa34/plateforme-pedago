from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Page de connexion
    path('signup/', views.signup, name='signup'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
]