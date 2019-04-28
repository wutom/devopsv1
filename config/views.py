# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json, time, re, os, sys, subprocess
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django import forms
from django.contrib import messages
from django.views.decorators import csrf
from django.contrib.auth.decorators import login_required
###app models
from .models import Structure_info, Structure_appname, Structure_data_id, Structure_accesskey_id, Structure_project
from .models import nav_info, doc_info, nav_types
# Create your views here.

'''
定义表单类 PostForm 从models加载表单
工单调用表单并初始化一些默认值
保存表单后调用邮件发送函数发送邮件
'''

class PostForm(forms.ModelForm):
	class Meta:
		model = Structure_info
		#申请人 申请人Email 资源类型 申请部门 归属项目 审批人 申请详情
		fields = ['owner', 'owner_email', 'project', 'appname', 'app_remark', 'data_id', 'data_user', 'data_remark', 'accesskey_id', 'accesskey_remark', 'oss_remark']

##导航栏和文档不能添加认证
def nav_doc(request):
	server = request.META['HTTP_HOST']
	doc = doc_info.objects.all()
	nav = nav_info.objects.all()
	types = nav_types.objects.all()

	d_list = {}
	t_list = {}
	n_list = {}
	k = 1
	i = 1
	for d in doc:
		d_list.update({i : {}})
		d_list[i]["name"] = d.name
		d_list[i]["url"] = d.doc_url
		i = i + 1

	i = 1
	for t in types:
		t_list.update({i : {}})
		t_list[i]["id"] = t.id
		t_list[i]["name"] = t.name
		i = i + 1
		nav_list = nav_info.objects.filter(types=t.id)
		for n in nav_list:
			n_list.update({k : {}})
			n_list[k]["id"] = n.types_id
			n_list[k]["name"] = n.name
			n_list[k]["navurl"] = n.navurl
			k = k + 1

	context =  {
		'd_list' : d_list,
		't_list' : t_list,
		'server' : server,
		'n_list' : n_list,
		}
	return context


#新建应用关系工单申请
#@login_required(login_url='/login/')
def structure_add(request):
	server = request.META['HTTP_HOST']
	form = PostForm(request.POST)
	if form.is_valid():
		form.save()
		#保存完后跳转到/itres
		return HttpResponseRedirect('/stru/add')
	#else:
	#	messages.error(request, u'工单%s提交错误' % pk)

	context = {
		'form' : form,
		}
	return render(request, 'config/structure_add.html', context)
