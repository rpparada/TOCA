# Generated by Django 2.2.1 on 2020-09-04 15:23

import django.core.files.storage
from django.db import migrations, models
import tocata.models


class Migration(migrations.Migration):

    dependencies = [
        ('tocata', '0003_auto_20200904_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tocataticketfile',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/Users/rodrigoparada/Desktop/Proyectos/Proyectos Django/TOCA/protected_media'), upload_to=tocata.models.upload_tocata_ticket_file_loc),
        ),
    ]