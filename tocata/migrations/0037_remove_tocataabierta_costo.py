# Generated by Django 2.2.1 on 2020-07-24 00:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tocata', '0036_auto_20200722_1805'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tocataabierta',
            name='costo',
        ),
    ]