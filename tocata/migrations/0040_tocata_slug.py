# Generated by Django 2.2.1 on 2020-07-26 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tocata', '0039_auto_20200725_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='tocata',
            name='slug',
            field=models.SlugField(default='test'),
        ),
    ]
