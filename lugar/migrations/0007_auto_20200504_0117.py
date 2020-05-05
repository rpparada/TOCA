# Generated by Django 2.2.1 on 2020-05-04 01:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lugar', '0006_remove_comuna_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lugar',
            name='comuna',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lugar.Comuna'),
        ),
        migrations.AlterField(
            model_name='lugar',
            name='provincia',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lugar.Provincia'),
        ),
        migrations.AlterField(
            model_name='lugar',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lugar.Region'),
        ),
    ]