# Generated by Django 2.2 on 2019-05-08 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookapp', '0006_unauthorizedparkings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='penaltyreservations',
            name='slot_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pl', to='gridapp.Slots'),
        ),
        migrations.AlterField(
            model_name='reservations',
            name='slot_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservations', to='gridapp.Slots'),
        ),
    ]