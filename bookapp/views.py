# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.shortcuts import render, reverse, redirect
import mysql.connector
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from datetime import datetime, timedelta
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import Reservations
from gridapp.models import Slots
from accounts.models import User
from django.db.models import Q
import json
import pytz
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

@csrf_exempt
def searchslots(request):
    if(request.method=="POST"):
        print("request post data")
        print(str(request.POST))
        indian=pytz.timezone('Asia/Kolkata')
        #request_data=request.POST["data"]
        start_date=request.POST["startdate"]
        end_date=request.POST["enddate"]
        start_time=request.POST["starttime"]
        end_time=request.POST["endtime"]
        start_datetime=start_date + ' ' + start_time 
        start_datetime=datetime.strptime(start_datetime,"%Y-%m-%d %H:%M")
        start_datetime=start_datetime.astimezone(pytz.utc)
        end_datetime=end_date + ' ' + end_time
        end_datetime=datetime.strptime(end_datetime,"%Y-%m-%d %H:%M")
        end_datetime=end_datetime.astimezone(pytz.utc)

        print(f"datetimes: st:  {start_datetime} et: {end_datetime}")
        q1=Reservations.objects.filter(start_time__lte=start_datetime, end_time__gte=start_datetime).only('slot_id')
        q2=Reservations.objects.filter(Q(start_time__range=(start_datetime, end_datetime-timedelta(minutes=1))) | Q(end_time__range=(start_datetime+timedelta(minutes=1), end_datetime))).only('slot_id')
        booked_slots=q1.union(q2)
        # print(str(booked_slots))
        booked_slots_list=list(map(lambda x: x.slot_id.slot_id, booked_slots))
        print(str(booked_slots_list))
        avaliable_slots=Slots.objects.exclude(slot_id__in=booked_slots_list).only('slot_id')
        avaliable_slots_list=list(avaliable_slots)
        list2=list(map(lambda x: x.slot_id, avaliable_slots))
        print(list2)
        #print(avaliable_slots_list[0].slot_id)
        grid_dict={}
        booked_dict={}
        for i in booked_slots_list:
          booked_dict[i]=1;
        avaliable_dict={}
        for slot in avaliable_slots_list:
            avaliable_dict[slot.slot_id]=0   
        grid_dict["booked"]=booked_dict
        grid_dict["avaliable"]=avaliable_dict    
        print(grid_dict)    
        return JsonResponse(grid_dict) 

    return JsonResponse({"status":1}) 

class Bookslot(LoginRequiredMixin,View):
    login_url = '/grid/getslots/html/'
    #redirect_field_name = 'redirect_to'
    def post(self, request):
        print("Entered book slot")
        print(str(request.POST))
        indian=pytz.timezone('Asia/Kolkata')
        current_slot_id = request.POST["slotselected"]
        current_user = request.user
        current_slot = Slots.objects.get(slot_id=current_slot_id)
        start_date=request.POST["sdate"]
        end_date=request.POST["edate"]
        start_time=request.POST["stime"]
        end_time=request.POST["etime"]
        start_datetime=start_date + ' ' + start_time 
        start_datetime=datetime.strptime(start_datetime,"%Y-%m-%d %H:%M")
        start_datetime=start_datetime.astimezone(pytz.utc)
        end_datetime=end_date + ' ' + end_time
        end_datetime=datetime.strptime(end_datetime,"%Y-%m-%d %H:%M")
        end_datetime=end_datetime.astimezone(pytz.utc)
        print("start datetime: ", start_datetime, "enddattime: ", end_datetime)
        reservation_id=None
        try:
            with transaction.atomic():
                q1=Reservations.objects.filter(start_time__lte=start_datetime, end_time__gte=start_datetime).only('slot_id')
                q2=Reservations.objects.filter(Q(start_time__range=(start_datetime, end_datetime-timedelta(minutes=1))) | Q(end_time__range=(start_datetime+timedelta(minutes=1), end_datetime))).only('slot_id')
                booked_slots=q1.union(q2)
                print("len is : 0,", len(booked_slots))
                booked_slots_list=set(list(map(lambda x: x.slot_id.slot_id, booked_slots)))
                print("booked slots list is")
                print(booked_slots_list)
                if(int(current_slot_id) not in booked_slots_list):
                  new_reservation=Reservations(user_id=current_user, slot_id=current_slot, start_time=start_datetime,
                    end_time=end_datetime)
                  new_reservation.save()
                  reservation_id=new_reservation.reservation_id;
            if(reservation_id):      
                  diff=abs(start_datetime - end_datetime)
                  total_mins = (diff.days*1440 + diff.seconds/60)
                  amt=total_mins/60*10
                  amt=round(amt,2)
                  context={"slotselected":current_slot_id,"dst":start_datetime,"det":end_datetime,"amt":amt,
                  "st":start_time, "et": end_time, "name":request.user.email, "rid":reservation_id}
                  return render(request, "bookapp/confirm.html", context)
            else:
                  return HttpResponse("seat already booked")
        except IntegrityError:
            return HttpResponse({"status":1})

    def get(self, request):
        return JsonResponse({"status":1})        
        

@login_required
def confirmslot(request):
  if(request.method=="POST"):
    print(str(request.POST))
    reservation_id=int(request.POST["rid"])
    payment= int(float(request.POST["amount"]))
    current_reservation=Reservations.objects.get(reservation_id=reservation_id)
    print(current_reservation)
    if current_reservation:
      current_reservation.confirmation=True;
      current_reservation.payment=payment
      current_reservation.save()
      return redirect("/bookings/mybookings")
  return JsonResponse({"status":1})


@login_required
def bookedslots(request):
  if(request.method=="GET"):
    current_user=request.user
    user_reservations=Reservations.objects.filter(user_id=current_user.id)
    print(user_reservations)
    return render(request, "bookapp/userbookings.html",{"result":user_reservations})
  else:
    return JsonResponse({"status":1})



