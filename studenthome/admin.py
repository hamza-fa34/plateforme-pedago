from django.contrib import admin
from .models import Favorite, Notification

# Register your models here.
admin.site.register(Favorite)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')
