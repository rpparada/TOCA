# Generated by Django 2.2.1 on 2020-08-15 01:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=100)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=100)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=100)),
                ('nombre', models.CharField(max_length=100)),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='lugar.Region')),
            ],
        ),
        migrations.CreateModel(
            name='Lugar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=200)),
                ('nombre_calle', models.CharField(max_length=200)),
                ('numero', models.IntegerField()),
                ('ciudad', models.CharField(blank=True, max_length=200)),
                ('pais', models.CharField(default='Chile', max_length=100)),
                ('codigo_postal', models.CharField(blank=True, max_length=20)),
                ('departamento', models.CharField(blank=True, max_length=20)),
                ('otros', models.CharField(blank=True, max_length=20)),
                ('descripción', models.TextField(blank=True)),
                ('capacidad', models.IntegerField()),
                ('evaluacion', models.IntegerField(choices=[(0, 'No Evaluada'), (1, 'Muy Mala'), (2, 'Mala'), (3, 'Regular'), (4, 'Buena'), (5, 'Muy Buena')], default=0)),
                ('estado', models.CharField(choices=[('DI', 'Disponible'), ('ND', 'No Disponible')], default='DI', max_length=2)),
                ('fecha_crea', models.DateTimeField(auto_now_add=True)),
                ('fecha_actu', models.DateTimeField(auto_now=True)),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lugar.Comuna')),
                ('provincia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='lugar.Provincia')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lugar.Region')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comuna',
            name='provincia',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='lugar.Provincia'),
        ),
        migrations.AddField(
            model_name='comuna',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='lugar.Region'),
        ),
    ]
