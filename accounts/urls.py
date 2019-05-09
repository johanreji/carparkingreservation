from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from accounts import views
from django.contrib.auth import views as auth_views

app_name="accounts"
urlpatterns = [
       url('^signup/$', views.signup, name='signup'),
       url('^login/$' , views.loginuser, name='login'),
       url('^logout/$' , views.logoutuser, name='logout'),
       url('^profile/$', views.profile, name='profile'),
       
    
]

