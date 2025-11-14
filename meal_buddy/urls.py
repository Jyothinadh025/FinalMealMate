
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('delivery.urls')),
]

# Media files setting (VERY IMPORTANT for images)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
