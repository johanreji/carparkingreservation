from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
from master import views

app_name='master'

urlpatterns = [
       url(r'master/', views.master, name='master'),
       url(r'addslot/', views.addslot, name='addslot'),
       url(r'cropper/', views.cropper, name='cropper'),
       url(r'getslots/', views.sendSlotDims, name='getslots'),
       url(r'addarea/(?P<reqtype>\w+)', views.addarea, name='addarea'),
       url(r'genslots/', views.generateSlots, name='genslots'),
       

]




