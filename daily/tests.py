from django.test import TestCase, Client
from django.urls import reverse
from .models import FoodLog, DailyLog, Whisper
from accounts.models import User


class FoodDeleteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.other_user = User.objects.create_user(username='user2', password='pass123')
        self.food = FoodLog.objects.create(
            author=self.user,
            meal_type='lunch',
            title='Test Food',
            date='2025-01-01',
        )

    def test_owner_can_delete(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.post(reverse('daily:food_delete', args=[self.food.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(FoodLog.objects.filter(pk=self.food.pk).exists())

    def test_other_user_cannot_delete(self):
        self.client.login(username='user2', password='pass123')
        response = self.client.post(reverse('daily:food_delete', args=[self.food.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(FoodLog.objects.filter(pk=self.food.pk).exists())

    def test_delete_requires_post(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('daily:food_delete', args=[self.food.pk]))
        self.assertEqual(response.status_code, 405)

    def test_unauthenticated_cannot_delete(self):
        response = self.client.post(reverse('daily:food_delete', args=[self.food.pk]))
        self.assertEqual(response.status_code, 302)


class JournalDeleteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.other_user = User.objects.create_user(username='user2', password='pass123')
        self.journal = DailyLog.objects.create(
            author=self.user,
            content='Test journal',
            date='2025-01-01',
        )

    def test_owner_can_delete(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.post(reverse('daily:journal_delete', args=[self.journal.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(DailyLog.objects.filter(pk=self.journal.pk).exists())

    def test_other_user_cannot_delete(self):
        self.client.login(username='user2', password='pass123')
        response = self.client.post(reverse('daily:journal_delete', args=[self.journal.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(DailyLog.objects.filter(pk=self.journal.pk).exists())


class WhisperDeleteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.other_user = User.objects.create_user(username='user2', password='pass123')
        self.whisper = Whisper.objects.create(
            author=self.user,
            content='Test whisper',
        )

    def test_owner_can_delete(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.post(reverse('daily:whisper_delete', args=[self.whisper.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Whisper.objects.filter(pk=self.whisper.pk).exists())

    def test_other_user_cannot_delete(self):
        self.client.login(username='user2', password='pass123')
        response = self.client.post(reverse('daily:whisper_delete', args=[self.whisper.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Whisper.objects.filter(pk=self.whisper.pk).exists())
