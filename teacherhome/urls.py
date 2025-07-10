from django.urls import path
from . import views
from .views import edit_resource

urlpatterns = [
    path('teacherhome/', views.teacher_home, name='teacher_home'),
    path('upload/', views.upload_form, name='upload_form'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('edit_resource/<int:resource_id>/', edit_resource, name='edit_resource'),
]