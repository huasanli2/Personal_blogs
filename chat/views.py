import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Message


EMOJI_LIST = [
    '😀','😃','😄','😁','😆','😅','🤣','😂','🙂','🥰','😍','😘','😗','😙','😚',
    '😋','😛','🤔','🤫','🤭','🤐','😐','🙄','😬','😌','😔','😴','😷','🤒',
    '🥴','🤯','🤠','🥳','😎','🤓','🧐','😤','😡','😈','💀','💩','👻','👽','🤖',
    '😺','😸','😻','🙀','😿','🙈','🙉','🙊',
    '💌','💘','💝','💖','💗','💓','💞','💕','💟','❤️','🧡','💛','💚','💙','💜',
    '🖤','🤍','🤎','💔','💤','💢','💣','💥','💦','💨',
    '👍','👎','👊','✊','🤞','✌️','🤘','🙏','💪','🔥','⭐','🌟','✨','💫','🌈',
    '☀️','🌤️','⛅','☁️','🌧️','🍎','🍊','🍋','🍉','🍇','🍓','🍒','🍑','🍔','🍕',
    '🍟','🍿','🥚','🍳','🍞','🧀','🥗','🌮','🍝','🍜','🍲','🍣','🥟','🍰','🎂',
    '🍮','🍭','🍬','🍫','🍩','🍪','☕','🍵','🍺','🍻','🥂','🍷','🍸','🍹','🧊',
    '🌸','💐','🌷','🌹','🌺','🌻','🌼','🌱','🌲','🌳','🌴','🌵','🍀','🍁','🍂',
    '🏠','🏡','🏢','🏥','🏦','🏨','🏪','🏫','🏰','💒','🗼','🗽','⛪','⛲',
    '🎆','🎇','🎑','💰','💴','💵','💶','💷','🗿','🔑','🗝️','🔒','🔓',
    '✏️','✒️','🖊️','📝','📁','📂','📅','📆','📌','📍','📎','✂️','🗑️',
    '🔨','🔧','🔩','⚙️','🧲','💉','💊',
    '🚂','🚃','🚄','🚇','🚈','🚌','🚐','🚑','🚒','🚓','🚕','🚗','🚙','🚚','🚛',
    '🛵','🏍️','🚲','🛴','✈️','🛩️','🚀','🛸','🚁',
    '⛵','🛶','🚤','🛳️','⛴️','🚢',
    '🎮','🎲','🎯','🎳','🎰','🧩',
]


@login_required
def chat_room(request):
    chat_messages = Message.objects.select_related('sender').order_by('-created_at')[:50]
    chat_messages = reversed(chat_messages)
    return render(request, 'chat/room.html', {'chat_messages': chat_messages, 'emoji_list': EMOJI_LIST})


@login_required
@require_POST
def send_message(request):
    content = request.POST.get('content', '').strip()
    if not content:
        return JsonResponse({'error': 'empty'}, status=400)

    message = Message.objects.create(
        sender=request.user,
        content=content,
        message_type='text',
    )

    broadcast_message(message)
    return JsonResponse({
        'id': message.id,
        'content': message.content,
        'time': message.created_at.strftime('%H:%M'),
    })


@login_required
@require_POST
def upload_image(request):
    image = request.FILES.get('image')
    if not image:
        return JsonResponse({'error': 'no image'}, status=400)

    message = Message.objects.create(
        sender=request.user,
        content='',
        message_type='image',
        image=image,
    )

    broadcast_message(message)
    return JsonResponse({
        'id': message.id,
        'image_url': message.image.url,
        'time': message.created_at.strftime('%H:%M'),
    })


@login_required
def load_messages(request):
    before_id = request.GET.get('before')
    messages = Message.objects.select_related('sender').order_by('-created_at')
    if before_id:
        messages = messages.filter(id__lt=before_id)
    messages = messages[:50]

    data = [{
        'id': m.id,
        'sender': m.sender.get_display_name(),
        'sender_id': m.sender.id,
        'content': m.content,
        'type': m.message_type,
        'image_url': m.image.url if m.image else None,
        'time': m.created_at.strftime('%H:%M'),
        'is_self': m.sender == request.user,
    } for m in reversed(list(messages))]

    return JsonResponse({'messages': data, 'has_more': len(messages) == 50})


@login_required
def unread_count(request):
    count = Message.objects.filter(is_read=False).exclude(sender=request.user).count()
    return JsonResponse({'count': count})


@login_required
@require_POST
def mark_read(request):
    try:
        ids = json.loads(request.body).get('ids', [])
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'error': 'invalid json'}, status=400)
    if not ids:
        return JsonResponse({'ok': True})
    Message.objects.filter(id__in=ids, is_read=False).exclude(sender=request.user).update(is_read=True)
    return JsonResponse({'ok': True})


def broadcast_message(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('chat_room', {
        'type': 'chat_message',
        'message': {
            'id': message.id,
            'sender': message.sender.get_display_name(),
            'sender_id': message.sender.id,
            'content': message.content,
            'type': message.message_type,
            'image_url': message.image.url if message.image else None,
            'time': message.created_at.strftime('%H:%M'),
        }
    })
