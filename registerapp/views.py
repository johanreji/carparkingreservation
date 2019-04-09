# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import datetime
from django.shortcuts import redirect
import MySQLdb
from django.db import transaction
# BookingQueue = queue.Queue(10)
# Create your views here.
def registerform(request):
 if(request.method=="GET"):
  stat=request.session.setdefault('loggedin',0)
  name=request.session.setdefault('name',"user")
  ss=request.GET["slotselected"]
  st=request.GET["stime"]
  dst = datetime.datetime.strptime(st, '%H:%M')
  et=request.GET["etime"]
  det = datetime.datetime.strptime(et, '%H:%M')
  diff=det-dst
  total_mins = (diff.days*1440 + diff.seconds/60)
  amt=total_mins/60*10
  amt=round(amt,2)
  print("session test",name)
  return render(request, "signup.html",{"slotselected":ss,"st":st,"et":et,"amt":amt,"stat":stat,"name":name})



@csrf_exempt
def register(request):
 sustatus=0
 db = MySQLdb.connect(user='django', db='bookmyslot', passwd='virurohan', host='127.0.0.1')
 cursor = db.cursor()
 # e=request.POST["email"]
 # p=request.POST["psw"]
   
 # q="""insert into accountdetail (email,password) values (%s , %s );"""
 # d=(e,p)
 # cursor.execute(q,d)
 st=request.POST["st"]
 dst = datetime.datetime.strptime(st, '%H:%M')
 dst=dst.replace(year=2018)
 strst=dst.strftime('%Y-%m-%d %H:%M:%S')
 et=request.POST["et"]
 det = datetime.datetime.strptime(et, '%H:%M')
 det=det.replace(year=2018)
 stret=det.strftime('%Y-%m-%d %H:%M:%S')
 slot=request.POST["slot"]
 q="""SELECT SlotID  FROM ReservedSlots WHERE StartTime = %s AND EndTime = %s ;"""
 d=(strst,stret)
 cursor.execute(q,d)
 result = cursor.fetchone()
 print(result)
 if(result):
  if(result[0]==slot):
   print("going back")
   response = redirect('/grid/grid')
   return response

 # name=request.POST["name"]
 name=request.session["name"]
 # email=request.POST["email"]
 # phonenumber=request.POST["phone"]
 # vehiclenumber=request.POST["vehiclenumber"]

 # q="""insert into Customer (Name,MobileNumber,VehicleNumber) values (%s , %s ,%s );"""
 # d=(name,phonenumber,vehiclenumber)
 # cursor.execute(q,d)
 # q="""SELECT CustomerID FROM Customer ORDER BY CustomerID DESC LIMIT 1;"""
 # cursor.execute(q)
 # cid=cursor.fetchone()
 cid=request.session["customerid"]
 print("cid moosa",cid)
 q="""insert into Reservation (CustomerID,ReservationStatus) values (%s , %s );"""
 d=(cid,1)
 cursor.execute(q,d)
 q="""SELECT ReservationID FROM Reservation ORDER BY ReservationID DESC LIMIT 1;"""
 cursor.execute(q)
 rid=cursor.fetchone()
 print(rid[0])
 q="""insert into ReservedSlots (ReservationID, SlotID, StartTime, EndTime) values (%s , %s , %s , %s);"""
 d=(rid,slot,strst,stret)
 cursor.execute(q,d)
 db.commit()
 db.close()
 stat=request.session.setdefault('loggedin',0)
 name=request.session.setdefault('name',"user")
 sustatus=1
 response = redirect('/bookings/bookings')
 return response
 # , {"sustatus" : sustatus,"sistatus" : 0 }
 # return render(request, "result.html",{"slot":slot,"st":st,"et":et,"name":name,"rid":rid[0],"stat":stat})



@csrf_exempt
def signup(request):
 db = MySQLdb.connect(user='django', db='bookmyslot', passwd='virurohan', host='127.0.0.1')
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
 db = MySQLdb.connect(user='django', db='bookmyslot', passwd='virurohan', host='127.0.0.1')
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
 db = MySQLdb.connect(user='django', db='bookmyslot', passwd='virurohan', host='127.0.0.1')
 cursor = db.cursor()
 cid=request.session['customerid']
 print(type(cid))
 q="""SELECT Reservation.ReservationID,SlotID,StartTime,EndTime  FROM Reservation inner join ReservedSlots ON Reservation.ReservationID = ReservedSlots.ReservationID WHERE CustomerID = %s ;"""
 # q="""SELECT ReservationID FROM ReservedSlots WHERE CustomerID = %s"""
 d=(cid,)

 cursor.execute(q,d)
 result = cursor.fetchall()
 print("kittiyee",result)

 db.commit()
 db.close()
 # if(result):
 #  if(result[0]==slot):
 #   print("going back")
 #   response = redirect('/grid/grid')
 #   return response

 # # name=request.POST["name"]
 # name=request.session["name"]
 # # email=request.POST["email"]
 # # phonenumber=request.POST["phone"]
 # # vehiclenumber=request.POST["vehiclenumber"]

 # # q="""insert into Customer (Name,MobileNumber,VehicleNumber) values (%s , %s ,%s );"""
 # # d=(name,phonenumber,vehiclenumber)
 # # cursor.execute(q,d)
 # # q="""SELECT CustomerID FROM Customer ORDER BY CustomerID DESC LIMIT 1;"""
 # # cursor.execute(q)
 # # cid=cursor.fetchone()
 # cid=request.session["customerid"]
 # print("cid moosa",cid)
 # q="""insert into Reservation (CustomerID,ReservationStatus) values (%s , %s );"""
 # d=(cid,1)
 # cursor.execute(q,d)
 # q="""SELECT ReservationID FROM Reservation ORDER BY ReservationID DESC LIMIT 1;"""
 # cursor.execute(q)
 # rid=cursor.fetchone()
 # print(rid[0])
 # q="""insert into ReservedSlots (ReservationID, SlotID, StartTime, EndTime) values (%s , %s , %s , %s);"""
 # d=(rid,slot,strst,stret)
 # cursor.execute(q,d)
 # db.commit()
 # db.close()
 # stat=request.session.setdefault('loggedin',0)
 # name=request.session.setdefault('name',"user")
 # sustatus=1
 # , {"sustatus" : sustatus,"sistatus" : 0 }
 return render(request, "result.html",{"result":result,"name":name,"stat":stat})
 # return render(request, "result.html")
