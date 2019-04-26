# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.http import JsonResponse
import time
import os
import mysql.connector
import itertools
import json



CNNDELAY = 2

@csrf_exempt
def getdata(request):
 if(request.method=="POST"):
  data=request.POST["val"]
  ts=request.POST["ts"]
  #ts=ts.encode('ascii')
  ts=float(ts)
  cnnts=datetime.fromtimestamp(ts / 1e3)
  print(cnnts)
  details=json.loads(data)
  detailsplain={}
  db = mysql.connector.connect(user='django', password='virurohan', 
                                database='bookmyslot')
  cursor = db.cursor()
  #cur= db.cursor()
  cursor.execute('SELECT SlotID,occupied FROM Slots')
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
    q="""UPDATE Slots SET occupied = %s, CNNFlag = %s, CNNTimestamp = %s WHERE SlotID = %s ;"""
    d=(1,1,cnnts,datatuple[i][0])
    cursor.execute(q,d) 
   elif(datatuple[i][1]=="False" and result[i][1]==1):
    print("change to free : ", datatuple[i][0])
    q="""UPDATE Slots SET occupied = %s, CNNFlag = %s, CNNTimestamp = %s WHERE SlotID = %s ;"""
    d=(0,1,cnnts,datatuple[i][0])
    cursor.execute(q,d) 
   else:
    print("no change")
  db.commit()
  db.close()
  return HttpResponse("succs")


@csrf_exempt
def grid(request):    
 db = mysql.connector.connect(user='django', password='virurohan', 
                                database='bookmyslot')
 cursor = db.cursor(buffered=True)
 cur=db.cursor(buffered=True)
 cursor.execute('SELECT SlotID,occupied FROM Slots')
 #curr_time=time.time()
 curr_time = datetime.utcnow() + timedelta(hours=5.5)
 curr_time=curr_time.strftime('%Y-%m-%d %H:%M:%S')
 q = "SELECT SlotID, StartTime, EndTime FROM ReservedSlots WHERE EndTime > %s"
 d=(curr_time,)
 cur.execute(q,d)

 result = cursor.fetchall()
 cursor.close()
 res=cur.fetchall()
 cur.close()
 
 
 if(request.method=="POST"):

  print("post data", request.POST)
  st=request.POST["st"]
  st1=st
  print(st)
  et=request.POST["et"]
  et1=et
  start_date_view=request.POST["dst"]
  end_date_view=request.POST["det"]
  start_timestamp=start_date_view + ' ' + st
  start_timestamp=datetime.strptime(start_timestamp,"%Y-%m-%d %H:%M")
  end_timestamp=end_date_view + ' ' + et
  end_timestamp=datetime.strptime(end_timestamp,"%Y-%m-%d %H:%M")
  # print(et)
  # print("sts", start_timestamp)
  # print("sts type", type(start_timestamp))
  stat=request.session.setdefault('loggedin',0)
  name=request.session.setdefault('name',"user")
  if True:
   # print("res is : ", res)
   # dst=res[1][1]
   # print("dst",dst)
   # det=res[1][2].time()
   # print("det",det)
   o=()
   a=()
   r=()
# if(st>dst and st<dst ):
#   print("success")
   for item in result:
    a=a+(item[0],)
   for item in res:

    if((start_timestamp>=item[1] and start_timestamp<=item[2]) or (end_timestamp>=item[1] and end_timestamp<=item[2])):
     o=o+(item[0],)
     
    
   a=tuple(set(a))
   o=tuple(set(o))
   print("aaa",a)
   print("ooo",o)
   for i in a:
    if( i in o):
     r=r+((i,1),)
    else:
     r=r+((i,0),) 
    print("avaliable tuples: ", r)
   if r: 
    return render(request, "grid.html", {"result" : r , "res":res, "dst":start_date_view, "det":end_date_view, "st":st1,"et":et1,"stat":stat,"name":name})
   else: 
    print("no bookings")
    return render(request, "grid.html", {"result" : result , "res":r, "dst":start_date_view, "det":end_date_view, "st":st1,"et":et1,"stat":stat,"name":name})


 elif request.method=="GET":
  try:
    status=request.GET["status"]
    sta=request.GET.get('sta',0 )
    
    stat=request.session.setdefault('loggedin',0)
    griddict={}
    for i in result:
      griddict[i[0]]=i[1]
    return JsonResponse(griddict) 
  except Exception:

      sta=request.GET.get('sta',0 )
      
      stat=request.session.setdefault('loggedin',0)
      name=request.session.setdefault('name',"user")
      print(result)
      if res:
        return render(request, "grid.html", {"result" : result , "res":res,"sta":sta,"stat":stat,"name":name})
      else:
        return render(request, "grid.html", {"result" : result,"sta":sta,"stat":stat,"name":name})
 else:
  return render(request, "grid.html", {"result" : result , "res":res})

@csrf_exempt
def scan(request):
 resdict={}
 try:
  # stat=request.session.setdefault('loggedin',0)
  # name=request.session.setdefault('name',"user")
  user_id=request.session["customerid"]
 except Exception:
  resdict["status"]=-1
  return JsonResponse(resdict)  
 else:  
  if(request.method=="POST"):
   received_json_data=json.loads(request.body)
   print(received_json_data)
   print(type(received_json_data))
   curr_slot=received_json_data["slot_id"]
   print(curr_slot)
   print(user_id)
   db = mysql.connector.connect(user='django', password='virurohan', 
                                 database='bookmyslot')
   cursor = db.cursor()
   print(datetime.now())
   curr_time = datetime.utcnow() + timedelta(hours=5.5)
   curr_time=curr_time.strftime('%Y-%m-%d %H:%M:%S')
   print(curr_time)
   q = "SELECT SlotID, StartTime, EndTime, ReservedSlots.ReservationID FROM Reservation INNER JOIN ReservedSlots WHERE Reservation.ReservationID \
   = ReservedSlots.ReservationID AND Reservation.CustomerID = %s AND StartTime < %s AND EndTime > %s AND SlotID = %s"
   d=(user_id, curr_time, curr_time, curr_slot)
   cursor.execute(q,d)
   result = cursor.fetchall()
   if result:
    reservation_id = result[0][3]
    endtime = result[0][2]
    resdict["status"]=1
    q2 = "SELECT occupied, CNNTimestamp, ReservationID, CNNFlag FROM Slots WHERE SlotID = %s"
    d2 = (curr_slot,)
    cursor.execute(q2, d2)
    slot_details = cursor.fetchall()
    print(slot_details)
    car_check_flag = True
    while(True):
     if(slot_details[0][0] == 1):
     	if(slot_details[0][2]):
     		resdict["status"] = 3
     		return JsonResponse(resdict)
     	print("check if")
     	q3 = "UPDATE Slots SET ReservationID = %s, EndTime = %s, CNNFlag = %s WHERE SlotID = %s"
     	d3 = (reservation_id, endtime,0, curr_slot)
     	cursor.execute(q3, d3)
     	cursor.close()
     	db.commit()
     	db.close()
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
  		
