# Generated by Django 2.2.1 on 2020-04-15 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tocata', '0003_tocata_evaluacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tocata',
            name='asistentes_max',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tocata',
            name='asistentes_min',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tocata',
            name='asistentes_total',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tocata',
            name='costo',
            field=models.IntegerField(default=0),
        ),
    ]
