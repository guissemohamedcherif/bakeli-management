# Generated by Django 3.1.5 on 2021-02-23 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_classe'),
    ]

    operations = [
        migrations.AddField(
            model_name='classe',
            name='ecole',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.ecole'),
        ),
    ]