# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib import admin
from django.forms import CheckboxSelectMultiple

from .models import mail_info, Structure_info, Structure_appname, Structure_data_id, Structure_accesskey_id, Structure_project
from .models import nav_info, doc_info, nav_types, env_types, app_types, code_types, app_status
from .models import domain_info, domain_dns, domain_supplier, domain_manager, domain_owner, domain_jieru
from .models import App_info,Itres_department
# Register your models here.

#文档管理
class Docinfo(admin.ModelAdmin):
	formfield_overrides = {
		models.ManyToManyField: {'widget': CheckboxSelectMultiple},
		}
	list_display = ('name', 'doc_url', 'remark')
	search_fields = ['name']
	list_per_page = 50
#	ordering = ['id',]

#导航管理
class Navinfo(admin.ModelAdmin):
	formfield_overrides = {
		models.ManyToManyField: {'widget': CheckboxSelectMultiple},
		}
	list_display = ('name', 'types', 'navurl', 'remark')
	search_fields = ['name']
	list_per_page = 50
#	ordering = ['id',]

#邮件信息
class Mailinfo(admin.ModelAdmin):
	formfield_overrides = {
		models.ManyToManyField: {'widget': CheckboxSelectMultiple},
		}
	list_display = ('send', 'server', 'port', 'head', 'remark')
	search_fields = ['send']
	list_per_page = 50
#	ordering = ['id',]

#关系结构配置
class Structureinfo(admin.ModelAdmin):
	formfield_overrides = {
		models.ManyToManyField: {'widget': CheckboxSelectMultiple},
		}
	list_display = ('owner', 'project', 'appname', 'app_remark', 'data_user', 'data_id', 'data_remark', 'accesskey_id', 'accesskey_remark')
	search_fields = ['owner']
	list_per_page = 50
#	ordering = ['id',]

#应用程序管理替代关系结构配置

class Appinfo(admin.ModelAdmin):
	formfield_overrides = {
		models.ManyToManyField: {'widget': CheckboxSelectMultiple},
		}
	list_display = ('owner','project', 'appname', 'app_types', 'code_types', 'env_types', 'app_remark', 'data_id', 'accesskey_id', 'app_status')
	search_fields = ('owner', 'appname__apppname', 'project__project', 'app_types__app', 'code_types__code', 'env_types__env', 'app_remark', 'data_id__data_id', 'accesskey_id__accesskey_id', 'app_status__status',)
	list_per_page = 50

#域名管理
class Domaininfo(admin.ModelAdmin):
	formfield_overrides = {
		models.ManyToManyField: {'widget': CheckboxSelectMultiple},
		}
	list_display = ('domian', 'expire', 'owner', 'supplier', 'beian_id', 'beian_ip', 'manager', 'beian_jieru', 'domain_dns')
	search_fields = ['domian',]
	list_per_page = 50
#	ordering = ['id',]

###在后台隐藏部分表单 可在主表单里面修改编辑
class  MyModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


#域名管理
admin.site.register(domain_info, Domaininfo)
#邮件配置
admin.site.register(mail_info, Mailinfo)
#文档管理
admin.site.register(doc_info, Docinfo)
#导航管理
admin.site.register(nav_info, Navinfo)
admin.site.register(nav_types, MyModelAdmin)
#关系结构配置
#admin.site.register(Structure_info, Structureinfo)
admin.site.register(Structure_appname, MyModelAdmin)
admin.site.register(Structure_data_id, MyModelAdmin)
admin.site.register(Structure_accesskey_id, MyModelAdmin)
#新的应用程序管理替代上面关系结构配置
admin.site.register(App_info, Appinfo)


#项目管理
admin.site.register(Structure_project)
#申请部门
admin.site.register(Itres_department)
#
admin.site.register(code_types, MyModelAdmin)
admin.site.register(app_types, MyModelAdmin)
admin.site.register(env_types, MyModelAdmin)
admin.site.register(app_status, MyModelAdmin)
admin.site.register(domain_dns, MyModelAdmin)
admin.site.register(domain_supplier, MyModelAdmin)
admin.site.register(domain_manager, MyModelAdmin)
admin.site.register(domain_owner, MyModelAdmin)
admin.site.register(domain_jieru, MyModelAdmin)