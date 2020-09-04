# Generated by Django 2.2.1 on 2020-09-03 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orden', '0009_entradascompradas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entradascompradas',
            name='usuario',
        ),
        migrations.AddField(
            model_name='entradascompradas',
            name='orden',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='orden.OrdenCompra'),
            preserve_default=False,
        ),
    ]