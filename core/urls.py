# core/urls.py

from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import (
    ResultadoViewSet,
    historico_view,
    home_view,
    dashboard_view,
    sobre_view,
    DashboardDataView, 
    download_pdf,
    exportar_excel,
    ResultadoUpdateView,
    EventosListView,
    RegistrarEventoAPIView,
    RegistrarEventoView,
    ResultadoImagemView
)

router = DefaultRouter()
router.register(r'resultados', ResultadoViewSet, basename='resultado')

# core/urls.py

urlpatterns = [
    # Rotas da API (por exemplo, /api/resultados/)
    path('api/', include(router.urls)),
    path('api/dashboard-data/', DashboardDataView.as_view(), name='dashboard-data'),

    # Páginas
    path('home', home_view, name='home'),             # /
    path('historico/', historico_view, name='historico'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('sobre/', sobre_view, name='sobre'),
    path('resultados/<int:pk>/editar/', ResultadoUpdateView.as_view(), name='editar_resultado'),
    path('eventos/', EventosListView.as_view(), name='eventos'),  # Removido duplicado
    path('api/eventos/registrar/', RegistrarEventoView.as_view(), name='registrar_evento'),
    path('eventos/', EventosListView.as_view(), name='lista_eventos'),
    path('api/resultados/<int:resultadoId>/imagem/', ResultadoImagemView.as_view(), name='resultado_imagem'),

    # Rotas de funções
    path('resultados/<int:pk>/download/', download_pdf, name='download_resultado'),  # Renomeado de 'download_pdf' para 'download_resultado'
    path('historico/exportar/', exportar_excel, name='exportar_excel'),
    path('api/eventos/registrar/', RegistrarEventoAPIView.as_view(), name='registrar_evento'),

    # Autenticação
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

