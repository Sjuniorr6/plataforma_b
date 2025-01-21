from django.db import models
from django.db import models
from django.utils.timezone import now
from django.db import models



class Resultado(models.Model):
    qr_value = models.CharField(max_length=255)
    max_padroes = models.IntegerField()
    informacao = models.CharField(max_length=200)
    fazenda = models.CharField(max_length=200,null=True,blank=True)
    data_hora = models.DateTimeField()
    imagem = models.BinaryField(null=True,blank=True)
    

    class Meta:
        db_table = 'resultados'  # Certifique-se de usar o nome correto da tabela
        
        
from django.db import models
from django.utils.timezone import now

class Evento(models.Model):
    qr_value = models.CharField(max_length=255, null=True, blank=True)
    mensagem = models.TextField()  # Armazena o alerta completo
    data_hora = models.DateTimeField(default=now)  # Timestamp do evento

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ["-data_hora"]

    def __str__(self):
        return f"{self.qr_value or 'N/A'}: {self.mensagem[:50]}"
