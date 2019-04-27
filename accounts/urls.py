from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from accounts import views


urlpatterns = [
      url(r'register', views.register, name='register'),
    
]

