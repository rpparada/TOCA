# Generated by Django 2.2.1 on 2020-07-25 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tocata', '0038_tocataabierta_costo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tocataabierta',
            name='descripción',
            field=models.TextField(blank=True, null=True),
        ),
    ]