# Generated by Django 2.2.1 on 2020-04-30 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0009_usuarioartista_num_cuenta'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarioartista',
            name='tipo_cuenra',
            field=models.CharField(choices=[('001', 'Cuenta Corriente'), ('002', 'Cuenta de Ahorro'), ('003', 'Cuenta Vista'), ('004', 'Cuenta Chequera Electrónica'), ('005', 'Cuenta RUT')], default='001', max_length=200),
        ),
    ]