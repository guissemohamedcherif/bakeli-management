# Generated by Django 3.1.5 on 2021-03-06 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_auto_20210306_1824'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pere',
            old_name='Pere',
            new_name='person',
        ),
    ]