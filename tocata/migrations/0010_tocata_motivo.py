# Generated by Django 2.2.1 on 2020-10-15 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tocata', '0009_auto_20201012_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='tocata',
            name='motivo',
            field=models.CharField(choices=[('artista', 'Suspendido por Artista'), ('anfitrion', 'Anfitrio canceló Lugar'), ('otro', 'Otro')], default='artista', max_length=20),
        ),
    ]
