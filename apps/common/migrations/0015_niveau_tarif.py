# Generated by Django 3.1.5 on 2021-03-02 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0014_auto_20210302_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='niveau',
            name='tarif',
            field=models.FloatField(default=12),
            preserve_default=False,
        ),
    ]