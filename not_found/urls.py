from django.urls import path
from . import views

urlpatterns = [
    path('not_found/', views.custom_404, name='not_found'),
    path('mentions-legales/', views.MentionsLegalesView.as_view(), name='mentions_legales'),
]