# Generated by Django 2.2.1 on 2020-08-16 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tocataabierta', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tocataabierta',
            name='estado',
            field=models.CharField(choices=[('publicado', 'Publicado'), ('suspendido', 'Suspendido'), ('confirmado', 'Confirmado'), ('borrado', 'Borrado')], default='publicado', max_length=20),
        ),
    ]
