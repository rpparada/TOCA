# Generated by Django 2.2.1 on 2020-08-28 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carro', '0008_auto_20200827_0026'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemcarrocompra',
            options={'ordering': ['tocata__nombre']},
        ),
    ]
