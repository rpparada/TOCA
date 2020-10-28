# Generated by Django 2.2.1 on 2020-10-15 01:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orden', '0022_entradascompradas_slug'),
        ('anulaciones', '0003_remove_anulacionentrada_motivo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anulacionentrada',
            name='metodo_reembolso',
        ),
        migrations.AddField(
            model_name='anulacionentrada',
            name='cobro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orden.Cobro'),
        ),
    ]