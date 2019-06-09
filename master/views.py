from __future__ import unicode_literals
import os
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from datetime import datetime, timedelta
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from .models import ParkingAreas, SlotDims, RenderDims
from gridapp.models import Slots, SlotsCache
from bookapp.models import Reservations, PenaltyReservations
from tempfile import NamedTemporaryFile
from PIL import Image
from django.db.models import F, Sum, FloatField, Avg, Min, Max
import json
import pytz
from .getImage import getImage
from django.core.files import File
from urllib.request import urlopen
import subprocess, signal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import UserPassesTestMixin
import psutil


cache.set('cnnstatus', False)
cache.set('pid', None)

def getfilename():
  try:
    id=ParkingAreas.objects.latest('area_id')
    return 'areas/{0}.jpg'.format(str(id))
  except Exception:
    id=0
    return 'areas/{0}.jpg'.format(str(id))  

@csrf_exempt
@staff_member_required
def master(request):
  result = None
  query2 = ParkingAreas.objects.order_by('-area_id')
  if(query2):
    query2=query2[0]
    area_id=query2.area_id
    query=SlotDims.objects.filter(area_id=area_id)
    slotimg = query2.area_image
    print(slotimg.url)
    area=(query2.width, query2.height)
    print(result)
    # print("area", area)
    # print("url, ", slotimg.url)
    return render(request, "master/master.html", {"result" : query ,"area":area, "slotimg":slotimg, "area_id":area_id})
  else:
    return render(request, "master/master.html", {"result" : None ,"area":(0,0),"slotimg":None, "area_id":None})

    
  #if request.method == 'POST' and request.FILES['myfile']:
  # myfile = request.FILES['myfile']
  # fs = FileSystemStorage()
  # print("myfile",myfile.name)
  # fs.delete("bg.jpg")
  # filename = fs.save("bg.jpg", myfile)
  # print("fn",filename)
  # uploaded_file_url = fs.url(filename)
  # return render(request, 'master.html', {
  #           'uploaded_file_url': uploaded_file_url
  #       })

@csrf_exempt
def sendSlotDims(request):
  if(request.method=="GET"):
    query2 = ParkingAreas.objects.order_by('-area_id')
    if(query2):
      query2=query2[0]
      area_id=query2.area_id
      query=list(SlotDims.objects.filter(area_id=area_id).only('slot_id','x_left', 'y_left', 'width','height').values())
      return JsonResponse({"data":query})
  return JsonResponse({"status":-1})    


@csrf_exempt
@staff_member_required
def cropper(request):
  return render(request,"master/cropper.html")

@csrf_exempt
@staff_member_required
def addslot(request):
  if(request.method=="POST"):
    aid=request.POST["aid"]
    sid=request.POST["slotid"]
    x=int(float(request.POST["x"]))
    y=int(float(request.POST["y"]))
    width=int(float(request.POST["width"]))
    height=int(float(request.POST["height"]))
    row=int(request.POST["row"])
    column=int(request.POST["column"])
    slotdims_obj=SlotDims.objects.create(area_id=ParkingAreas.objects.get(area_id=aid), x_left=x, y_left=y, width=width,
     height=height, row=row, column=column)
    slotdims_obj.save()
    return JsonResponse({"status":True, "slot_id":slotdims_obj.pk, "x":x, "y":y, "width":width, "height":height, "row":row})
  else:
    return JsonResponse({"status":False})

 


@csrf_exempt
@staff_member_required
def generateSlots(request):
    query2 = ParkingAreas.objects.order_by('-area_id')
    if(query2):
      recentobj=query2[0]
      area=(recentobj.width, recentobj.height)
      area_id=recentobj.area_id
      slotimg=recentobj.area_image
      query=SlotDims.objects.filter(area_id=area_id).only("slot_id")
      if(query):
        query2.update(is_active=False)
        recentobj.is_active=True
        recentobj.save()
        PenaltyReservations.objects.all().delete()
        Reservations.objects.all().delete()
        SlotsCache.objects.all().delete()
        Slots.objects.all().delete()
        RenderDims.objects.all().delete()
        current_datetime=datetime.now()
        current_datetime=current_datetime.astimezone(pytz.utc)
        numrows = recentobj.row_count
        numcols = recentobj.column_count
        rowdict= {}
        columndict = {}
        maxthreshold=700
        currthreshold = area[1]
        columnthreshold = area[0]
        print("columnthreshold", columnthreshold)
        maxcolthreshold = 500

        for i in range(1, numrows+1):
          rowaverage = query.filter(row=i).annotate(maxcount=Max('y_left'), mincount=Min('y_left'))
          currpos = (rowaverage[0].maxcount + rowaverage[0].mincount)/2
          rowdict[i]= (currpos/currthreshold)*maxthreshold

        for i in range(1, numcols+1):
          columnaverage = query.filter(column=i).annotate(maxcount=Max('x_left'), mincount=Min('x_left'))
          currpos = (columnaverage[0].maxcount + columnaverage[0].mincount)/2  
          print("currposs ", currpos)
          columndict[i]=(currpos/columnthreshold)*maxcolthreshold
          print("columdicti ",columndict[i])
        count = 1
        for i in query:
          s=Slots.objects.create(slot_id=count, occupied=False, cnn_timestamp=current_datetime)
          s1=SlotsCache.objects.create(slot_id=s, reservation_id=None, end_time=None)
          s2=RenderDims.objects.create(slot_id=count, x_left=rowdict[i.row], y_left=columndict[i.column])
          count += 1
        message="Slots are generated please view home page"
        query.update(updated=True)
        if(cache.get('cnnstatus')==True):
          os.kill(cache.get('pid'), signal.SIGKILL)
          proc=subprocess.Popen(["cv/bin/python", "cnn/pipeline.py"])
          cache.set('pid', proc.pid)
        return render(request, "master/master.html", {"result" : query ,"message":message,"area":area, "slotimg":slotimg,"area_id":area_id})  
      else:
        message="Please crop some slots"
        return render(request, "master/master.html", {"result" : None ,"area":area,"slotimg":slotimg,"message":message})
    else:
      message="Please upload area and crop slots"
      return render(request, "master/master.html", {"result" : None ,"area":None,message:"message"})

