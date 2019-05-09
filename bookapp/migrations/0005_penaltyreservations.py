# Generated by Django 2.2 on 2019-05-07 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gridapp', '0003_auto_20190507_1347'),
        ('bookapp', '0004_auto_20190505_1905'),
    ]

    operations = [
        migrations.CreateModel(
            name='PenaltyReservations',
            fields=[
                ('reservation_id', models.IntegerField(primary_key=True, serialize=False)),
                ('actual_end_time', models.DateTimeField()),
                ('lastseen_time', models.DateTimeField(auto_now_add=True)),
                ('slot_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gridapp.Slots')),
            ],
        ),
    ]
