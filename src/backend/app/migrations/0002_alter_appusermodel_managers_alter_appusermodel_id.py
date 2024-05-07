# Generated by Django 4.2.4 on 2024-05-06 11:11

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='appusermodel',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='appusermodel',
            name='id',
            field=models.CharField(max_length=64, primary_key=True, serialize=False),
        ),
    ]
