# Generated by Django 2.2.1 on 2020-10-15 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anulaciones', '0006_tocatacancelada'),
    ]

    operations = [
        migrations.AddField(
            model_name='tocatacancelada',
            name='motivo',
            field=models.CharField(choices=[('artista', 'Suspendido por Artista'), ('anfitrion', 'Anfitrio canceló Lugar'), ('otro', 'Otro')], default='artista', max_length=20),
        ),
    ]
