# Generated by Django 5.1.2 on 2025-01-20 18:46

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr_value', models.CharField(max_length=255)),
                ('mensagem', models.TextField()),
                ('data_hora', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
                'ordering': ['-data_hora'],
            },
        ),
        migrations.CreateModel(
            name='Resultado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr_value', models.CharField(max_length=255)),
                ('max_padroes', models.IntegerField()),
                ('informacao', models.CharField(max_length=200)),
                ('fazenda', models.CharField(blank=True, max_length=200, null=True)),
                ('data_hora', models.DateTimeField()),
                ('imagem', models.BinaryField(blank=True, null=True)),
            ],
            options={
                'db_table': 'resultados',
            },
        ),
    ]
