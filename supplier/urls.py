# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
app_name = 'supplier'

urlpatterns = [
	url(r'^$', views.supp_info, name='supp'),
	url(r'^ftp/add/', views.ftpuser_add, name='ftpadd'),
	url(r'^cre/', views.create_info, name='crateftp'),
	url(r'^user/(?P<id>\d+)/$', views.user_details, name='userdetails'),
	##FTP 账户状态更改url
	url(r'^ftp/create/(?P<id>\d+)/$', views.ftpuser_create, name='ftpusercreate'),
	url(r'^ftp/stop/(?P<id>\d+)/$', views.ftpuser_stop, name='ftpuserstop'),
	url(r'^ftp/enable/(?P<id>\d+)/$', views.ftpuser_enable, name='ftpuserenable'),
]