# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import django.utils.timezone as timezone
import datetime
#python 3 兼容2添加
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.
###import apps 
from api.pub import common
#资源类型表
@python_2_unicode_compatible
class sp_zone(models.Model):
	zone = models.CharField(u'所在地区', max_length=24)
	def __str__(self):
		return self.zone
	class Meta:
		verbose_name = verbose_name_plural = u'所在地区'
		db_table = 'sp_zone'
#'IP地址
@python_2_unicode_compatible
class sp_addr(models.Model):
	addr = models.CharField(u'服务器地址', max_length=24)
	def __str__(self):
		return self.addr
	class Meta:
		verbose_name = verbose_name_plural = u'服务器地址'
		db_table = 'sp_addr'
#归属项目表
@python_2_unicode_compatible
class sp_project(models.Model):
	project = models.CharField(u'账户分类', max_length=24)
	def __str__(self):
		return self.project
	class Meta:
		verbose_name = verbose_name_plural = u'账户分类'
		db_table = 'sp_project'

#权限
@python_2_unicode_compatible
class sp_auth(models.Model):
    auth = models.CharField(u'权限', max_length=8)
    def __str__(self):
        return self.auth
    class Meta:
        verbose_name = verbose_name_plural = u'权限'
        db_table = 'sp_auth'

#状态
@python_2_unicode_compatible
class sp_status(models.Model):
    status = models.CharField(u'状态', max_length=8)
    def __str__(self):
        return self.status
    class Meta:
        verbose_name = verbose_name_plural = u'状态'
        db_table = 'sp_status'

#FTP管理表 itresource
@python_2_unicode_compatible
class supplier_info(models.Model):
    id = models.AutoField(primary_key=True)
    sp_applicant = models.CharField(u'申请人', max_length=12, blank=False, null=False)
    sp_applicat_email = models.EmailField(u'申请人Email', blank=False, null=False)
    sp_id = models.CharField(u'供应商ID', max_length=24, blank = False, null=False)
    sp_project = models.ForeignKey(sp_project, verbose_name = u'账户分类', blank=False, null=False)
    sp_addr = models.ForeignKey(sp_addr, verbose_name = u'服务器地址', blank=False, null=False)
    sp_zone = models.ForeignKey(sp_zone, verbose_name = u'所在地区', blank=False, null=False)
    sp_user = models.CharField(u'FTP用户名', max_length=24, blank=False, null=False)
    sp_pwd = models.CharField(u'FTP密码', max_length=24, blank=False, null=False)
    sp_auth = models.ForeignKey(sp_auth, verbose_name='权限', blank=False, null=False)
    sp_details = models.TextField(u'申请备注', max_length=128, blank=True, null=False)
    sp_creation = models.DateTimeField(u'申请时间', default = timezone.now)
    sp_association_id = models.CharField(u'工单ID', max_length=8, editable=False)
    sp_status = models.ForeignKey(sp_status, verbose_name = u'状态', blank = True, null=True)
    sp_remark = models.TextField(u'备注信息', max_length=256, blank = True, null=True)

    def __str__(self):
        return self.sp_applicant
    class Meta:
        verbose_name = verbose_name_plural = u'FTP账户管理'
        db_table = 'supplier_info'
