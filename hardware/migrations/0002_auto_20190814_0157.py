# Generated by Django 2.2.4 on 2019-08-14 00:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpost',
            old_name='images',
            new_name='image',
        ),
    ]