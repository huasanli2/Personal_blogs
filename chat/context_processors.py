from .models import Message


def unread_message_count(request):
    if not request.user.is_authenticated:
        return {}
    try:
        count = Message.objects.filter(is_read=False).exclude(sender=request.user).count()
    except Exception:
        count = 0
    return {'unread_message_count': count}
