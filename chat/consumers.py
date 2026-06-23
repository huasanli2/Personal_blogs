import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    room_name = 'chat_room'

    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
        logger.info('ws connect: user=%s', self.user.get_display_name())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        logger.info('ws disconnect: user=%s code=%s', getattr(self, 'user', '?'), close_code)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            logger.warning('ws receive: invalid JSON from user=%s', getattr(self, 'user', '?'))
            await self.send(text_data=json.dumps({'type': 'error', 'reason': 'invalid_json'}))
            return

        msg_type = data.get('type', 'text')
        content = data.get('content', '')

        if msg_type == 'ping':
            await self.send(text_data=json.dumps({'type': 'pong'}))
            return

        if msg_type == 'recall':
            message_id = data.get('message_id')
            if message_id:
                ok = await self._mark_recalled(message_id)
                if ok:
                    await self.channel_layer.group_send(self.room_name, {
                        'type': 'chat_message',
                        'message': {
                            'type': 'message_recalled',
                            'message_id': message_id,
                            'sender_id': self.user.id,
                        }
                    })
            return

        if msg_type == 'text' and not content.strip():
            return

        try:
            message = await self.save_message(msg_type, content)
        except Exception:
            logger.exception('ws receive: save_message failed for user=%s', self.user.get_display_name())
            await self.send(text_data=json.dumps({'type': 'error', 'reason': 'server_error'}))
            return

        try:
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
        except Exception:
            logger.exception('ws receive: group_send failed for user=%s', self.user.get_display_name())

    async def chat_message(self, event):
        try:
            await self.send(text_data=json.dumps(event['message']))
        except Exception:
            logger.exception('ws chat_message: send failed event=%s', event.get('message'))

    @database_sync_to_async
    def _mark_recalled(self, message_id):
        updated = Message.objects.filter(id=message_id, sender=self.user).update(is_recalled=True)
        return updated > 0

    @database_sync_to_async
    def save_message(self, msg_type, content):
        return Message.objects.create(
            sender=self.user,
            content=content,
            message_type=msg_type,
        )
