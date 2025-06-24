from django.urls import path
from . import views

urlpatterns = [
    path('teacherhome/', views.teacher_home, name='teacher_home'),
    path('upload/', views.upload_form, name='upload_form'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
]