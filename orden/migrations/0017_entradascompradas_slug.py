# Generated by Django 2.2.1 on 2020-09-21 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orden', '0016_ordencompra_fecha_pago'),
    ]

    operations = [
        migrations.AddField(
            model_name='entradascompradas',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
