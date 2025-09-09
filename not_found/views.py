from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import TemplateView

def custom_404(request, exception=None, template_name='404.html'):
    """Vue personnalisée pour les erreurs 404"""
    context = {
        'error_code': 404,
        'error_message': 'Page non trouvée',
        'request_path': request.path
    }
    return render(request, template_name, context, status=404)

def custom_500(request, template_name='500.html'):
    """Vue personnalisée pour les erreurs 500"""
    context = {
        'error_code': 500,
        'error_message': 'Erreur serveur interne',
        'request_path': request.path
    }
    return render(request, template_name, context, status=500)

class MentionsLegalesView(TemplateView):
    """Vue pour afficher les mentions légales"""
    template_name = 'mentions_legales.html'