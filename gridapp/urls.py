from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from gridapp import views


urlpatterns = [
      url(r'grid', views.grid, name='grid'),
      url(r'getdata', views.getdata, name='getdata'),
]
