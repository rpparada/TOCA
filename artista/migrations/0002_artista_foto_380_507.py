# Generated by Django 2.2.1 on 2020-08-18 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artista', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artista',
            name='foto_380_507',
            field=models.ImageField(blank=True, upload_to='fotos/artistas/'),
        ),
    ]
