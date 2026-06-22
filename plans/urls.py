from django.urls import path
from . import views

app_name = 'plans'

urlpatterns = [
    path('places/', views.place_list, name='place_list'),
    path('places/new/', views.place_create, name='place_create'),
    path('places/<int:pk>/visit/', views.place_visit, name='place_visit'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/new/', views.movie_create, name='movie_create'),
    path('movies/<int:pk>/status/', views.movie_update_status, name='movie_update_status'),
]
