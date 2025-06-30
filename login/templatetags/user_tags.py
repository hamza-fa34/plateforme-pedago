from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def is_student(user):
    """Vérifie si l'utilisateur est un étudiant"""
    if user.is_authenticated and hasattr(user, 'userprofile'):
        return user.userprofile.user_type == 'student'
    return False

@register.filter
def is_teacher(user):
    """Vérifie si l'utilisateur est un enseignant"""
    if user.is_authenticated and hasattr(user, 'userprofile'):
        return user.userprofile.user_type == 'teacher'
    return False

@register.filter
def get_user_role_display(user):
    """Retourne le nom d'affichage du rôle de l'utilisateur"""
    if user.is_authenticated and hasattr(user, 'userprofile'):
        return user.userprofile.get_user_type_display()
    return "Utilisateur"

@register.filter
def get_user_icon(user):
    """Retourne l'icône appropriée pour le type d'utilisateur"""
    if user.is_authenticated and hasattr(user, 'userprofile'):
        if user.userprofile.user_type == 'student':
            return 'fas fa-graduation-cap'
        elif user.userprofile.user_type == 'teacher':
            return 'fas fa-chalkboard-teacher'
    return 'fas fa-user' 