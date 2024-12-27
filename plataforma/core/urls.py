# core/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ResultadoViewSet,
    historico_view,
    home_view,
    dashboard_view,
    sobre_view,
    DashboardDataView, 
    download_pdf,
    exportar_excel
)

router = DefaultRouter()
router.register(r'resultados', ResultadoViewSet, basename='resultado')

urlpatterns = [
    # Rotas da API (por exemplo, /api/resultados/)
    path('api/', include(router.urls)),
    path('api/dashboard-data/', DashboardDataView.as_view(), name='dashboard-data'),

    # Páginas
    path('', home_view, name='home'),             # /
    path('historico/', historico_view, name='historico'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('sobre/', sobre_view, name='sobre'),

    # Rotas de funções
    path('resultados/<int:pk>/download/', download_pdf, name='download_pdf'),
    path('historico/exportar/', exportar_excel, name='exportar_excel'),
]
