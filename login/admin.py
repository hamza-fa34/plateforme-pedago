from django.contrib import admin
from django.contrib.auth.models import Group
from .models import UserProfile

# Masquer la gestion des groupes dans l'admin
admin.site.unregister(Group)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'roll_number')
    list_filter = ('user_type',)
    search_fields = ('user__username', 'user__email', 'roll_number')