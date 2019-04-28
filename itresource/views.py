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
from config.models import App_info, mail_info, Structure_info, Structure_appname, Structure_data_id, Structure_accesskey_id, Structure_project, Itres_department
from api.pub import common
from api.mail import sendmail
from .models import Itres_info,Itres_types,Itres_approver,Itres_cycle,Itres_status
from api.ali.cloud import Cloud as cloud
cloud = cloud()
# Create your views here.

'''
#定义全局需要引用的函数和变量
'''
###定义发送邮件模块因发送内网不一样暂调不使用公告函数send_mail
def send_mail(pk):
	#获取邮件配置
	mail = mail_info.objects.get(id=2)
	send = mail.send
	passwd = mail.passwd
	server = mail.server.split("//")[1]
	port = mail.port
	head = mail.head
	remark = mail.remark

	#获取工单详情
	res = Itres_info.objects.get(res_association_id=pk)
	to_addr = ['ops@vcg.com']
	app_add = Itres_approver.objects.get(id=res.res_approver_id)
	to_addr.append(app_add.approver_email)
	approver = res.res_approver
	applicant = res.res_applicant
	applicat_email = res.res_applicat_email
	types = res.res_types
	department = res.res_department
	project = res.project
	creation = res.res_creation
	cycle = res.res_cycle
	details = res.res_details

	text = """
		<h4>请审批人:%s 仔细查看工单内容并审核.运维获取到工单ID后即代表审核人同意并完成工单内容.</h4>
		<p>申请人:%s, 申请人Email:%s, 申请部门:%s, 归属项目:%s</p>
		<p>资源类型:%s, 使用周期:%s, 申请时间:%s </p>
		<p>资源详情:%s </p>
		<p>请将工单ID:%s 提供给运维同学.</p>
		""" % (approver,applicant,applicat_email,department,project,types,cycle,creation,details,pk)
	try:
		sendmail.Smtp_To(send, passwd, server, port, to_addr, remark, head, text)
	except:
		return False
	else:
		return True

'''
定义表单类 PostForm 从models加载表单
工单调用表单并初始化一些默认值
保存表单后调用邮件发送函数发送邮件
'''
##-----------------------------------新建资源工单申请
class PostForm(forms.ModelForm):
	class Meta:
		model = Itres_info
		#申请人 申请人Email 资源类型 申请部门 归属项目 审批人 申请详情
		fields = ['res_applicant', 'res_applicat_email', 'res_types', 'res_department', 'project',
			'res_approver', 'res_cycle', 'res_details']


####
#@login_required(login_url='/login/')
def itres_add(request):
	pk = common.pkgen()
	server = request.META['HTTP_HOST']
	form = PostForm(request.POST)
	if form.is_valid():
		fs = form.save(commit=False)
		##初始化默认值
		fs.res_association_id = pk
		fs.res_status_id = '3'
		fs.save()
		send_mail(pk=pk)
		#保存完后跳转到/itres
		return HttpResponseRedirect('/itres/')
	#else:
	#	messages.error(request, u'工单%s提交错误' % pk)

	context = {
		'form' : form,
		}
	return render(request, 'itresource/itres_add.html', context)


'''
工单列表部分
'''

###资源工单列表
#@login_required(login_url='/login/')
def itres_info(request):
	itres = Itres_info.objects.all()
#调用分页函数
	list_page = common.page_info(request,v_keys=itres, limit=100)

	v_list = {}
	i = 1
	for k in list_page:
		v_list.update({i : {}})
		v_list[i]["id"] = k.id
		v_list[i]["res_applicant"] = k.res_applicant #申请人
		v_list[i]["res_types"] = k.res_types #资源类型
		v_list[i]["res_department"] = k.res_department #申请部门
		v_list[i]["project"] = k.project #归属项目
		v_list[i]["res_approver"] = k.res_approver #审批人
		v_list[i]["res_creation"] = k.res_creation #申请时间
		v_list[i]["res_resid"] = k.res_resid #资源ID
		v_list[i]["res_status"] = k.res_status #状态

		i = i + 1

	context =  {
		'v_list' : v_list,
		'list_page' : list_page,
		}
	return render(request, 'itresource/itres_info.html', context)

