# Generated by Django 2.2.4 on 2019-08-14 01:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0002_auto_20190814_0157'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpost',
            old_name='image',
            new_name='images',
        ),
    ]