# Generated by Django 2.2.1 on 2020-06-27 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tocata', '0027_auto_20200626_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lugarestocata',
            name='estado',
            field=models.CharField(choices=[('EL', 'Elegido'), ('NE', 'No Elegido'), ('PE', 'Pendiente')], default='NE', max_length=2),
        ),
    ]