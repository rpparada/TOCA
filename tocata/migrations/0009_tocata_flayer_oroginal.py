# Generated by Django 2.2.1 on 2020-05-08 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tocata', '0008_tocata_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='tocata',
            name='flayer_oroginal',
            field=models.ImageField(blank=True, upload_to='fotos/tocatas/%Y/%m/%d/'),
        ),
    ]
