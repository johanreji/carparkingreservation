# Generated by Django 2.2 on 2019-05-05 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookapp', '0003_auto_20190505_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservations',
            name='booking_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]