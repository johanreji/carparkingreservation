from django.conf.urls import url
from django.conf.urls import include

from django.contrib import admin
from bookapp import views

app_name = "bookapp"

urlpatterns = [
  #      url(r'registerform', views.registerform, name='registerform'),
	 # url(r'register', views.register, name='register'),
	 # url(r'signup', views.signup, name='signup'),
	 # url(r'login', views.login, name='login'),
	 # url(r'logout', views.logout, name='logout'),
	 url(r'search/$', views.searchslots, name='searchslots'),
	 url(r'book/$', views.Bookslot.as_view(), name='bookslot'),
	 url(r'confirm/$', views.confirmslot, name='confirmslot'),
	 url(r'mybookings/$', views.bookedslots, name='bookedslots'),

	 

]
