# Generated by Django 2.2.1 on 2020-07-31 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artista', '0016_auto_20200730_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cualidad',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='estilo',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]