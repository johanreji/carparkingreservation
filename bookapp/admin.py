# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import PenaltyReservations, UnauthorizedParkings

# admin.site.register(PenaltyReservations)
# admin.site.register(UnauthorizedParkings)

@admin.register(UnauthorizedParkings)
class UnauthorizedParkingsAdmin(admin.ModelAdmin):
  readonly_fields=('lastseen_time','getslot_id','start_time')
  fields = ('getslot_id', 'start_time','lastseen_time')
  labels = {
            'getslot_id': 'Slot Number',
        }
  list_display = ('start_time', 'getslot_id')
  def getslot_id(self, obj):
    try:
    	return obj.slot_id.pk
    except Exception:
    	return "None"


@admin.register(PenaltyReservations)
class PenaltyReservations(admin.ModelAdmin):
  readonly_fields=('lastseen_time','reservation','actual_end_time','slot')
  fields = ('reservation', 'actual_end_time','lastseen_time','slot')
  labels = {
            'slot': 'Slot Number','actual_end_time':'Endtime','lastseen_time':'Last Seen',
        }
  list_display = ('reservation', 'slot')
  def reservation(self, obj):
    return obj.reservation_id
  def slot(self, obj):
    return obj.slot_id.slot_id
