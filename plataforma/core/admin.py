from django.contrib import admin
from .models import Resultado

@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('qr_value', 'max_padroes', 'informacao', 'data_hora')
    search_fields = ('qr_value', 'informacao')
    list_filter = ('data_hora',)
