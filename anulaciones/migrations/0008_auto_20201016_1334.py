# Generated by Django 2.2.1 on 2020-10-16 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anulaciones', '0007_tocatacancelada_motivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anulacionentrada',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('enviadatbk', 'Enviada a Transbank'), ('reembolsadotbk', 'Reembolsado Transbank'), ('reembolsado', 'Reembolsado Manual')], default='pendiente', max_length=20),
        ),
    ]
