# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.template.loader import get_template
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
###app models

from itresource.models import Itres_info,Itres_types,Itres_approver,Itres_cycle,Itres_status
from config.models import Itres_department
# Create your views here.
###app api function
from api.ali.cloud import Cloud as cloud
from api.pub import common
##全局变量
###从Redis获取数据
cloud = cloud()

try:
	ali_rds = cloud.get_Ali_Rds_List()
	ali_ecs = cloud.get_Ali_Ecs_List()
	ali_slb = cloud.get_Ali_Slb_List()
	slb_details = cloud.get_Ali_Slb_Detail()
	ecs_details = cloud.get_Ali_Ecs_Detail()
	rds_details = cloud.get_Ali_Rds_Detail()

except TypeError:
	ali_rds = {}
	ali_ecs = {}
	ali_slb = {}
	slb_details = {}
	ecs_details = {}
	rds_details = {}


###公共函数 从数据库查询工单信息,填充未知数据

def select_itres_info(i, res_resid, v_list):
	try:
		itres = Itres_info.objects.get(res_resid=res_resid)
		v_list[i]['project'] = itres.project
		v_list[i]['status'] = itres.res_status
		v_list[i]['association_id'] = itres.res_association_id
		v_list[i]['res_id'] = itres.id
		v_list[i]['association_com'] = 2
	except Itres_info.DoesNotExist:
		v_list[i]['project'] = u'未关联'
		v_list[i]['status'] = u'未关联'
		v_list[i]['association_com'] = 1
		v_list[i]['association_id'] = u'未关联'


##############################slb 实例列表
#@login_required(login_url='/login/')
def ali_slb_info(request):
	rds_count = len(ali_rds)
	ecs_count = len(ali_ecs)
	slb_count = len(ali_slb)
	#调用分页函数
	list_page = common.page_info(request,v_keys=ali_slb, limit=100)

	v_list = {}
	i = 1
	for k in list_page:
		#开始遍历实例
		v_list.update({i : {}})
		vid = k['LoadBalancerId']
		v_list[i]['id'] = k['LoadBalancerId']
		v_list[i]['name'] = k['LoadBalancerName']
		v_list[i]['add'] = k['Address']
		select_itres_info(i=i, res_resid=vid, v_list=v_list)
		i = i + 1

	context = {
		'v_list' : v_list,
		'rds_count' : rds_count,
		'ecs_count' : ecs_count,
		'slb_count' : slb_count,
		'list_page' : list_page,
		}
	return render(request, 'itmessage/itmes_info_slb.html', context)

#############slb 实例详细信息
#@login_required(login_url='/login/')
def ali_slb_details(request, slb_id):
	details = slb_details[slb_id]

	context = {
		'slb_id' : slb_id,
		'details' : details,
		}
	return render(request, 'itmessage/itmes_slb_details.html', context)


#########------------------ecs 实例列表
#@login_required(login_url='/login/')
def ali_ecs_info(request):
	rds_count = len(ali_rds)
	ecs_count = len(ali_ecs)
	slb_count = len(ali_slb)
#调用分页函数
	list_page = common.page_info(request,v_keys=ali_ecs, limit=100)

	v_list = {}
	i = 1
	for k in list_page:
		#开始遍历实例
		v_list.update({i : {}})
		vid = k['InstanceId']
		v_list[i]['id'] = k['InstanceId']
		v_list[i]['name'] = k['InstanceName']
		v_list[i]['pubadd'] = k['PublicIpAddress']
		v_list[i]['lanadd'] = k['InnerIpAddress']
		#调用公共函数查询数据库
		select_itres_info(i=i, res_resid=vid, v_list=v_list)
		i = i + 1

	context = {
		'v_list' : v_list,
		'rds_count' : rds_count,
		'ecs_count' : ecs_count,
		'slb_count' : slb_count,
		'list_page' : list_page,
		}
	return render(request, 'itmessage/itmes_info_ecs.html', context)

#ecs实例详细信息
#@login_required(login_url='/login/')
def ali_ecs_details(request, ecs_id):
	details = ecs_details[ecs_id]

	context = {
		'ecs_id' : ecs_id,
		'details' : details,
		}
	return render(request, 'itmessage/itmes_ecs_details.html', context)


#########------------------rds 实例列表
#@login_required(login_url='/login/')
def ali_rds_info(request):
	rds_count = len(ali_rds)
	ecs_count = len(ali_ecs)
	slb_count = len(ali_slb)
#调用分页函数
	list_page = common.page_info(request,v_keys=ali_rds, limit=100)

	v_list = {}
	i = 1
	for k in list_page:
		#开始遍历实例
		v_list.update({i : {}})
		vid = k['DBInstanceId']
		v_list[i]['id'] = k['DBInstanceId']
		v_list[i]['name'] = k['DBInstanceDescription']
		v_list[i]['add'] = k['ConnectionString']
		#调用公共函数查询数据库
		select_itres_info(i=i, res_resid=vid, v_list=v_list)
		i = i + 1

	context = {
		'v_list' : v_list,
		'rds_count' : rds_count,
		'ecs_count' : ecs_count,
		'slb_count' : slb_count,
		'list_page' : list_page,
		}
	return render(request, 'itmessage/itmes_info_rds.html', context)

#ecs实例详细信息
#@login_required(login_url='/login/')
def ali_rds_details(request, rds_id):
	server = request.META['HTTP_HOST']
	details = rds_details[rds_id]

	context = {
		'rds_id' : rds_id,
		'details' : details,
		}
	return render(request, 'itmessage/itmes_rds_details.html', context)