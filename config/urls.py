# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
app_name = 'config'

urlpatterns = [
	url(r'^add/', views.structure_add, name='struadd'),
	#url(r'^add/', views.itres_add, name='itresadd'),
	#url(r'^info/(?P<id>\d+)/$', views.itres_info_details, name='itresinfo'),
]