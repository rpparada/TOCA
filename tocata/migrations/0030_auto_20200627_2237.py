# Generated by Django 2.2.1 on 2020-06-27 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tocata', '0029_auto_20200627_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lugarestocata',
            name='estado',
            field=models.CharField(choices=[('EL', 'Elegido'), ('NE', 'No Elegido'), ('PE', 'Pendiente'), ('CA', 'Cancelada')], default='PE', max_length=2),
        ),
    ]