# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import admin
from django.forms import CheckboxSelectMultiple


from .models import Dev_info, Dev_idc, Dev_seq, Dev_types, Dev_cabinets
#设备管理
class Devinfo(admin.ModelAdmin):
	formfield_overrides = {
		models.ManyToManyField: {'widget': CheckboxSelectMultiple},
		}
	list_display = ('name', 'types', 'dev_id', 'add1', 'cabinets', 'dev_sys')
	search_fields = ('name', 'add1')
	list_per_page = 50
	ordering = ('id',)

###在后台隐藏部分表单 可在主表单里面修改编辑
class  MyModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
#设备管理
admin.site.register(Dev_info, Devinfo)
admin.site.register(Dev_cabinets, MyModelAdmin)
admin.site.register(Dev_types, MyModelAdmin)
admin.site.register(Dev_seq, MyModelAdmin)
admin.site.register(Dev_idc, MyModelAdmin)