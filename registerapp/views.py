# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import datetime
from django.shortcuts import redirect
import mysql.connector
from django.db import transaction
# BookingQueue = queue.Queue(10)
# Create your views here.
@csrf_exempt
def registerform(request):
 if(request.method=="POST"):
  stat=request.session.setdefault('loggedin',0)
  name=request.session.setdefault('name',"user")
  slot=request.POST["slotselected"]
  st=request.POST["stime"]
  et=request.POST["etime"]
  start_date=request.POST["sdate"]
  end_date = request.POST["edate"]
  start_timestamp = start_date + ' ' + st
  start_timestamp = datetime.datetime.strptime(start_timestamp,'%Y-%m-%d %H:%M') 
  end_timestamp = end_date + ' ' + et
  end_timestamp = datetime.datetime.strptime(end_timestamp,'%Y-%m-%d %H:%M') 
  diff=abs(start_timestamp - end_timestamp)
  total_mins = (diff.days*1440 + diff.seconds/60)
  amt=total_mins/60*10
  amt=round(amt,2)
  print("start_timestamp", start_timestamp)
  db = mysql.connector.connect(user='django', password='virurohan', 
                                database='bookmyslot')
  cursor = db.cursor()
  user_id=request.session["customerid"]
  q="""INSERT INTO Reservation (CustomerID,ReservationStatus) VALUES (%s , %s );"""
  d=(user_id,0)
  cursor.execute(q, d)
  rid=cursor.lastrowid
  # cursor.execute(q, d)
  # rid=cursor.fetchone()
  # rid=rid[0]
  print("rid ", rid)
  q="""SELECT SlotID  FROM ReservedSlots WHERE StartTime = %s AND EndTime = %s AND SlotID =%s ;"""
  d=(start_timestamp,end_timestamp, slot)
  cursor.execute(q,d)
  result = cursor.fetchall()
  if(result):
    response = redirect('/grid/grid')
    return response
  q="""INSERT into ReservedSlots (ReservationID, SlotID, StartTime, EndTime) VALUES (%s , %s , %s , %s);"""
  d=(rid,slot,start_timestamp,end_timestamp)
  cursor.execute(q,d)
  db.commit()
  cursor.close()
  db.close()
  print("session test",name)
  return render(request, "signup.html",{"slotselected":slot,"st":st,"et":et,"amt":amt,
    "stat":stat, "dst":start_timestamp, "det": end_timestamp, "name":name, "rid":rid})



@csrf_exempt
def register(request):
 print("post data", request.POST)
 sustatus=0
 db = mysql.connector.connect(user='django', password='virurohan', 
                                database='bookmyslot')
 cursor = db.cursor()
 name=request.session["name"]
 customer_id=request.session["customerid"]
 reservation_id=request.POST["rid"]
 q="""UPDATE Reservation SET ReservationStatus = %s WHERE ReservationID=%s ;"""
 d=(1,reservation_id)
 cursor.execute(q,d)
 count = cursor.rowcount
 cursor.close()
 db.commit()
 db.close()
 stat=request.session.setdefault('loggedin',0)
 name=request.session.setdefault('name',"user")
 sustatus=1
 if count > 0:
  response = redirect('/bookings/bookings')
  return response
 else:
  response = redirect('/grid/grid' , {'alert':"Payment session timed out please book again"}) 
  return response
 # , {"sustatus" : sustatus,"sistatus" : 0 }
 # return render(request, "result.html",{"slot":slot,"st":st,"et":et,"name":name,"rid":rid[0],"stat":stat})



@csrf_exempt
def signup(request):
 db = mysql.connector.connect(user='django', password='virurohan', 
                            database='bookmyslot')
 cursor = db.cursor()
 name=request.POST["name"]
 email=request.POST["email"]
 phonenumber=request.POST["phonenumber"]
 vehiclenumber=request.POST["vehiclenumber"]
 password=request.POST["password"]
 print(email)
 q="insert into Customer (Name,MobileNumber,VehicleNumber,email,password) values (%s , %s ,%s, %s, %s );"
 d=(name,phonenumber,vehiclenumber,email,password)
 # q="""SELECT SlotID  FROM ReservedSlots ;"""
 
 # cursor.execute(q)
 # result = cursor.fetchall()
 # print(result)
 cursor.execute(q,d)
 try:
    transaction.commit_unless_managed()
 except:
    response = redirect('/grid/grid?sta=1')
 else:
    response = redirect('/grid/grid?sta=2')
 db.commit()
 db.close()
 
 return response

@csrf_exempt
def login(request):
 db = mysql.connector.connect(user='django', password='virurohan', 
                                database='bookmyslot')
 cursor = db.cursor()
 email=request.POST["email"]
 print(email)

 password=request.POST["password"]
 print(password)
 q="select password,name,CustomerID from Customer where email = %s ;"
 d=(email,)
 cursor.execute(q,d)
 result=cursor.fetchone()
 print(result)

 try:
    transaction.commit_unless_managed()
 except:
    if(result[0]==password):
      request.session['loggedin'] = 1
      request.session['name'] = result[1]
      request.session['customerid'] = result[2]
      response = redirect('/grid/grid')
    else:
      request.session['loggedin'] = 0
      response = redirect('/grid/grid')

 else:
    response = redirect('/grid/grid?stat=2')
 db.commit()
 db.close()


 return response


@csrf_exempt
def logout(request):
  del request.session['loggedin']
  del request.session['name']
  del request.session['customerid']
  response = redirect('/grid/grid')
  return response

@csrf_exempt
def bookings(request):
 sustatus=0
 stat=request.session.setdefault('loggedin',0)
 name=request.session.setdefault('name',"user")
 db = mysql.connector.connect(user='django', password='virurohan', 
                                database='bookmyslot')
 cursor = db.cursor()
 try:
  cid=request.session['customerid']
 except Exception:
  response = redirect('/grid/grid') 
  return response
 else: 
  print(type(cid))
  q="""SELECT Reservation.ReservationID,SlotID,StartTime,EndTime  FROM Reservation inner join ReservedSlots ON Reservation.ReservationID = ReservedSlots.ReservationID WHERE CustomerID = %s ;"""
  d=(cid,)
  cursor.execute(q,d)
  result = cursor.fetchall()
  print("kittiyee",result)
  cursor.close()
  db.commit()
  db.close()
  return render(request, "result.html",{"result":result,"name":name,"stat":stat})

