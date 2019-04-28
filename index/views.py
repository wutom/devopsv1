# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json, time, re, os, sys, subprocess
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate
from django.views.decorators import csrf
from django.contrib.auth.decorators import login_required
from datetime import datetime as dat

###app models
from config.models import mail_info, Structure_info, Structure_appname, Structure_data_id, Structure_accesskey_id, Structure_project
from api.mail import sendmail
from api.ali.cloud import Cloud as cloud
cloud = cloud()
from api.pub import common, ldapauth
from itmessage.models import Dev_info

os_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
###首页及登录页面

##登陆表单类
class UserForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())

##用户不存在创建用户
#@login_required(login_url='/login/')
def createuser(username, password):
	user = User(username=username, password=password)
	user.set_password(password)
	user.is_staff = True
	user.save()

##用户存在django 密码不对重置密码
#@login_required(login_url='/login/')
def respasswd(username, password):
	user = User.objects.get(username=username)
	user.set_password(password)
	user.is_staff = True
	user.save()

##ldap + django 认证
#def login_auth(request, username, password):


##登陆页面
def login(request):
    #server = request.META['HTTP_HOST']
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            ##判断ldap 和 django自身auth系统账户，在后期登陆验证使用.
            ldap_auth = ldapauth.LDAPlogin(username=username,password=password)
            local_auth = auth.authenticate(username=username, password=password)
            if ldap_auth == 'True' and local_auth:
            	auth.login(request, local_auth)
            	response = HttpResponseRedirect('/')
            	response.set_cookie('username', username, 3600)
            	return response
            elif ldap_auth == 'True' and not local_auth:
            	local_user = auth.forms.User.objects.filter(username=username)
            	if local_user:
            		respasswd(username=username,password=password)
            		local_reset_pwd = auth.authenticate(username=username, password=password)
            		if local_reset_pwd:
            			response = HttpResponseRedirect('/')
            			response.set_cookie('username', username, 3600)
            			return response
            	else:
            		createuser(username=username,password=password)
            		local_auth_res = auth.authenticate(username=username, password=password)
            		if local_auth_res:
            			auth.login(request, local_auth_res)
            			response = HttpResponseRedirect('/')
            			response.set_cookie('username', username, 3600)
            			return response
        else:
			return HttpResponseRedirect('/login/')
    else:
        uf = UserForm()
    return render(request, 'index/login.html', {'uf':uf},)

##注销页面
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/") 

#@login_required(login_url='/login/')
def index(request):
    context = {}
    return render(request, 'index/index.html', context)
#@login_required(login_url='/login/')
def itlist(request):
	return render(request, 'index/itlist.html')
