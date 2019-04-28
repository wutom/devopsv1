# -*- coding: utf-8 -*-
"""vcgopsdev URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    ##it resource 资源工单列表
    url(r'^itres/', include('itresource.urls')),
    ##it message 资源信息
    url(r'^itmes/', include('itmessage.urls')),
    ##supplier  FTP
    url(r'^supp/', include('supplier.urls')),
]
