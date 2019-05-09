# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Slots(models.Model):
    slot_id = models.AutoField(primary_key=True)
    occupied = models.BooleanField()
    cnn_timestamp = models.DateTimeField()
    cnnflag = models.BooleanField(default=False)
    confidence = models.IntegerField(primary_key=False, default=0)

class SlotsCache(models.Model):
    slot_id = models.OneToOneField(
        Slots,
        on_delete=models.CASCADE,
        related_name='slot_cache',
    )
    reservation_id = models.IntegerField(primary_key=False, null=True)
    end_time = models.DateTimeField(null=True)



