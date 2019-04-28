# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms
##import 
import django.utils.timezone as timezone
import datetime
#python 3 兼容2添加
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.
##import apps

from config.models import Structure_project, Itres_department
##创建资源管理的各个表
#资源类型表
@python_2_unicode_compatible
class Itres_types(models.Model):
	types = models.CharField(u'资源类型', max_length=14)
	def __str__(self):
		return self.types
	class Meta:
		verbose_name = verbose_name_plural = u'资源类型'
		db_table = 'Itres_types'
#申请部门 后期会弃用 用config 模块里面的申请部门替换
#@python_2_unicode_compatible
#class Itres_department(models.Model):
#	department = models.CharField(u'申请部门', max_length=14)
#	def __str__(self):
#		return self.department
#	class Meta:
#		verbose_name = verbose_name_plural = u'申请部门'
#		db_table = 'Itres_department'
#归属项目表

#使用周期表
@python_2_unicode_compatible
class Itres_cycle(models.Model):
	cycle = models.CharField(u'使用周期', max_length=8)
	def __str__(self):
		return self.cycle
	class Meta:
		verbose_name = verbose_name_plural = u'使用周期'
		db_table = 'Itres_cycle'
#审批人表
@python_2_unicode_compatible
class Itres_approver(models.Model):
    approver = models.CharField(u'审批人', max_length=8)
    approver_email = models.EmailField(u'Email', blank = False, null=False)
    def __str__(self):
        return self.approver
    class Meta:
        verbose_name = verbose_name_plural = u'审批人'
        db_table = 'Itres_approver'

#状态
@python_2_unicode_compatible
class Itres_status(models.Model):
    status = models.CharField(u'状态', max_length=8)
    def __str__(self):
        return self.status
    class Meta:
        verbose_name = verbose_name_plural = u'状态'
        db_table = 'Itres_status'

#资源管理表 itresource
@python_2_unicode_compatible
class Itres_info(models.Model):
    id = models.AutoField(primary_key=True)
    res_applicant = models.CharField(u'申请人', max_length=12, blank=False, null=False)
    res_applicat_email = models.EmailField(u'申请人Email', blank=False, null=False)
    res_types = models.ForeignKey(Itres_types, verbose_name=u'资源类型', blank = False, null=False)
    res_department = models.ForeignKey(Itres_department, verbose_name=u'申请部门', blank=False, null=False)
    project = models.ForeignKey(Structure_project, verbose_name=u'归属项目')
    res_approver = models.ForeignKey(Itres_approver, verbose_name = u'审批人', blank=False, null=False)
    res_details = models.TextField(u'资源详情', max_length=256, blank=True, null=False)
    res_cycle = models.ForeignKey(Itres_cycle, verbose_name = u'使用周期', blank = False, null=False)
    res_creation = models.DateTimeField(u'申请时间', default = timezone.now)
    res_association_id = models.CharField(u'工单ID', max_length=8, editable=False)
    res_resid = models.CharField(u'实例ID', max_length=48, blank=True, null=True)
    res_status = models.ForeignKey(Itres_status, verbose_name = u'状态', blank = True, null=True)
    res_remark = models.TextField(u'备注信息', max_length=256, blank = True, null=True)

    def __str__(self):
        return self.res_applicant
    class Meta:
        verbose_name = verbose_name_plural = u'资源工单'
        db_table = 'Itres_info'
