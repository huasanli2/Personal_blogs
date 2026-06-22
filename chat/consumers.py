import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    room_name = 'chat_room'

    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        msg_type = data.get('type', 'text')
        content = data.get('content', '')

        if msg_type == 'mark_read':
            ids = data.get('ids', [])
            if ids:
                await self.mark_messages_read(ids)
            return

        if msg_type == 'text' and not content.strip():
            return

        message = await self.save_message(msg_type, content)

        await self.channel_layer.group_send(self.room_name, {
            'type': 'chat_message',
            'message': {
                'id': message.id,
                'sender': self.user.get_display_name(),
                'sender_id': self.user.id,
                'content': message.content,
                'type': message.message_type,
                'time': message.created_at.strftime('%H:%M'),
            }
        })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

    @database_sync_to_async
    def mark_messages_read(self, ids):
        Message.objects.filter(id__in=ids, is_read=False).exclude(sender=self.user).update(is_read=True)

    @database_sync_to_async
    def save_message(self, msg_type, content):
        return Message.objects.create(
            sender=self.user,
            content=content,
            message_type=msg_type,
        )
