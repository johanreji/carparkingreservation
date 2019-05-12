from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from gridapp import views

app_name="gridapp"
urlpatterns = [
      url(r'^getslots/(?P<restype>\w+)/', views.getslots, name='getslots'),
      url(r'^scan/', views.qrscan, name='qrscan'),
      url(r'^getdata/', views.getdata, name='getdata'),
      url(r'^$', views.getslots, {'restype': 'html'}, name='index'),

]

