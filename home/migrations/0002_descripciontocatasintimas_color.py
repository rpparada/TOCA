# Generated by Django 2.2.1 on 2020-08-15 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='descripciontocatasintimas',
            name='color',
            field=models.CharField(default='#2F2F2F', max_length=7),
        ),
    ]