# Generated by Django 3.1.3 on 2021-01-05 19:05

import cloud.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0020_auto_20201221_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='document',
            field=models.FileField(max_length=1000, upload_to=cloud.models.user_directory_path),
        ),
    ]
