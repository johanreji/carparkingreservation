# Generated by Django 2.2 on 2019-06-09 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0004_auto_20190609_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='renderdims',
            name='id',
        ),
        migrations.AlterField(
            model_name='renderdims',
            name='slot_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
