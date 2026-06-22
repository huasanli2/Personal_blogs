from django.urls import path
from . import views

app_name = 'daily'

urlpatterns = [
    path('food/', views.food_list, name='food_list'),
    path('food/new/', views.food_create, name='food_create'),
    path('food/<int:pk>/like/', views.food_like, name='food_like'),
    path('food/<int:pk>/delete/', views.food_delete, name='food_delete'),
    path('journal/', views.journal_list, name='journal_list'),
    path('journal/new/', views.journal_create, name='journal_create'),
    path('journal/<int:pk>/delete/', views.journal_delete, name='journal_delete'),
    path('whisper/', views.whisper_list, name='whisper_list'),
    path('whisper/new/', views.whisper_create, name='whisper_create'),
    path('whisper/<int:pk>/delete/', views.whisper_delete, name='whisper_delete'),
]
