def unread_message_count(request):
    if not request.user.is_authenticated:
        return {}
    return {'unread_message_count': 0}
