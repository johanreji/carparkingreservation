# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from datetime import datetime, timedelta
from django.http import JsonResponse
from .models import Slots, SlotsCache
from master.models import  SlotDims, ParkingAreas
from bookapp.models import Reservations
import json
import pytz
import time
import os
import mysql.connector
import itertools
from django.db.models import Sum, Avg, Max




CNNDELAY = 2

@csrf_exempt
def getdata(request):
 if(request.method=="POST"):
  data=request.POST["val"]
  cnnts=request.POST["ts"][:19]
  cnnts=datetime.strptime(cnnts,"%Y-%m-%d %H:%M:%S")
  #cnnts=cnnts.astimezone(pytz.utc)
  print(cnnts)
  details=json.loads(data)
  detailsplain={}
  db = mysql.connector.connect(user='django', password='virurohan', 
                                database='bookmyslot')
  cursor = db.cursor()
  #cur= db.cursor()
  cursor.execute('SELECT slot_id,occupied, confidence FROM gridapp_slots')
  result = cursor.fetchall()
  
  for i, j in details.items():
    
   k=i
   l=j
   detailsplain[k]=l
  datatuple=tuple(detailsplain.items())
  slot_len=len(datatuple)
  
  for i in range(slot_len):
   if(datatuple[i][1]=="True" and result[i][1]==0):
    print("change")
    q="""UPDATE gridapp_slots SET occupied = %s, cnnflag = %s, cnn_timestamp = %s, confidence = %s WHERE slot_id = %s ;"""
    d=(1,1,cnnts,0,datatuple[i][0])
    cursor.execute(q,d) 
   elif(datatuple[i][1]=="False" and result[i][1]==1):
    print("change to free : ", datatuple[i][0])
    q="""UPDATE gridapp_slots SET occupied = %s, cnnflag = %s, cnn_timestamp = %s, confidence = %s WHERE slot_id = %s ;"""
    d=(0,0,cnnts,0,datatuple[i][0])
    cursor.execute(q,d) 
   else:
    print("no change")
    q="""UPDATE gridapp_slots SET confidence = %s WHERE slot_id = %s ;"""
    d=(result[i][2] + 1, datatuple[i][0])
    cursor.execute(q, d)
  db.commit()
  cursor.close()
  db.close()
  return HttpResponse("succs")


def getslots(request, restype):
    if(request.method=="GET"):
        slot_list = Slots.objects.order_by('slot_id')
        query2 = ParkingAreas.objects.filter(is_active=True).order_by('-area_id')
        if not query2:
          return render(request, "gridapp/grid.html", {"result":None, "st":timezone.now(), "area":None, "centertext":None,"noarea":"Please add an area"})
        maxrow=SlotDims.objects.all().aggregate(Max('row'))['row__max']  
        print("max row")
        count=Slots.objects.count()
        if count <1:
          return render(request, "gridapp/grid.html", {"result":None, "st":timezone.now(), "area":None, "centertext":None,"noarea":"Please generate slots from admin page"})
        query2=query2[0]
        area=(query2.width, query2.height)
        area_id=query2.area_id
        height = min(area[1]/maxrow - 10*maxrow,75)
        maxcolumn=count/maxrow
        width=min(area[0]/maxrow - 10*maxcolumn, 50)
        halfheight=int(height/2)
        halfwidth=int(width/2)
        centertext=(halfwidth-10, halfheight-halfheight/(2*maxrow))
        area=(query2.width + maxcolumn*10, query2.height + maxrow*10, width, height)
        print("area_id",area_id)
        slot_dims = SlotDims.objects.filter(area_id__area_id=area_id, updated=True).order_by('row')
        print("slotdims", slot_dims)

        print("slot_list", slot_list)
        if restype=="html":
            grid_dict = {} #list of tuples of format (id, occupied)
            for slot in slot_list:
                if(slot.occupied):
                    grid_dict[slot.slot_id]=(1,)
                else:
                    grid_dict[slot.slot_id]=(0,)

            print(grid_dict)
            startrow=1
            xpos=10
            ypos=10
            
            incheight=height +10
            incwidth=width + 10
            
            for dim in slot_dims:
              sid=dim.slot_id
              if(dim.row>startrow):
                xpos=10
                ypos+=incheight
                startrow=dim.row
              gs=grid_dict[sid]  
              grid_dict[sid]=gs+ (xpos,ypos)
              xpos+=incwidth
            print(grid_dict)  
            return render(request, "gridapp/grid.html", {"result":grid_dict, "st":timezone.now(), "area":area, "centertext":centertext})
        else:
            grid_dict={}
            for slot in slot_list:
                 if(slot.occupied):
                 	grid_dict[slot.slot_id]=1
                 else:
                    grid_dict[slot.slot_id]=0 	
            print(grid_dict)        
            return JsonResponse(grid_dict) 

    else:
        messages.error(request, 'Invalid request type')
        return redirect(reverse('gridapp:index'))     

# def getdata2(request):
#   if(request.method=="POST"):
#     cnn_data=request.POST["val"]
#     cnn_timestamp=request.POST["ts"]
#     cnn_timestamp=float(cnn_timestamp)
#     cnn_timestamp = datetime.fromtimestamp(cnn_timestamp / 1e3)
#     details=json.loads(data)


@csrf_exempt
def qrscan(request):
  resdict={}
  if not request.user.is_authenticated:
    resdict["status"] =-1
    return JsonResponse(resdict)

  if(request.method=="POST"):
    received_json_data=json.loads(request.body)
    current_slot=int(received_json_data["slot_id"])
    user_id=request.user.id
    print("user id ", user_id)
    print("slot_id id ", current_slot)
    current_datetime=datetime.now()
    current_datetime=current_datetime.astimezone(pytz.utc)
    print("current datetime", current_datetime)
    reservation_query = Reservations.objects.filter(user_id=user_id, slot_id=current_slot,
      start_time__lt=current_datetime, end_time__gt=current_datetime,
      confirmation=True).only('slot_id', 'end_time', 'start_time')
    # r1=Reservations.objects.get(reservation_id=5)
    # print("r1; ", r1.start_time, r1.end_time)
    print(reservation_query)
    if reservation_query:
      print("qr scan check")
      resdict["status"]=1
      current_reservation = reservation_query[0]
      slot_obj = Slots.objects.get(slot_id=current_slot)
      car_check_flag = True
      while(True):
        if(slot_obj.occupied==True):
          try:
            slotcache_obj=SlotsCache.objects.get(slot_id=current_slot)
            if not slotcache_obj.reservation_id==None:
              resdict["status"] = 3
              return JsonResponse(resdict)
            else:
              # obj, created = Pe.objects.update_or_create(
              # first_name='John', last_name='Lennon',
              # defaults={'first_name': 'Bob'},
              # )
              slotcache_obj.reservation_id=current_reservation.reservation_id
              slotcache_obj.end_time=current_reservation.end_time
              slotcache_obj.save()
              break
          except SlotsCache.DoesNotExist:
            new_slot_cache=SlotsCache(slot_id=slot_obj,
              reservation_id=current_reservation.reservation_id, end_time=current_reservation.end_time)
            new_slot_cache.save()
            break 
        else:
          if car_check_flag:
            time.sleep(CNNDELAY)
            car_check_flag = False
          else:
            print("no car detected")
            resdict["status"] = 4
            return JsonResponse(resdict)    
      print("booking confirmed")
      return JsonResponse(resdict)
    else: 
      resdict["status"]=2
      print("you have not booked seat")
      return JsonResponse(resdict) 
  else:
    resdict["status"]=0
    return JsonResponse(resdict)     














 





