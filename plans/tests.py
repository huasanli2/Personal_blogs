from django.test import TestCase, Client
from django.urls import reverse
from .models import Place, Movie
from accounts.models import User


class PlaceDeleteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.other_user = User.objects.create_user(username='user2', password='pass123')
        self.place = Place.objects.create(
            added_by=self.user,
            name='Test Place',
            rating=3,
        )

    def test_owner_can_delete(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.post(reverse('plans:place_delete', args=[self.place.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Place.objects.filter(pk=self.place.pk).exists())

    def test_other_user_cannot_delete(self):
        self.client.login(username='user2', password='pass123')
        response = self.client.post(reverse('plans:place_delete', args=[self.place.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Place.objects.filter(pk=self.place.pk).exists())

    def test_delete_requires_post(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('plans:place_delete', args=[self.place.pk]))
        self.assertEqual(response.status_code, 405)


class MovieDeleteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.other_user = User.objects.create_user(username='user2', password='pass123')
        self.movie = Movie.objects.create(
            added_by=self.user,
            title='Test Movie',
            movie_type='movie',
        )

    def test_owner_can_delete(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.post(reverse('plans:movie_delete', args=[self.movie.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Movie.objects.filter(pk=self.movie.pk).exists())

    def test_other_user_cannot_delete(self):
        self.client.login(username='user2', password='pass123')
        response = self.client.post(reverse('plans:movie_delete', args=[self.movie.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Movie.objects.filter(pk=self.movie.pk).exists())
