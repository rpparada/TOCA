# Generated by Django 2.2.1 on 2020-04-17 01:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tocata', '0005_auto_20200417_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tocata',
            name='fecha_actu',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]