from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Q
from .forms import FileModelForm
from .models import Resource
from login.models import UserProfile
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from mimetypes import guess_type
from studenthome.views import create_notification

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
        # Rechercher dans le titre et le sujet de la ressource
        user_resources = user_resources.filter(
            models.Q(title__icontains=search_query) | 
            models.Q(subject__icontains=search_query)
        )

    form = FileModelForm()

    context = {
        'profile': profile,
        'form': form,
        'files_data': user_resources,
        'search_query': search_query,
    }
    return render(request, 'teacherhome.html', context)

@login_required
def upload_form(request):
    if request.method == 'POST':
        form = FileModelForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Sauvegarder le formulaire sans commit pour définir le propriétaire
                resource = form.save(commit=False)
                resource.owner = request.user
                resource.email = request.user.email
                
                # Sauvegarder la ressource (les mots-clés sont gérés dans la méthode save() du formulaire)
                resource.save()
                
                # Notifier tous les étudiants d'une nouvelle ressource publique
                if resource.permission == 1:
                    students = UserProfile.objects.filter(user_type='student').select_related('user')
                    for student in students:
                        create_notification(student.user, f"Nouvelle ressource disponible : {resource.title or resource.file.name}")
                
                # Ajouter un message de succès
                from django.contrib import messages
                messages.success(request, "La ressource a été ajoutée avec succès.")
                
                return redirect('teacher_home')
                
            except Exception as e:
                # En cas d'erreur, ajouter un message d'erreur
                from django.contrib import messages
                messages.error(request, f"Une erreur est survenue lors de l'ajout de la ressource : {str(e)}")
                return redirect('teacher_home')
    
    # Si ce n'est pas un POST ou si le formulaire n'est pas valide, on redirige simplement vers la home
    # (vous pourriez vouloir afficher les erreurs du formulaire dans une version future)
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
    from django.http import HttpResponseForbidden
    
    # Récupérer la ressource ou retourner 404
    resource_to_delete = get_object_or_404(Resource, id=file_id)
    
    # Vérifier que l'utilisateur est bien le propriétaire
    if resource_to_delete.owner != request.user:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à supprimer cette ressource.")
    
    # Supprimer le fichier physique et l'entrée en base de données
    if resource_to_delete.file:
        resource_to_delete.file.delete()
    resource_to_delete.delete()
    
    # Rediriger vers la page d'accueil avec un message de succès
    from django.contrib import messages
    messages.success(request, "La ressource a été supprimée avec succès.")
    
    return redirect('teacher_home')

@login_required
def edit_resource(request, resource_id):
    from .models import Resource
    from .forms import FileModelForm
    from login.models import UserProfile
    from django.http import HttpResponseForbidden
    
    # Récupérer la ressource ou retourner 404
    resource = get_object_or_404(Resource, id=resource_id)
    
    # Vérifier que l'utilisateur est bien le propriétaire de la ressource
    if resource.owner != request.user:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à modifier cette ressource.")
    
    if request.method == 'POST':
        form = FileModelForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            # Sauvegarder le formulaire sans commit pour gérer les mots-clés manuellement
            resource = form.save(commit=False)
            
            # Mettre à jour les mots-clés si nécessaire
            if 'keywords' in request.POST:
                keywords = request.POST.get('keywords', '')
                if keywords:
                    # Convertir la chaîne de mots-clés en liste
                    keywords_list = [k.strip() for k in keywords.split(',') if k.strip()]
                    resource.keywords = keywords_list
            
            # Sauvegarder les modifications
            resource.save()
            
            # Sauvegarder à nouveau pour les relations many-to-many si nécessaire
            form.save_m2m()
            
            return redirect('teacher_home')
    else:
        form = FileModelForm(instance=resource)
    
    # Récupérer le profil de l'utilisateur pour le template
    profile = get_object_or_404(UserProfile, user=request.user)
    
    return render(request, 'edit_resource.html', {
        'form': form, 
        'resource': resource, 
        'profile': profile
    })

def get_teacher_name_and_id(uploaded_by):
    try:
        teacher_profile = UserProfile.objects.get(user__username=uploaded_by)
        return teacher_profile.name, None  # teacher_id n'existe pas dans UserProfile
    except UserProfile.DoesNotExist:
        return None, None

def getStudents():
    students_emails = UserProfile.objects.filter(user_type='student').values_list('user__email', flat=True)
    return students_emails