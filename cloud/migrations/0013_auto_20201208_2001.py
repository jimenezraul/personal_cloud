# Generated by Django 3.1.3 on 2020-12-08 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0012_cloud_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloud',
            name='current_dir',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='cloud',
            name='dir_name',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='cloud',
            name='uid',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='cloud',
            name='user_root',
            field=models.CharField(default='', max_length=1000),
        ),
    ]