# Generated by Django 2.2.1 on 2020-07-26 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tocata', '0041_auto_20200726_0140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tocata',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]