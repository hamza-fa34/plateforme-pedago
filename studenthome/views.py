# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from teacherhome.models import Resource, ResourceView
from login.models import UserProfile
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse, JsonResponse
from .models import Favorite, Notification
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

def get_recommendations_for_user(user, max_results=5):
    from teacherhome.models import Resource, ResourceView
    viewed_ids = set(ResourceView.objects.filter(user=user).values_list('resource_id', flat=True))
    favorite_ids = set(Favorite.objects.filter(user=user).values_list('resource_id', flat=True))
    interacted_ids = viewed_ids.union(favorite_ids)

    # Extraire les critères des ressources consultées/favorisées
    keywords = []
    subjects = []
    levels = []
    types = []
    titles = []
    for res in Resource.objects.filter(id__in=interacted_ids):
        if res.keywords:
            keywords.extend(res.keywords)
        if res.subject:
            subjects.append(res.subject)
        if res.level:
            levels.append(res.level)
        if res.resource_type:
            types.append(res.resource_type)
        if res.title:
            titles.append(res.title)
    keywords = set(keywords)
    subjects = set(subjects)
    levels = set(levels)
    types = set(types)
    titles = set(titles)

    # Trouver d'autres ressources publiques partageant ces critères, non encore consultées/favorisées
    candidates = Resource.objects.filter(permission=1).exclude(id__in=interacted_ids).distinct()
    def score(resource):
        score = 0
        if resource.keywords:
            score += len(set(resource.keywords) & keywords) * 3
        if resource.subject in subjects:
            score += 2
        if resource.level in levels:
            score += 2
        if resource.resource_type in types:
            score += 2
        if resource.title in titles:
            score += 1
        return score
    candidates = sorted(candidates, key=score, reverse=True)
    if candidates:
        return candidates[:max_results]
    else:
        # Si pas d'historique, recommander les trending
        seven_days_ago = timezone.now() - timedelta(days=7)
        trending_resources = Resource.objects.filter(
            views__timestamp__gte=seven_days_ago,
            permission=1
        ).annotate(
            view_count=Count('views')
        ).order_by('-view_count')[:max_results]
        return trending_resources

def create_notification(user, message):
    Notification.objects.create(user=user, message=message)

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
    recommendations = get_recommendations_for_user(request.user)
    # Notifier l'utilisateur s'il y a de nouvelles recommandations
    if recommendations:
        for reco in recommendations:
            notif_msg = f"Nouvelle recommandation personnalisée : {reco.title or reco.file.name}"
            if not Notification.objects.filter(user=request.user, message=notif_msg).exists():
                create_notification(request.user, notif_msg)

    context = {
        'profile': profile,
        'files_data': resources,
        'trending_resources': trending_resources, # Add to context
        'search_query': search_query,
        'favorite_ids': favorite_ids,
        'recommendations': recommendations,
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
    print("=== DEBUG TOGGLE FAVORITE ===")
    print(f"User: {request.user}")
    print(f"Method: {request.method}")
    print(f"POST data: {request.POST}")
    
    resource_id = request.POST.get('resource_id')
    user = request.user
    print(f"Resource ID: {resource_id}")
    print(f"User: {user}")
    
    if not resource_id:
        print("❌ ID manquant")
        return JsonResponse({'success': False, 'error': 'ID manquant.'}, status=400)
    
    try:
        resource = Resource.objects.get(id=resource_id)
        print(f"✅ Ressource trouvée: {resource.file.name}")
    except Resource.DoesNotExist:
        print(f"❌ Ressource introuvable: {resource_id}")
        return JsonResponse({'success': False, 'error': 'Ressource introuvable.'}, status=404)
    
    favorite, created = Favorite.objects.get_or_create(user=user, resource=resource)
    print(f"Favori existant: {not created}")
    
    if not created:
        favorite.delete()
        print("🗑️ Favori supprimé")
        return JsonResponse({'success': True, 'favorited': False})
    
    print("❤️ Favori créé")
    return JsonResponse({'success': True, 'favorited': True})

@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    # Marquer comme lues
    notifications.update(is_read=True)
    return render(request, 'notifications_list.html', {
        'notifications': notifications,
        'unread_count': unread_count,
    })