@csrf_exempt
@staff_member_required
def addarea(request, reqtype="html"):
  if(request.method=="POST" and reqtype=="program"):
    print("request:, ", str(request.FILES["media"]))
    print("postdata", str(request.POST))
    new_area = ParkingAreas.objects.create()
    new_area.area_image = request.FILES["media"]
    try:
      area_name=request.POST["area_name"]
      rows=request.POST["rows"]
      new_area.area_name=area_name
      new_area.row_count=rows
      new_area.save()
      return JsonResponse({"status":1})
    except Exception:
      area_name=None
      rows=None
      new_area.area_name=area_name
      new_area.row_count=rows
      new_area.save()
      return JsonResponse({"status":2})
  elif(request.method=="POST" and reqtype=="html"):
    img=request.FILES["myfile"]
    name=request.POST["area_name"]
    rows=request.POST["rows"]
    new_area = ParkingAreas.objects.create(area_image=img, area_name=name, row_count=rows)
    new_area.save()
    area=[(new_area.height, new_area.width)]
    return render(request, "master/master.html",{"area":area, "slotimg":new_area.area_image, "area_id":new_area.area_id})
  else:  
    return render(request, "master/master.html")
    
 
  # width=request.POST["width"]
  # height=request.POST["height"]
 
  # print("width",width)
  # print("height",height)
  # db = MySQLdb.connect(user='django', db='bookmyslot', passwd='virurohan', host='127.0.0.1')
  # cursor = db.cursor()
  # cursor.execute("delete from area")
  # cursor.execute("delete from Slots")
  # q="""insert into area (width,height) values ( %s, %s );"""
  # d=(width,height)
  # cursor.execute(q,d)
  # cursor.execute('SELECT SlotID,occupied,x,y,width,height FROM Slots')
  # result = cursor.fetchall()
  # cursor.execute('SELECT width,height FROM area')
  # area=cursor.fetchone()
  # db.commit()
  # db.close()
#   return render(request, "master.html", {"result" : result ,"area":area}) 


@csrf_exempt
@staff_member_required
def fetch(request):
  filepath_prefix="/media/"
  if(request.method=="GET"):
    filepath=filepath_prefix + getfilename()
    print("filepath is ", filepath)
    flag=getImage(filepath.strip('/'), 0)
    cache_breaker=datetime.now()  # to force removal of cached image
    return JsonResponse({"status":flag,"url":filepath,"cache_breaker":f"?{cache_breaker}"})
  return JsonResponse({"status":False})

@csrf_exempt
@staff_member_required
def save(request):
  filepath="frame.jpg"
  if(request.method=="POST"):
    print(str(request.POST))
    img=request.POST["url"]
    name=request.POST["area_name"]
    rows=request.POST["rows"]
    columns=request.POST["columns"]
    new_area = ParkingAreas.objects.create(area_name=name,area_image=img.replace('/media/', ''), row_count=rows, column_count=columns)
    new_area.save()
    return JsonResponse({"url":new_area.area_image.url,"status":True,"aid":new_area.pk, "width":new_area.width, "height":new_area.height})
  else:
   return JsonResponse({"status":False})

@csrf_exempt
@staff_member_required
def removeslot(request):
  if(request.method=="POST"):
    slot_id = int(request.POST["slot_id"])
    slotdimobj = SlotDims.objects.get(slot_id=slot_id)
    if(slotdimobj.updated==True):
    	Slots.objects.get(slot_id=slot_id).delete()
    slotdimobj.delete()	
    return JsonResponse({"status":True}) 
  else:
    return JsonResponse({"status":False})   


class startcnn(LoginRequiredMixin, UserPassesTestMixin,View):

    def test_func(self):
        return self.request.user.is_admin
    def get(self, request):
      if(request.GET["op"]=="startcnn"):  
        pid=None
        if(cache.get('cnnstatus')==False):
          print("check flow")
          proc=subprocess.Popen(["cv/bin/python3", "cnn/pipeline.py"])
          print(proc)
          print(proc.pid)
          cache.set('cnnstatus', True)
          cache.set('pid', proc.pid)
          pid=proc.pid
        return JsonResponse({"status":1, "pid":pid, "message":"CNN camera scanning started"}) 
      elif(request.GET["op"]=="stopcnn"):
        if(cache.get('cnnstatus')==True):
          info=os.kill(cache.get('pid'), signal.SIGKILL)
          cache.set('cnnstatus', False)
          
        return JsonResponse({"status":2, "info":None, "message":"CNN camera scanning stopped"})
      else:
        if cache.get('pid') and cache.get('cnnstatus'):
          return JsonResponse({"status":3, "message":"CNN camera scanning currently running"})
        return JsonResponse({"status":4, "message":"CNN camera scanning is not running"})      
  

    
