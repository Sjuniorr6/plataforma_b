# views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils.dateparse import parse_date
from django.http import HttpResponse
from .models import Resultado
from .serializers import ResultadoSerializer
from .utils import gerar_pdf
import base64
import openpyxl

# API
class ResultadoViewSet(ModelViewSet):
    queryset = Resultado.objects.all()
    serializer_class = ResultadoSerializer

    @action(detail=True, methods=['get'])
    def imagem(self, request, pk=None):
        resultado = self.get_object()
        encoded_image = base64.b64encode(resultado.imagem).decode('utf-8')

        return Response({"imagemBase64": encoded_image})
    
class DashboardDataView(APIView):
    def get(self, request, format=None):
        # Pega os parâmetros de data
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        qs = Resultado.objects.all()

        # Se tiver start_date e end_date, filtra
        if start_date_str:
            start_date = parse_date(start_date_str)
            if start_date:
                qs = qs.filter(data_hora__date__gte=start_date)
        if end_date_str:
            end_date = parse_date(end_date_str)
            if end_date:
                qs = qs.filter(data_hora__date__lte=end_date)

        # 1) total_tests
        total_tests = qs.count()

        # 2) distribution (quantidade por 'informacao')
        #    Ex: [{"informacao": "POSITIVO - PATENTE VALIDA", "count": 10}, ...]
        distribution = (
            qs.values('informacao')
            .annotate(count=Count('id'))
        )

        # 3) monthly_counts (quantidade por mês, a partir de data_hora)
        #    Ex: [{"month": "2024-01-01", "count": 4}, ...]
        monthly_counts = (
            qs.annotate(month=TruncMonth('data_hora'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )

        data = {
            'total_tests': total_tests,
            'distribution_data': list(distribution),
            'monthly_counts_data': list(monthly_counts),
        }
        return Response(data)

# páginas
def historico_view(request):
    resultados = Resultado.objects.all()
    return render(request, 'historico.html', {'resultados': resultados})

def home_view(request):
    return render(request, 'home.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')

def sobre_view(request):
    return render(request, 'sobre.html')


# funções
def download_pdf(request, pk):
    resultado = get_object_or_404(Resultado, pk=pk)
    return gerar_pdf(resultado)

def exportar_excel(request):
    # Criação de um workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Histórico"

    # Adiciona cabeçalhos
    ws.append(["ID", "QR Code", "Informação", "Data e Hora"])

    # Busca os dados
    resultados = Resultado.objects.all()
    for resultado in resultados:
        ws.append([
            resultado.id,
            resultado.qr_value,
            resultado.informacao,
            resultado.data_hora.strftime('%d/%m/%Y %H:%M:%S'),
        ])

    # Responde com o arquivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="historico.xlsx"'
    wb.save(response)
    return response
