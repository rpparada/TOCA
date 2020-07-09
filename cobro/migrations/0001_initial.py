# Generated by Django 2.2.1 on 2020-07-06 20:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tocata', '0033_tocataabierta_costo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=0)),
                ('estado', models.CharField(choices=[('PE', 'Pendiente'), ('PA', 'Pagado'), ('CA', 'Cancelado')], default='PE', max_length=2)),
                ('fecha_actu', models.DateTimeField(auto_now=True)),
                ('fecha_crea', models.DateTimeField(auto_now_add=True)),
                ('tocata', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tocata.Tocata')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]