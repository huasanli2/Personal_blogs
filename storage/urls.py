from django.urls import path
from . import views

app_name = 'storage'

urlpatterns = [
    path('', views.storage_list, name='list'),
]
