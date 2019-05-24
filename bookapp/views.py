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
from django.contrib import messages
from .models import Reservations
from gridapp.models import Slots, SlotsCache
from accounts.models import User
from django.db.models import Q
import json
import pytz
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BookingSearchForm, BookingForm
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

@csrf_exempt
def searchslots(request):
    if(request.method=="POST"):
        form = BookingSearchForm(request.POST)
        if form.is_valid():
          print("valid form")
        else:
          print("not valid")
          return JsonResponse({"status":2,"message":form.errors})    
        print("request post data")
        print(str(request.POST))
        # request_data=request.POST["data"]
        # start_date=request.POST["startdate"]
        # end_date=request.POST["enddate"]
        # start_time=request.POST["starttime"]
        # end_time=request.POST["endtime"]
        # start_datetime=start_date + ' ' + start_time 
        # start_datetime=datetime.strptime(start_datetime,"%Y-%m-%d %H:%M")
        start_datetime=form.cleaned_data["startdatetime"]
        start_datetime=start_datetime.astimezone(pytz.utc)
        end_datetime = form.cleaned_data["enddatetime"]
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
        grid_dict["status"]=1
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

    return JsonResponse({"status":3}) 

class Bookslot(LoginRequiredMixin,View):
    login_url = '/'
    #redirect_field_name = 'redirect_to'
    def post(self, request):
        print("Entered book slot")
        print(str(request.POST))
        form=BookingForm(request.POST)
        if form.is_valid():
          print("valid")  
        else:
          messages.warning(request, 'form validation error please refresh and try again')
          return redirect(reverse('gridapp:index'))

        current_slot_id = form.cleaned_data["slotselected"]
        current_user = request.user
        current_slot = Slots.objects.get(slot_id=current_slot_id)
        # start_date=request.POST["sdate"]
        # end_date=request.POST["edate"]
        # start_time=request.POST["stime"]
        # end_time=request.POST["etime"]
        # start_datetime=start_date + ' ' + start_time 
        # start_datetime=datetime.strptime(start_datetime,"%Y-%m-%d %H:%M")
        start_datetime=form.cleaned_data["startdatetime"]
        start_datetime=start_datetime.astimezone(pytz.utc)
        # end_datetime=end_date + ' ' + end_time
        # end_datetime=datetime.strptime(end_datetime,"%Y-%m-%d %H:%M")
        end_datetime=form.cleaned_data["enddatetime"]
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
                  "st":form.cleaned_data["starttime"], "et": form.cleaned_data["endtime"], "name":request.user.email, "rid":reservation_id}
                  return render(request, "bookapp/confirm.html", context)
            else:
                  messages.warning(request, 'Slot is booked by another person, Please try again')
                  return redirect(reverse('gridapp:index'))
        except IntegrityError:
             messages.error(request, 'Database error refresh and try again')
             return redirect(reverse('gridapp:index'))

    def get(self, request):
        messages.error(request, 'Invalid request type')
        return redirect(reverse('gridapp:index'))    
        

@login_required
def confirmslot(request):
  if(request.method=="POST"):
    print(str(request.POST))
    reservation_id=int(request.POST["rid"])
    payment= int(float(request.POST["amount"]))
    try:
      current_reservation=Reservations.objects.get(reservation_id=reservation_id)
      print(current_reservation)
      current_reservation.confirmation=True;
      current_reservation.payment=payment
      current_reservation.save()
      return redirect("/bookings/mybookings")
    except Reservations.DoesNotExist:
      messages.warning(request, "Booking timed out, please try again")  
      return redirect(reverse('gridapp:index'))
  else:    
    messages.error(request, 'Invalid request type')
    return redirect(reverse('gridapp:index'))


@login_required
def bookedslots(request):
  if(request.method=="GET"):
    current_time=datetime.now()
    current_time=current_time.astimezone(pytz.utc)
    print("current time",current_time)
    current_user=request.user
    user_reservations=Reservations.objects.filter(user_id=current_user.id)
    ongoing_reservations=user_reservations.add_engaged().filter(start_time__lt=current_time,end_time__gt=current_time).values(
        'reservation_id','slot_id','start_time','end_time','booking_time','engaged')
    past_reservations=user_reservations.filter(end_time__lt=current_time)
    future_reservations=user_reservations.filter(start_time__gt=current_time)
    print(user_reservations)
    return render(request, "bookapp/userbookings.html",{"past":past_reservations,
        "future":future_reservations,"current":ongoing_reservations})
  else:
    messages.error(request, 'Invalid request type')
    return redirect(reverse('gridapp:index'))

@login_required
def cancelslot(request):
  if(request.method=="POST"):
    current_time=datetime.now()
    current_time=current_time.astimezone(pytz.utc)
    current_user=request.user;
    reservation_id=int(request.POST["reservation_id"]);
    print("reservation_id", reservation_id);
    res_obj = Reservations.objects.get(reservation_id=reservation_id)
    if res_obj.end_time < current_time:
        return JsonResponse({"status":5})  
    slot_query=SlotsCache.objects.filter(reservation_id=reservation_id, slot_id__occupied=True)
    if not slot_query:
      try:
        with transaction.atomic():
          res_obj.delete()
          current_reservation_cache=SlotsCache.objects.filter(reservation_id=reservation_id).update()
        return JsonResponse({"status":1,})
      except Exception as e:
        print(str(e))
      return JsonResponse({"status":2})   
    else:
      return JsonResponse({"status":3})  
  else:
    return JsonResponse({"status":4})               



