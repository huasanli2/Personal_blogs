from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('moments.urls')),
    path('', include('accounts.urls')),
    path('chat/', include('chat.urls')),
    path('daily/', include('daily.urls')),
    path('plans/', include('plans.urls')),
    path('storage/', include('storage.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
