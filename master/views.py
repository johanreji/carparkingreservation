from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
import MySQLdb
from django.db import transaction
# BookingQueue = queue.Queue(10)
# Create your views here.
@csrf_exempt
def master(request):
 db = MySQLdb.connect(user='django', db='bookmyslot', passwd='virurohan', host='127.0.0.1')
 cursor = db.cursor()
 cursor.execute('SELECT SlotID,occupied,x,y,width,height FROM Slots')
 result = cursor.fetchall()
 cursor.execute('SELECT width,height FROM area')
 area=cursor.fetchone()
 if request.method == 'POST' and request.FILES['myfile']:
  myfile = request.FILES['myfile']
  fs = FileSystemStorage()
  print("myfile",myfile.name)
  fs.delete("bg.jpg")
  filename = fs.save("bg.jpg", myfile)
  print("fn",filename)
  uploaded_file_url = fs.url(filename)
  # return render(request, 'master.html', {
  #           'uploaded_file_url': uploaded_file_url
  #       })

  

 return render(request, "master.html", {"result" : result ,"area":area})

@csrf_exempt
def cropper(request):
 return render(request,"cropper.html")

@csrf_exempt
def addslot(request):
 sid=request.POST["slotid"]
 x=request.POST["x"]
 y=request.POST["y"]
 width=request.POST["width"]
 height=request.POST["height"]
 print("sid",sid)
 print("x",x)
 print("y",y)
 print("width",width)
 print("height",height)
 db = MySQLdb.connect(user='django', db='bookmyslot', passwd='virurohan', host='127.0.0.1')
 cursor = db.cursor()
 
 q="""insert into Slots (SlotID,occupied,x,y,width,height) values (%s,%s , %s ,%s, %s, %s );"""
 d=(sid,0,x,y,width,height)
 cursor.execute(q,d)
 cursor.execute('SELECT SlotID,occupied,x,y,width,height FROM Slots')
 result = cursor.fetchall()
 cursor.execute('SELECT width,height FROM area')
 area=cursor.fetchone()
 db.commit()
 db.close()
 return render(request, "master.html", {"result" : result ,"area":area})


@csrf_exempt
def addarea(request):

 width=request.POST["width"]
 height=request.POST["height"]

 print("width",width)
 print("height",height)
 db = MySQLdb.connect(user='django', db='bookmyslot', passwd='virurohan', host='127.0.0.1')
 cursor = db.cursor()
 cursor.execute("delete from area")
 cursor.execute("delete from Slots")
 q="""insert into area (width,height) values ( %s, %s );"""
 d=(width,height)
 cursor.execute(q,d)
 cursor.execute('SELECT SlotID,occupied,x,y,width,height FROM Slots')
 result = cursor.fetchall()
 cursor.execute('SELECT width,height FROM area')
 area=cursor.fetchone()
 db.commit()
 db.close()
 return render(request, "master.html", {"result" : result ,"area":area})