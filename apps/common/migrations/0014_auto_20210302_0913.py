# Generated by Django 3.1.5 on 2021-03-02 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0013_mensualite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscription',
            name='num',
            field=models.IntegerField(),
        ),
    ]