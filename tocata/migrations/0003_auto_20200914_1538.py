# Generated by Django 2.2.1 on 2020-09-14 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tocata', '0002_auto_20200907_0012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tocata',
            name='evaluacion',
        ),
        migrations.AlterField(
            model_name='tocata',
            name='estado',
            field=models.CharField(choices=[('publicado', 'Publicado'), ('suspendido', 'Suspendido'), ('confirmado', 'Confirmado'), ('vendido', 'Vendido'), ('completado', 'Completado'), ('borrado', 'Borrado')], default='publicado', max_length=2),
        ),
    ]
