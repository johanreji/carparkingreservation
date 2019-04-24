# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.http import JsonResponse


import MySQLdb
import itertools
import json


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
  db = MySQLdb.connect(user='django', db='bookmyslot', passwd='virurohan', host='127.0.0.1')
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
 db = MySQLdb.connect(user='django', db='bookmyslot', passwd='virurohan', host='127.0.0.1')
 cursor = db.cursor()
 cur=db.cursor()
 cursor.execute('SELECT SlotID,occupied,x,y,width,height FROM Slots')
 cur.execute('SELECT SlotID, StartTime, EndTime FROM ReservedSlots')
 result = cursor.fetchall()
 print("sivane--",result)
 res=cur.fetchall()
 db.close()
 
 if(request.method=="POST"):
  st=request.POST["st"]
  timest=datetime.strptime(st,'%H:%M').time()
  print(st)
 # print(res[0][1])
  et=request.POST["et"]
  timeet=datetime.strptime(et,'%H:%M').time()
  print(et)
  stat=request.session.setdefault('loggedin',0)
  name=request.session.setdefault('name',"user")
  if res:

   o=()
   a=()
   r=()
# if(st>dst and st<dst ):
#   print("success")
   for item in result:
    a=a+(item[0],)
   for item in res:

    if((timest>item[1].time() and timest<item[2].time()) or (timeet>item[1].time() and timeet<item[2].time())):
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
    print(r)

   return render(request, "grid.html", {"result" : r , "res":res,"st":st,"et":et,"stat":stat,"name":name})
  else: 
   r=()
   return render(request, "grid.html", {"result" : result , "res":r,"st":st,"et":et,"stat":stat,"name":name})


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



