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
from config.models import mail_info
from api.mail import sendmail
from api.pub import common
from .models import supplier_info, sp_zone, sp_addr, sp_project, sp_auth, sp_status

# Create your views here.
'''
---------------以下方法对应的页面-----------------
FTP账户申请 ftpuser_add
申请中列表  create_info
创建完成或已关闭列表 supp_info
账户详情页面 user_details
'''
##获取supplier数据库信息表单
class PostForm(forms.ModelForm):
	class Meta:
		model = supplier_info
		#申请人 申请人Email 资源类型 申请部门 归属项目 审批人 申请详情
		fields = ['sp_applicant', 'sp_applicat_email', 'sp_id', 'sp_addr', 'sp_zone', 'sp_user', 'sp_auth', 'sp_project',
				'sp_details']

#新建资源工单申请
#@login_required(login_url='/login/')
def ftpuser_add(request):
	pk = common.pkgen()
	form = PostForm(request.POST)
	if form.is_valid():
		fs = form.save(commit=False)
		##初始化默认值
		fs.sp_association_id = pk
		fs.sp_status_id = '1'
		fs.sp_pwd = pk
		fs.save()
		#send_mail(pk=pk)
		#保存完后跳转到/itres
		return HttpResponseRedirect('/supp/')
	#else:
	#	messages.error(request, u'工单%s提交错误' % pk)

	context = {
		'form' : form,
		}
	return render(request, 'supplier/ftpuser_add.html', context)

#FTP创建状态是申请中的账户列表
#@login_required(login_url='/login/')
def create_info(request):
	#查询状态包含sp_status=1 的数据
	supp_info = supplier_info.objects.filter(sp_status=1)
	#实现分页 调用分页函数
	list_page = common.page_info(request=request, v_keys=supp_info, limit=100)
	##定义空值导入数据库数值 ilt = "itres list"
	v_list = {}
	i = 1
	for k in list_page:
		v_list.update({i : {}})
		v_list[i]["id"] = k.id
		v_list[i]["applicant"] = k.sp_applicant #申请人
		v_list[i]["project"] = k.sp_project #归属项目
		v_list[i]["creation"] = k.sp_creation #申请时间
		v_list[i]["sp_id"] = k.sp_id #供应商ID
		v_list[i]["addr"] = k.sp_addr #地址
		v_list[i]["zone"] = k.sp_zone #区域
		v_list[i]["user"] = k.sp_user #用户名
		v_list[i]["status"] = k.sp_status #状态

		i = i + 1

	context =  {
		'v_list' : v_list,
		'list_page' : list_page,
		}
	return render(request, 'supplier/create_info.html', context)


#FTP状态是运行中或已关闭的账户列表
#@login_required(login_url='/login/')
def supp_info(request):
	server = request.META['HTTP_HOST']
	#查询状态不包含sp_status=1 的数据
	supp_info = supplier_info.objects.exclude(sp_status=1)
	#实现分页 调用分页函数
	list_page = common.page_info(request=request, v_keys=supp_info, limit=200)
	##定义空值导入数据库数值 ilt = "itres list"
	v_list = {}
	i = 1
	for k in list_page:
		v_list.update({i : {}})
		v_list[i]["id"] = k.id
		v_list[i]["applicant"] = k.sp_applicant #申请人
		v_list[i]["project"] = k.sp_project #归属项目
		v_list[i]["creation"] = k.sp_creation #申请时间
		v_list[i]["sp_id"] = k.sp_id #供应商ID
		v_list[i]["addr"] = k.sp_addr #地址
		v_list[i]["zone"] = k.sp_zone #区域
		v_list[i]["user"] = k.sp_user #用户名
		v_list[i]["status"] = k.sp_status #状态
		v_list[i]["status_id"] = k.sp_status_id

		i = i + 1

	context =  {
		'v_list' : v_list,
		'list_page' : list_page,
		}
	return render(request, 'supplier/supplier_info.html', context)

#FTP用户详细信息
#@login_required(login_url='/login/')
def user_details(request, id):
	details = supplier_info.objects.get(id=int(id))

	context =  {
		'details' : details,
		}
	return render(request, 'supplier/user_details.html', context)

'''
---------------以下方法对应的页面-----------------
FTP账户创建 ftpuser_create
FTP账户关闭 ftpuser_stop
FTP账户启用 ftpuser_enable
'''
#创建账户并更改状态未使用中
#@login_required(login_url='/login/')
def ftpuser_create(request,id):
	supp_info = supplier_info.objects.filter(id=id).update(sp_status=2)
	#调用FTP模块
	return HttpResponseRedirect('/supp/')
#停止状态
#@login_required(login_url='/login/')
def ftpuser_stop(request,id):
	supp_info = supplier_info.objects.filter(id=id).update(sp_status=3)
	#调用FTP模块
	return HttpResponseRedirect('/supp/')
#启用状态
#@login_required(login_url='/login/')
def ftpuser_enable(request,id):
	supp_info = supplier_info.objects.filter(id=id).update(sp_status=2)
	#调用FTP模块
	return HttpResponseRedirect('/supp/')