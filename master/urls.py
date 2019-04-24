from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
from master import views

urlpatterns = [
       url(r'master', views.master, name='master'),
       url(r'addslot', views.addslot, name='addslot'),
       url(r'cropper', views.cropper, name='cropper'),
	

	 

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
