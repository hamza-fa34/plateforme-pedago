# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from teacherhome.models import Resource, ResourceView
from login.models import UserProfile
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse, JsonResponse
from .models import Favorite
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

@login_required
def studentHome(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        if not profile or profile.user_type != 'student':
            return redirect('no_access')
    except UserProfile.DoesNotExist:
        return redirect('no_access')

    search_query = request.GET.get('search', '')

    # Start with all public resources
    resources = Resource.objects.filter(permission=1)

    if search_query:
        # Advanced search: look in filename OR in keywords
        resources = resources.filter(
            Q(file__icontains=search_query) | 
            Q(keywords__icontains=search_query)
        ).distinct()

    # --- Trending Resources Logic ---
    seven_days_ago = timezone.now() - timedelta(days=7)
    trending_resources = Resource.objects.filter(
        views__timestamp__gte=seven_days_ago,
        permission=1
    ).annotate(
        view_count=Count('views')
    ).order_by('-view_count')[:5] # Top 5 trending

    favorite_ids = list(Favorite.objects.filter(user=request.user).values_list('resource_id', flat=True))

    context = {
        'profile': profile,
        'files_data': resources,
        'trending_resources': trending_resources, # Add to context
        'search_query': search_query,
        'favorite_ids': favorite_ids,
    }
    return render(request, 'studenthome.html', context)

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.files import File as DjangoFile
from wsgiref.util import FileWrapper
from mimetypes import guess_type

@login_required
def download_file(request, file_id):
    resource = get_object_or_404(Resource, id=file_id)
    
    # Track the view/download
    ResourceView.objects.create(resource=resource, user=request.user)
    
    file_path = resource.file.path

    # Create a file wrapper for the response
    response = HttpResponse(FileWrapper(open(file_path, 'rb')), content_type=guess_type(file_path)[0])
    
    # Set the Content-Disposition header to force download
    response['Content-Disposition'] = f'attachment; filename="{resource.file.name}"'
    
    return response

@login_required
@require_POST
@csrf_exempt  # À remplacer par @csrf_protect si tu utilises le token CSRF côté JS
def toggle_favorite(request):
    resource_id = request.POST.get('resource_id')
    user = request.user
    if not resource_id:
        return JsonResponse({'success': False, 'error': 'ID manquant.'}, status=400)
    try:
        resource = Resource.objects.get(id=resource_id)
    except Resource.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Ressource introuvable.'}, status=404)
    favorite, created = Favorite.objects.get_or_create(user=user, resource=resource)
    if not created:
        favorite.delete()
        return JsonResponse({'success': True, 'favorited': False})
    return JsonResponse({'success': True, 'favorited': True})