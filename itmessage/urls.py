# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
app_name = 'itmessage'

urlpatterns = [
	#默认使用ecs视图
	##itmes slb
	url(r'^$', views.ali_slb_info, name='itmes'),
	url(r'^info/slb/(?P<slb_id>[^/]+)/$', views.ali_slb_details, name='itmesinfoslb'),
	##itmes rds
	url(r'^info/rds/$', views.ali_rds_info, name='itmesrds'),
	#[^/]+ 匹配了所有字符串 a-z A-Z 0-9 _-+等
	url(r'^info/rds/(?P<rds_id>[^/]+)/$', views.ali_rds_details, name='itmesinfords'),
	##itmes ecs
	url(r'^info/ecs/$', views.ali_ecs_info, name='itmesecs'),
	url(r'^info/ecs/(?P<ecs_id>[^/]+)/$', views.ali_ecs_details, name='itmesinfoecs'),
]