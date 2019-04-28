# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
app_name = 'index'

urlpatterns = [
	url(r'^', views.index, name='index'),
	#url(r'^add/', views.itres_add, name='itresadd'),
	#url(r'^info/(?P<id>\d+)/$', views.itres_info_details, name='itresinfo'),
]