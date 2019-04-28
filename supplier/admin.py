# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import admin
from django.forms import CheckboxSelectMultiple


from .models import supplier_info, sp_zone, sp_addr, sp_project, sp_auth, sp_status
# Register your models here.


#程序信息
class Supplierinfo(admin.ModelAdmin):
	formfield_overrides = {
		models.ManyToManyField: {'widget': CheckboxSelectMultiple},
		}
	list_display = ('sp_applicant', 'sp_id', 'sp_addr', 'sp_user', 'sp_auth', 'sp_zone', 'sp_project', 'sp_association_id', 'sp_status')
	search_fields = ('sp_applicant','sp_user', 'sp_id', 'sp_addr__addr', 'sp_association_id',)
	list_per_page = 100
#	ordering = ['id',]

###在后台隐藏部分表单 可在主表单里面修改编辑
class  MyModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

#FTP工单
admin.site.register(supplier_info, Supplierinfo)
#资源类型
admin.site.register(sp_zone, MyModelAdmin)
admin.site.register(sp_addr, MyModelAdmin)
admin.site.register(sp_project)
admin.site.register(sp_auth, MyModelAdmin)
admin.site.register(sp_status, MyModelAdmin)