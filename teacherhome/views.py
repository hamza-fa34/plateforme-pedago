from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import FileModelForm
from .models import Resource
from login.models import UserProfile
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.files import File as DjangoFile
from wsgiref.util import FileWrapper
from mimetypes import guess_type
from django.contrib.auth.models import User
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from urllib.parse import unquote

@login_required
def teacher_home(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        if not profile or profile.user_type != 'teacher':
            return redirect('no_access')
    except UserProfile.DoesNotExist:
        return redirect('no_access')

    search_query = request.GET.get('search', '')
    
    # Récupérer les ressources de l'enseignant connecté
    user_resources = Resource.objects.filter(owner=request.user)

    if search_query:
        user_resources = user_resources.filter(file__name__icontains=search_query)

    form = FileModelForm()

    context = {
        'profile': profile,
        'form': form,
        'filtered_files': user_resources,
        'search_query': search_query,
    }
    return render(request, 'teacherhome.html', context)

@login_required
def upload_form(request):
    if request.method == 'POST':
        form = FileModelForm(request.POST, request.FILES)
        if form.is_valid():
            resource_instance = form.save(commit=False)
            resource_instance.owner = request.user
            resource_instance.email = request.user.email
            resource_instance.save()
            return redirect('teacher_home')
    # Si ce n'est pas un POST, on redirige simplement vers la home
    return redirect('teacher_home')

def download_file(request, file_id):
    file_instance = get_object_or_404(Resource, id=file_id)
    file_path = file_instance.file.path

    # Create a file wrapper for the response
    response = HttpResponse(FileWrapper(open(file_path, 'rb')), content_type=guess_type(file_path)[0])
    
    # Set the Content-Disposition header to force download
    response['Content-Disposition'] = f'attachment; filename="{file_instance.file.name}"'
    
    return response

@login_required
def delete_file(request, file_id):
    resource_to_delete = get_object_or_404(Resource, id=file_id)
    
    # Vérifier que l'utilisateur est bien le propriétaire
    if resource_to_delete.owner == request.user:
        resource_to_delete.file.delete() # Supprime le fichier physique
        resource_to_delete.delete() # Supprime l'entrée en base de données
        
    return redirect('teacher_home')

def get_teacher_name_and_id(uploaded_by):
    try:
        teacher_profile = UserProfile.objects.get(user__username=uploaded_by)
        return teacher_profile.name, None  # teacher_id n'existe pas dans UserProfile
    except UserProfile.DoesNotExist:
        return None, None

# def notification(file_name, name, email):
#     # DÉPRÉCIÉ : Ne pas utiliser en l'état.
#     pass

def getStudents():
    students_emails = UserProfile.objects.filter(user_type='student').values_list('user__email', flat=True)
    return students_emails