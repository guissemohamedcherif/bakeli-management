# Generated by Django 3.1.5 on 2021-02-26 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0011_auto_20210225_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscription',
            name='montant',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