#资源工单详细信息
#@login_required(login_url='/login/')
def itres_info_details(request, id):
	details = Itres_info.objects.get(id=int(id))

	context =  {
		'details' : details,
		}
	return render(request, 'itresource/itres_info_details.html', context)


####-------------------------应用工单申请
class App_PostForm(forms.ModelForm):
	class Meta:
		model = App_info
		#申请人 申请人Email 资源类型 申请部门 归属项目 审批人 申请详情
		fields = ['owner', 'owner_email', 'project', 'Itres_department', 'env_types', 'app_types', 'code_types', 'appname', 'app_remark',
			'code_addr', 'domain', 'port', 'amount', 'data_id', 'data_user', 'data_remark', 'accesskey_id', 'accesskey_remark', 'oss_remark', 'mail_remark']


#新建应用申请
#@login_required(login_url='/login/')
def app_add(request):
	server = request.META['HTTP_HOST']
	form = App_PostForm(request.POST)
	if form.is_valid():
		fs = form.save(commit=False)
		##初始化默认值
		fs.app_status_id = '1'
		fs.save()
		#保存完后跳转到/itres
		return HttpResponseRedirect('/itlist/')

	context = {
		'form' : form,
		}
	return render(request, 'itresource/app_add.html', context)

#应用程序列表
#@login_required(login_url='/login/')
def app_info(request):
	app = App_info.objects.all()
#调用分页函数
	list_page = common.page_info(request,v_keys=app,limit=100)

	v_list = {}
	i = 1
	for k in list_page:
		v_list.update({i : {}})
		v_list[i]["id"] = k.id
		v_list[i]["owner"] = k.owner
		v_list[i]["appname"] = k.appname
		v_list[i]["domain"] = k.domain
		v_list[i]["project"] = k.project
		v_list[i]["env_types"] = k.env_types
		v_list[i]["amount"] = k.amount
		v_list[i]["port"] = k.port
		v_list[i]["app_status_id"] = k.app_status_id

		i = i + 1

	context =  {
		'v_list' : v_list,
		'list_page' : list_page,
		}
	return render(request, 'itresource/app_info.html', context)

#应用拓扑结构
#@login_required(login_url='/login/')
def app_topology(request,id):
	app = App_info.objects.get(id=id)
	v_list = {}
	v_list['name'] = app.appname
	v_list['domain'] = app.domain
	v_list['owner'] = app.owner
	v_list['project'] = app.project
	v_list['env_types'] = app.env_types
	v_list['app_types'] = app.app_types
	v_list['code_addr'] = app.code_addr
	v_list['code_types'] = app.code_types
	v_list['port'] = app.port
	v_list['amount'] = app.amount
	v_list['data_id'] = app.data_id
	v_list['oss_remark'] = app.oss_remark
	v_list['ak'] = app.accesskey_id

	context =  {
		'v_list' : v_list,
		}

	return render(request, 'itresource/app_topology.html', context)


##应用程序发版汇总
#@login_required(login_url='/login/')
def app_update(request):
    try:
        jenkins_list = cloud.get_Jenkins_Builds_Pro()
    except TypeError:
        jenkins_list = {}

    nowtime = int(time.time())
    j_list = {}
    j_list.clear()
    i = 1
    for k in jenkins_list:
        #开始遍历
        j_list.update({i : {}})
        jtime = str(k['time'])
        if nowtime - common.string2timestamp(str(jtime)) < 604800:
            j_list[i]['ServiceName'] = k['ServiceName']
            j_list[i]['Action'] = k['Action']
            j_list[i]['time'] = k['time']
        else:
            j_list.pop(i)
        i = i + 1  

    context =  {
        'j_list' : j_list,
        'jenkins_count' : len(jenkins_list),
        'week_count' : len(j_list)
        }
    return render(request, 'itresource/index_app.html', context)