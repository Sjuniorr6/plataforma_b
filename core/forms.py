# forms.py
from django import forms

class DateRangeForm(forms.Form):
    start_date = forms.DateField(required=False, label='Data inicial')
    end_date = forms.DateField(required=False, label='Data final')


from django import forms
from .models import Resultado

class ResultadoForm(forms.ModelForm):
    class Meta:
        model = Resultado
        fields = ['qr_value', 'max_padroes', 'informacao', 'fazenda', 'data_hora']  # Exclua 'imagem' daqui
