"""foo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render

def send_index(request):
	return render(request,'index.html')

def send_js(request) :
    return render(request,'js/index.js')

def send_angular_js(request) :
    return render(request,'js/angular.min.js')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'js/index\.js',send_js),
    url(r'js/angular\.min\.js',send_angular_js),
    url(r'',send_index), 
]
