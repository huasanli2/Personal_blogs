from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_room, name='room'),
    path('send/', views.send_message, name='send'),
    path('upload/', views.upload_image, name='upload'),
    path('load/', views.load_messages, name='load'),
]
