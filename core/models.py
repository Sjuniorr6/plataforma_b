from django.db import models

class Resultado(models.Model):
    qr_value = models.CharField(max_length=255)
    max_padroes = models.IntegerField()
    informacao = models.CharField(max_length=200)
    data_hora = models.DateTimeField()
    imagem = models.BinaryField()

    class Meta:
        db_table = 'resultados'  # Certifique-se de usar o nome correto da tabela