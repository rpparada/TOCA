# Generated by Django 2.2.1 on 2020-07-29 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artista', '0009_auto_20200729_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='estilo',
            name='activo',
            field=models.BooleanField(default=True),
        ),
    ]