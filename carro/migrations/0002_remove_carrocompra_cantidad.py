# Generated by Django 2.2.1 on 2020-08-25 01:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carro', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrocompra',
            name='cantidad',
        ),
    ]
