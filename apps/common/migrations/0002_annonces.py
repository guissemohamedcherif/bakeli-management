# Generated by Django 3.1.7 on 2021-04-12 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Annonces',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(blank=True, max_length=250)),
                ('content', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
