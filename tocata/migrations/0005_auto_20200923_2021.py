# Generated by Django 2.2.1 on 2020-09-23 23:21

from django.db import migrations
import django_resized.forms
import tocata.models


class Migration(migrations.Migration):

    dependencies = [
        ('tocata', '0004_auto_20200914_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tocata',
            name='flayer_1920_1280',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='fotos/defecto/imagen_1920_1280.jpg', force_format='JPEG', keep_meta=True, quality=75, size=[1920, 1280], upload_to=tocata.models.upload_tocata_flayer_file_loc),
        ),
        migrations.AlterField(
            model_name='tocata',
            name='flayer_380_507',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='fotos/defecto/imagen_380_507.jpg', force_format='JPEG', keep_meta=True, quality=75, size=[380, 507], upload_to=tocata.models.upload_tocata_flayer_file_loc),
        ),
    ]
