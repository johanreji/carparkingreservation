# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from gridapp.models import SlotsCache, Slots
from django.db.models import Exists, OuterRef
from django.db.models import F
# Create your models here.


class ReservationsSet(models.QuerySet):
    def add_engaged(self):
        return self.annotate(
            engaged=Exists(SlotsCache.objects.filter(reservation_id=OuterRef('reservation_id'))
                ))
            

class Reservations(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    slot_id = models.ForeignKey(
    	Slots,
    	on_delete=models.SET_NULL, null=True,
        related_name="reservations")
    booking_time = models.DateTimeField( auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    confirmation = models.BooleanField(default=False)
    payment = models.IntegerField(primary_key=False, default=0)

    objects = ReservationsSet.as_manager()
    

class PenaltyReservations(models.Model):
    reservation_id = models.IntegerField(primary_key=True)
    slot_id = models.ForeignKey(
        Slots,
        on_delete=models.SET_NULL, null=True, related_name="pl")
    actual_end_time=models.DateTimeField()
    lastseen_time=models.DateTimeField(auto_now_add=True)

class UnauthorizedParkings(models.Model):
    start_time = models.DateTimeField(primary_key=True)
    slot_id = models.ForeignKey(
        Slots,
        on_delete=models.SET_NULL, null=True)
    lastseen_time = models.DateTimeField(auto_now_add=True)
       




