# Generated by Django 3.1.3 on 2020-12-21 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0018_auto_20201221_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='document',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
