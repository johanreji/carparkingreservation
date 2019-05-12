from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from datetime import datetime, timedelta
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from .models import ParkingAreas, SlotDims
from gridapp.models import Slots, SlotsCache
from bookapp.models import Reservations, PenaltyReservations
from PIL import Image
from django.db.models import Sum, Avg
import json
import pytz
# BookingQueue = queue.Queue(10)
# Create your views here.
@csrf_exempt
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
    print("area", area)
    print("url, ", slotimg.url)
    return render(request, "master/master.html", {"result" : query ,"area":area, "slotimg":slotimg, "area_id":area_id})
  else:
    return render(request, "master/master.html", {"result" : None ,"area":None,})

    
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
def cropper(request):
  return render(request,"master/cropper.html")

@csrf_exempt
def addslot(request):
  if(request.method=="POST"):
    aid=request.POST["aid"]
    sid=request.POST["slotid"]
    x=int(float(request.POST["x"]))
    y=int(float(request.POST["y"]))
    width=int(float(request.POST["width"]))
    height=int(float(request.POST["height"]))
    row=int(request.POST["row"])
    slotdims_obj=SlotDims.objects.create(area_id=ParkingAreas.objects.get(area_id=aid), x_left=x, y_left=y, width=width,
     height=height, row=row)
    slotdims_obj.save()
    query2 = ParkingAreas.objects.order_by('-area_id')
    query2=query2[0]
    slotimg = query2.area_image
    area_id = query2.area_id
    query = SlotDims.objects.filter(area_id=area_id)
    area=(query2.width, query2.height)
    return render(request, "master/master.html", {"result" : query ,"area":area, "slotimg":slotimg,"area_id":area_id})
  else:
    return JsonResponse({"status:"-1})

 


@csrf_exempt
def generateSlots(request):
    query2 = ParkingAreas.objects.order_by('-area_id')
    if(query2):
      query2=query2[0]
      area=(query2.width, query2.height)
      area_id=query2.area_id
      slotimg=query2.area_image
      query=SlotDims.objects.filter(area_id=area_id).only("slot_id")
      if(query):
        PenaltyReservations.objects.all().delete()
        Reservations.objects.all().delete()
        SlotsCache.objects.all().delete()
        Slots.objects.all().delete()
        current_datetime=datetime.now()
        current_datetime=current_datetime.astimezone(pytz.utc)
        for i in query:
          s=Slots.objects.create(slot_id=i.slot_id, occupied=False, cnn_timestamp=current_datetime)
          s1=SlotsCache.objects.create(slot_id=s, reservation_id=None, end_time=None)
        message="Slots are generated please view home page"
        return render(request, "master/master.html", {"result" : query ,"message":message,"area":area, "slotimg":slotimg,"area_id":area_id})  
      else:
        message="Please crop some slots"
        return render(request, "master/master.html", {"result" : query ,"area":area,"slotimg":slotimg,"message":message})
    else:
      message="Please upload area and crop slots"
      return render(request, "master/master.html", {"result" : query ,"area":None,message:"message"})

@csrf_exempt
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