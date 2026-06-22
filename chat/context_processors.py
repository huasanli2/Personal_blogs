from .models import Message


def unread_message_count(request):
    if not request.user.is_authenticated:
        return {}
    count = Message.objects.filter(is_read=False).exclude(sender=request.user).count()
    return {'unread_message_count': count}
