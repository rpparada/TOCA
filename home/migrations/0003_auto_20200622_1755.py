# Generated by Django 2.2.1 on 2020-06-22 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20200622_1730'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testimonios',
            old_name='objetico',
            new_name='objetivo',
        ),
    ]