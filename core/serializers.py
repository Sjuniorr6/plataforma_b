from rest_framework import serializers
from .models import Resultado

class ResultadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultado
        fields = [
            'id',
            'qr_value',
            'max_padroes',
            'informacao',
            'data_hora',
            'fazenda',
        ]
from rest_framework import serializers
from .models import Evento

class EventoSerializer(serializers.ModelSerializer):
    resultado = serializers.PrimaryKeyRelatedField(queryset=Resultado.objects.all())

    class Meta:
        model = Evento
        fields = ['resultado', 'qr_value', 'mensagem', 'data_hora']
