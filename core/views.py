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
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Resultado
from .serializers import ResultadoSerializer
from .utils import gerar_pdf
import base64
import openpyxl

# API
class ResultadoViewSet(LoginRequiredMixin, ModelViewSet):
    queryset = Resultado.objects.all().order_by('-id')
    serializer_class = ResultadoSerializer

    @action(detail=True, methods=['get'])
    def imagem(self, request, pk=None):
        resultado = self.get_object()
        encoded_image = base64.b64encode(resultado.imagem).decode('utf-8')

        return Response({"imagemBase64": encoded_image})
    
class DashboardDataView(LoginRequiredMixin, APIView):
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
        distribution = (
            qs.values('informacao')
            .annotate(count=Count('id'))
        )

        # 3) monthly_counts (quantidade por mês, a partir de data_hora)
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




from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import Resultado
from .forms import ResultadoForm

class ResultadoUpdateView(LoginRequiredMixin, UpdateView):
    model = Resultado
    form_class = ResultadoForm
    template_name = 'editar_resultado.html'
    success_url = reverse_lazy('historico')



# páginas
from django.contrib.auth.decorators import login_required

@login_required
def historico_view(request):
    resultados = Resultado.objects.all()
    return render(request, 'historico.html', {'resultados': resultados})

@login_required
def home_view(request):
    return render(request, 'home.html')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
def sobre_view(request):
    return render(request, 'sobre.html')


# funções
@login_required
def download_pdf(request, pk):
    resultado = get_object_or_404(Resultado, pk=pk)
    return gerar_pdf(resultado)

@login_required
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


from django.views.generic import ListView
from django.utils.timezone import now
from .models import Evento

class EventosListView(ListView):
    model = Evento
    template_name = 'eventos.html'
    context_object_name = 'eventos'

    def get_queryset(self):
        # Remove eventos duplicados com base no campo `qr_value`
        eventos = Evento.objects.order_by('-data_hora')
        eventos_unicos = {}
        for evento in eventos:
            if evento.qr_value not in eventos_unicos:
                eventos_unicos[evento.qr_value] = evento
        return list(eventos_unicos.values())


from core.models import Evento
from django.utils.timezone import now

def registrar_evento_duplicidade(qr_value, ids):
    """
    Salva um evento de duplicidade no banco de dados.
    """
    mensagem = f"Os IDs {', '.join(map(str, ids))} possuem o mesmo QR Code: {qr_value}."
    Evento.objects.create(qr_value=qr_value, mensagem=mensagem, data_hora=now())

from django.views.generic import ListView
from .models import Evento
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EventoSerializer

class EventosListView(ListView):
    model = Evento
    template_name = 'eventos.html'
    context_object_name = 'eventos'
    ordering = ['-data_hora']  # Ordena por data/hora decrescente
    paginate_by = 20  # Opcional: Adiciona paginação para melhor performance


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Evento

# core/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

class RegistrarEventoAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            mensagem = data.get('mensagem')
            qr_value = data.get('qr_value')
            ids = data.get('ids')
            data_hora = data.get('data_hora')

            # Aqui você pode salvar o evento no banco de dados
            # Exemplo:
            # Evento.objects.create(mensagem=mensagem, qr_value=qr_value, ids=ids, data_hora=data_hora)

            return Response({"message": "Evento registrado com sucesso!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

import base64
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Resultado  

def get_resultado_imagem(request, id):
    try:
        resultado = Resultado.objects.get(id=id)
        if resultado.imagem:
            with open(resultado.imagem.path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return JsonResponse({"imagemBase64": encoded_string})
        else:
            return JsonResponse({"imagemBase64": ""})
    except Resultado.DoesNotExist:
        return JsonResponse({"error": "Resultado não encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
    
    # views.py
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Evento
import json
from django.core.exceptions import ValidationError

@method_decorator(csrf_exempt, name='dispatch')  # Em produção, gerencie CSRF adequadamente
class RegistrarEventoView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            mensagem = data.get("mensagem")
            qr_value = data.get("qr_value")
            data_hora = data.get("data_hora")

            if not all([mensagem, qr_value, data_hora]):
                return JsonResponse({"message": "Campos 'mensagem', 'qr_value' e 'data_hora' são obrigatórios."}, status=400)

            # Verifica se já existe um evento com o mesmo qr_value e mensagem
            evento_existente = Evento.objects.filter(qr_value=qr_value, mensagem=mensagem).first()

            if evento_existente:
                return JsonResponse({"message": "Evento já registrado anteriormente."}, status=200)

            # Criar novo evento
            evento = Evento.objects.create(
                mensagem=mensagem,
                qr_value=qr_value,
                data_hora=data_hora
            )

            return JsonResponse({"message": "Evento registrado com sucesso."}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Dados JSON inválidos."}, status=400)
        except ValidationError as ve:
            return JsonResponse({"message": ve.messages}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)
from django.http import JsonResponse, Http404

class ResultadoImagemView(View):
    def get(self, request, resultadoId, *args, **kwargs):
        try:
            resultado = Resultado.objects.get(pk=resultadoId)
            if resultado.imagem:
                with resultado.imagem.open("rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                return JsonResponse({"imagemBase64": encoded_string}, status=200)
            else:
                return JsonResponse({"message": "Imagem não encontrada."}, status=404)
        except Resultado.DoesNotExist:
            raise Http404("Resultado não encontrado.")