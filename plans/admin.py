from django.contrib import admin
from .models import Place, Movie


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'rating', 'is_visited', 'added_by']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'movie_type', 'status', 'rating', 'added_by']
