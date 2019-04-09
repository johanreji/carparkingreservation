from django.conf.urls import url
from django.conf.urls import include

from django.contrib import admin
from registerapp import views

urlpatterns = [
       url(r'registerform', views.registerform, name='registerform'),
	 url(r'register', views.register, name='register'),
	 url(r'signup', views.signup, name='signup'),
	 url(r'login', views.login, name='login'),
	 url(r'logout', views.logout, name='logout'),
	 url(r'bookings', views.bookings, name='bookings'),

	 

]
