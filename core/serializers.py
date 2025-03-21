from rest_framework import serializers
from .models import Resultado, Evento

class ResultadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultado
        fields = [
            'id',
            'qr_value',
            'max_padroes',
            'id_entrada',  # <-- Adicionamos aqui
            'informacao',
            'data_hora',
            'fazenda',
        ]

class EventoSerializer(serializers.ModelSerializer):
    # Se seu Evento tem relacionamento com Resultado,
    # mantenha a referência ou ajuste conforme sua lógica.
    resultado = serializers.PrimaryKeyRelatedField(queryset=Resultado.objects.all())

    class Meta:
        model = Evento
        fields = ['resultado', 'qr_value', 'mensagem', 'data_hora']
