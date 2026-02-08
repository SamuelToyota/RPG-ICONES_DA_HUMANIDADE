from django.contrib import admin
from django.urls import path, include
# Importações necessárias para as imagens funcionarem:
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# ESTA LINHA ABAIXO É OBRIGATÓRIA PARA AS FOTOS APARECEREM
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)