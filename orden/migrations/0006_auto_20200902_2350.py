# Generated by Django 2.2.1 on 2020-09-02 23:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orden', '0005_controlcobro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controlcobro',
            name='orden',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='orden.OrdenCompra'),
        ),
        migrations.AlterField(
            model_name='controlcobro',
            name='token',
            field=models.CharField(max_length=64),
        ),
    ]
