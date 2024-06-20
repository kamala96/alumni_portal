
from django.conf import settings
from django.conf.urls.static import static
from decouple import config
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(config('SECRET_ADMIN_URL') + '/admin/', admin.site.urls),
    path('', include('site_app.urls')),
]

# Only for development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
