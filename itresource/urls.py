# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
app_name = 'itresource'

urlpatterns = [
	url(r'^$', views.itres_info, name='itres'),
	url(r'^add/', views.itres_add, name='itresadd'),
	url(r'^appinfo/', views.app_info, name='appinfo'),
	url(r'^appadd/', views.app_add, name='appadd'),
	url(r'^appupdate/', views.app_update, name='appupdate'),
	url(r'^apptpy/(?P<id>\d+)/$', views.app_topology, name='apptopology'),
	url(r'^info/(?P<id>\d+)/$', views.itres_info_details, name='itresinfo'),
]