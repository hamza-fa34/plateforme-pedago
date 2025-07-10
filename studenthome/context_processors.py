from .models import Notification

def notifications_unread_count(request):
    if request.user.is_authenticated:
        return {
            'notifications_unread': Notification.objects.filter(user=request.user, is_read=False).count()
        }
    return {'notifications_unread': 0} 