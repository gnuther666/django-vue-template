# Generated by Django 4.2.4 on 2024-06-17 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_frontmenumodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frontmenumodel',
            name='item_description',
            field=models.TextField(default=None),
        ),
    ]