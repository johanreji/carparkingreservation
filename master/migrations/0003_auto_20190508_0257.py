# Generated by Django 2.2 on 2019-05-07 21:27

from django.db import migrations, models
import master.models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0002_auto_20190507_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingareas',
            name='area_image',
            field=models.ImageField(height_field='height', upload_to=master.models.user_directory_path, width_field='width'),
        ),
    ]
