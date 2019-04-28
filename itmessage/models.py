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

from config.models import Structure_project

#设备管理表 itmessage
@python_2_unicode_compatible
class Dev_types(models.Model):
	types = models.CharField(u'设备型号', max_length=24)
	def __str__(self):
		return self.types
	class Meta:
		verbose_name = verbose_name_plural = u'设备型号'
		db_table = 'Dev_types'

@python_2_unicode_compatible
class Dev_cabinets(models.Model):
	cabinets = models.CharField(u'机柜编号', max_length=24)
	def __str__(self):
		return self.cabinets
	class Meta:
		verbose_name = verbose_name_plural = u'机柜编号'
		db_table = 'Dev_cabinets'

@python_2_unicode_compatible
class Dev_seq(models.Model):
	seq = models.CharField(u'放置序号', max_length=24)
	def __str__(self):
		return self.seq
	class Meta:
		verbose_name = verbose_name_plural = u'放置序号'
		db_table = 'Dev_seq'


@python_2_unicode_compatible
class Dev_idc(models.Model):
	idc = models.CharField(u'机房位置', max_length=24)
	def __str__(self):
		return self.idc
	class Meta:
		verbose_name = verbose_name_plural = u'机房位置'
		db_table = 'Dev_idc'


#设备管理表 itmessage
@python_2_unicode_compatible
class Dev_info(models.Model):
    name = models.CharField(u'设备名称', max_length=24)
    types = models.ForeignKey(Dev_types, verbose_name=u'设备型号')
    project = models.ForeignKey(Structure_project, verbose_name=u'归属项目')
    dev_id = models.CharField(u'设备ID号', max_length=24)
    add1 = models.GenericIPAddressField(u'网卡地址1')
    add2 = models.GenericIPAddressField(u'网卡地址2')
    add3 = models.GenericIPAddressField(u'网卡地址3')
    add4 = models.GenericIPAddressField(u'网卡地址4')
    dev_cpu = models.CharField(u'CPU信息', max_length=48)
    dev_disk = models.CharField(u'磁盘信息', max_length=48)
    dev_sys = models.CharField(u'系统信息', max_length=48)
    cabinets = models.ForeignKey(Dev_cabinets, verbose_name=u'机柜编号')
    seq = models.ForeignKey(Dev_seq, verbose_name=u'放置序号')
    idc = models.ForeignKey(Dev_idc, verbose_name=u'机房位置')
    remark = models.TextField(u'备注信息', max_length=256, blank = True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = verbose_name_plural = u'设备管理'
        db_table = 'Dev_info'