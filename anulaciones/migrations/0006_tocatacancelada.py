# Generated by Django 2.2.1 on 2020-10-15 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tocata', '0010_tocata_motivo'),
        ('anulaciones', '0005_auto_20201014_2219'),
    ]

    operations = [
        migrations.CreateModel(
            name='TocataCancelada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('reembolsado', 'Reembolsado')], default='pendiente', max_length=20)),
                ('fecha_actu', models.DateTimeField(auto_now=True)),
                ('fecha_crea', models.DateTimeField(auto_now_add=True)),
                ('tocata', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tocata.Tocata')),
            ],
        ),
    ]