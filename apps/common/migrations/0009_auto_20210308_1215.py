# Generated by Django 3.1.5 on 2021-03-08 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_auto_20210307_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mere',
            name='person',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='common.person'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pere',
            name='person',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='common.person'),
            preserve_default=False,
        ),
    ]