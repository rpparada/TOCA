# Generated by Django 2.2.1 on 2020-09-07 00:33

import artista.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artista', '0002_artista_foto_380_507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artista',
            name='foto_1920_1280',
            field=models.ImageField(blank=True, upload_to=artista.models.upload_fotos_artista_loc),
        ),
        migrations.AlterField(
            model_name='artista',
            name='foto_380_507',
            field=models.ImageField(blank=True, upload_to=artista.models.upload_fotos_artista_loc),
        ),
        migrations.AlterField(
            model_name='artista',
            name='foto_525_350',
            field=models.ImageField(blank=True, upload_to=artista.models.upload_fotos_artista_loc),
        ),
    ]