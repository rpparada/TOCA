# Generated by Django 2.2.1 on 2020-09-30 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('propuestaslugar', '0002_auto_20200928_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lugarestocata',
            name='lugar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lugar.Lugar'),
        ),
        migrations.AlterField(
            model_name='lugarestocata',
            name='tocataabierta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tocataabierta.TocataAbierta'),
        ),
    ]
