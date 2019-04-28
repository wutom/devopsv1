# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import admin
from django.forms import CheckboxSelectMultiple


from .models import Itres_info,Itres_types,Itres_approver,Itres_cycle,Itres_status
# Register your models here.

#资源信息
class Itresinfo(admin.ModelAdmin):
	formfield_overrides = {
		models.ManyToManyField: {'widget': CheckboxSelectMultiple},
		}
	list_display = ('res_applicant', 'res_department', 'res_creation', 'res_status', 'res_association_id', 'res_resid')
	search_fields = ['res_applicant', 'res_association_id', 'res_resid']
	list_per_page = 50

###在后台隐藏部分表单 可在主表单里面修改编辑
class  MyModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
#资源工单
admin.site.register(Itres_info, Itresinfo)
#资源类型
admin.site.register(Itres_types, MyModelAdmin)
#申请部门
#admin.site.register(Itres_department, MyModelAdmin)
#审批人
admin.site.register(Itres_approver, MyModelAdmin)
#使用周期
admin.site.register(Itres_cycle, MyModelAdmin)
#状态
admin.site.register(Itres_status, MyModelAdmin)