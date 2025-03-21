# project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Todas as rotas do app "core" (API + páginas)
    path('core/', include('core.urls')),
]
