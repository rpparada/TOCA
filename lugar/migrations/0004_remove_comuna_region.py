# Generated by Django 2.2.1 on 2020-05-03 02:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lugar', '0003_lugar_evaluacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comuna',
            name='region',
        ),
    ]