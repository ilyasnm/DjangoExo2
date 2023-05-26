"""
URL configuration for OpeniaVid project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include, path
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
import requests
from exo2.views import upload_video
from exo2 import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    #path('exo2/', include('OpeniaVid.urls')),
    path('', views.index, name='index'),
    path('upload/', views.upload_video, name='upload_video'),
    #path('', upload_video, name='home'),
    path('admin/', admin.site.urls),
   
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
