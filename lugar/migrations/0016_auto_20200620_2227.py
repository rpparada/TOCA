# Generated by Django 2.2.1 on 2020-06-20 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lugar', '0015_auto_20200620_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lugar',
            name='nombre',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]