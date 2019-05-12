from django.conf.urls import url
from django.conf.urls import include

from django.contrib import admin
from bookapp import views

app_name = "bookapp"

urlpatterns = [
	 url(r'search/$', views.searchslots, name='searchslots'),
	 url(r'book/$', views.Bookslot.as_view(), name='bookslot'),
	 url(r'confirm/$', views.confirmslot, name='confirmslot'),
	 url(r'mybookings/$', views.bookedslots, name='bookedslots'),
	 url(r'cancel/$', views.cancelslot, name='cancelslot'),

	 

]
