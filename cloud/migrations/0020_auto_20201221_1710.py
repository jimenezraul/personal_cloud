# Generated by Django 3.1.3 on 2020-12-21 17:10

import cloud.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0019_upload_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='document',
            field=models.FileField(upload_to=cloud.models.user_directory_path),
        ),
    ]
