from django.contrib import admin
from .models import Resource, ResourceView

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'subject', 'level', 'resource_type', 'permission')
    list_filter = ('subject', 'level', 'resource_type', 'permission', 'owner')
    search_fields = ('title', 'subject', 'owner__username')

@admin.register(ResourceView)
class ResourceViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'resource', 'timestamp')
    list_filter = ('user', 'resource')
    search_fields = ('user__username', 'resource__title')
