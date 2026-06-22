from django.urls import path
from . import views

app_name = 'plans'

urlpatterns = [
    path('places/', views.place_list, name='place_list'),
    path('places/new/', views.place_create, name='place_create'),
    path('places/<int:pk>/visit/', views.place_visit, name='place_visit'),
    path('places/<int:pk>/delete/', views.place_delete, name='place_delete'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/new/', views.movie_create, name='movie_create'),
    path('movies/<int:pk>/status/', views.movie_update_status, name='movie_update_status'),
    path('movies/<int:pk>/delete/', views.movie_delete, name='movie_delete'),
]
