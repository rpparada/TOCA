# Generated by Django 2.2.1 on 2020-04-30 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0010_usuarioartista_tipo_cuenra'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuarioartista',
            old_name='tipo_cuenra',
            new_name='tipo_cuenta',
        ),
    ]
