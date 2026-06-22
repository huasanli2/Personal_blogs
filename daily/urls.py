from django.urls import path
from . import views

app_name = 'daily'

urlpatterns = [
    path('food/', views.food_list, name='food_list'),
    path('food/new/', views.food_create, name='food_create'),
    path('food/<int:pk>/like/', views.food_like, name='food_like'),
    path('journal/', views.journal_list, name='journal_list'),
    path('journal/new/', views.journal_create, name='journal_create'),
    path('whisper/', views.whisper_list, name='whisper_list'),
    path('whisper/new/', views.whisper_create, name='whisper_create'),
]
