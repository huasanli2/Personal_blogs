import json
from django.test import TestCase, TransactionTestCase
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from .models import Message


def create_test_user(username='testuser', password='testpass123'):
    from accounts.models import User
    return User.objects.create_user(username=username, password=password)


class MessageRecallTest(TestCase):
    def test_message_is_recalled_field_default(self):
        user = create_test_user()
        msg = Message.objects.create(sender=user, content='Hello', message_type='text')
        self.assertFalse(msg.is_recalled)

    def test_message_recall_sets_flag(self):
        user = create_test_user()
        msg = Message.objects.create(sender=user, content='Hello', message_type='text')
        msg.is_recalled = True
        msg.save()
        msg.refresh_from_db()
        self.assertTrue(msg.is_recalled)

    def test_only_sender_can_recall(self):
        user1 = create_test_user('user1')
        user2 = create_test_user('user2')
        msg = Message.objects.create(sender=user1, content='Hello', message_type='text')
        self.assertEqual(msg.sender, user1)
        self.assertNotEqual(msg.sender, user2)

    def test_recalled_message_shows_placeholder(self):
        user = create_test_user()
        msg = Message.objects.create(sender=user, content='Hello', message_type='text')
        msg.is_recalled = True
        msg.save()
        self.assertTrue(msg.is_recalled)
        self.assertEqual(msg.content, 'Hello')


class ChatConsumerTest(TransactionTestCase):
    async def test_ping_pong(self):
        from channels.testing import WebsocketCommunicator
        from chat.consumers import ChatConsumer
        from accounts.models import User

        user = await database_sync_to_async(User.objects.create_user)(
            username='wsuser', password='testpass123'
        )

        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), '/ws/chat/')
        communicator.scope['user'] = user
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await communicator.send_json_to({'type': 'ping'})
        response = await communicator.receive_json_from(timeout=5)
        self.assertEqual(response['type'], 'pong')

        await communicator.disconnect()

    async def test_unauthenticated_rejected(self):
        from channels.testing import WebsocketCommunicator
        from chat.consumers import ChatConsumer
        from django.contrib.auth.models import AnonymousUser

        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), '/ws/chat/')
        communicator.scope['user'] = AnonymousUser()
        connected, _ = await communicator.connect()
        self.assertFalse(connected)

    async def test_empty_text_ignored(self):
        from channels.testing import WebsocketCommunicator
        from chat.consumers import ChatConsumer
        from accounts.models import User

        user = await database_sync_to_async(User.objects.create_user)(
            username='wsuser2', password='testpass123'
        )

        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), '/ws/chat/')
        communicator.scope['user'] = user
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        count_before = await database_sync_to_async(Message.objects.count)()
        await communicator.send_json_to({'type': 'text', 'content': '   '})
        count_after = await database_sync_to_async(Message.objects.count)()
        self.assertEqual(count_before, count_after)

        await communicator.disconnect()
