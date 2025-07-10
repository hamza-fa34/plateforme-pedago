from django.urls import path
from . import views
from .views import toggle_favorite, notifications_list

urlpatterns = [
    path('studenthome/', views.studentHome, name='studenthome'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('toggle_favorite/', toggle_favorite, name='toggle_favorite'),
    path('notifications/', notifications_list, name='notifications_list'),
]