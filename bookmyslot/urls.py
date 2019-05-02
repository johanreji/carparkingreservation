
"""bookmyslot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin

from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'accounts/', include('accounts.urls')),
    url(r'accounts/', include('django.contrib.auth.urls')),
    #url(r'^', include('gridapp.urls')),
    url(r'grid/', include('gridapp.urls')),
 url(r'getdata/', include('gridapp.urls')),
   
    url(r'^admin/', admin.site.urls),
     url(r'registerform/',  include('registerapp.urls')),
    url(r'register/',  include('registerapp.urls')),
    url(r'signup/',  include('registerapp.urls')),
    url(r'login/',  include('registerapp.urls')),
    url(r'logout/',  include('registerapp.urls')),
    url(r'bookings/',  include('registerapp.urls')),
    
 
]

# hello(repeat=10,repeat_until=None)
