# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from teacherhome.models import Resource, ResourceView
from login.models import UserProfile
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta

@login_required
def studentHome(request):
    try:
        profile = UserProfile.objects.get(email=request.user.email)
    except UserProfile.DoesNotExist:
        profile = None
        print('UserProfile not found for user:', request.user.email)

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

    context = {
        'profile': profile,
        'files_data': resources,
        'trending_resources': trending_resources, # Add to context
        'search_query': search_query,
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