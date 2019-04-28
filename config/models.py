# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.db import models

#python 3 兼容2添加
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.

##import apps

##文档管理

class doc_info(models.Model):
    name = models.CharField(u'文档标题', max_length=20, blank=False, null=False)
    doc_url = models.FileField(u'文档路径', upload_to='img/', blank=False, null=False)
    remark = models.TextField(u'文档备注', max_length=256, blank = True, null = True)

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = verbose_name_plural = u'公司文档'
        db_table = 'doc_info'

##首页导航栏
@python_2_unicode_compatible
class nav_types(models.Model):
    name = models.CharField(u'类型名称', max_length = 20)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = verbose_name_plural = u'导航类型' 
        db_table = 'nav_types'

@python_2_unicode_compatible
class nav_info(models.Model):
    name = models.CharField(u'导航名称', max_length=48, blank=False, null=False)
    types = models.ForeignKey(nav_types, verbose_name = u'导航类型', blank=False, null=False)
    navurl = models.URLField(u'导航地址', blank = False, null=False)
    remark = models.TextField(u'备注信息', max_length=256, blank = True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = verbose_name_plural = u'导航管理'
        db_table = 'nav_info'


##邮件配置表
@python_2_unicode_compatible
class mail_info(models.Model):
    send= models.EmailField(u'发件地址', max_length=254, blank=False, null=False)
    passwd= models.CharField(u'邮箱密码', max_length=48, blank=False, null=False)
    server = models.URLField(u'发送地址', blank = False, null=False)
    port = models.IntegerField(u'发送端口', default = 465, blank=False, null=False)
    head = models.CharField(u'邮件标题', max_length=48, blank=False, null=False)
    remark = models.CharField(u'地址备注', max_length=24, blank=False, null=False)
    mail_remark = models.TextField(u'备注信息', max_length=256, blank = True, null=True)

    def __str__(self):
        return self.send
    class Meta:
        verbose_name = verbose_name_plural = u'邮件配置'
        db_table = 'mail_info'

##应用程序和子账户关系表
@python_2_unicode_compatible
class Structure_appname(models.Model):
    apppname = models.CharField(u'应用名称', max_length=48)
    def __str__(self):
        return self.apppname
    class Meta:
        verbose_name = verbose_name_plural = u'应用名称'
        db_table = 'Structure_appname'
#
@python_2_unicode_compatible
class Structure_data_id(models.Model):
    data_id = models.CharField(u'RDS或Redis-ID', max_length=48)
    def __str__(self):
        return self.data_id
    class Meta:
        verbose_name = verbose_name_plural = u'RDS或Redis-ID'
        db_table = 'Structure_data_id'
#
@python_2_unicode_compatible
class Structure_accesskey_id(models.Model):
    accesskey_id = models.CharField(u'AccesskeyID', max_length=48)
    accesskey_user = models.CharField(u'账户名称', max_length=48)
    accesskey_uid = models.CharField(u'账户UID', max_length=48)
    def __str__(self):
        return self.accesskey_id
    class Meta:
        verbose_name = verbose_name_plural = u'AccesskeyID'
        db_table = 'Structure_accesskey_id'

@python_2_unicode_compatible
class Structure_project(models.Model):
    project = models.CharField(u'归属项目', max_length=24)
    def __str__(self):
        return self.project
    class Meta:
        verbose_name = verbose_name_plural = u'归属项目'
        db_table = 'Structure_project'

@python_2_unicode_compatible
class Itres_department(models.Model):
   department = models.CharField(u'申请部门', max_length=24)
   def __str__(self):
       return self.department
   class Meta:
       verbose_name = verbose_name_plural = u'申请部门'
       db_table = 'Itres_department'

@python_2_unicode_compatible
class env_types(models.Model):
    env = models.CharField(u'部署环境', max_length=24)
    def __str__(self):
        return self.env
    class Meta:
        verbose_name = verbose_name_plural = u'部署环境'
        db_table = 'env_types'

@python_2_unicode_compatible
class app_types(models.Model):
    app = models.CharField(u'应用类型', max_length=24)
    def __str__(self):
        return self.app
    class Meta:
        verbose_name = verbose_name_plural = u'应用类型'
        db_table = 'app_types'

@python_2_unicode_compatible
class code_types(models.Model):
    code = models.CharField(u'语言类型', max_length=24)
    def __str__(self):
        return self.code
    class Meta:
        verbose_name = verbose_name_plural = u'语言类型'
        db_table = 'code_types'

@python_2_unicode_compatible
class app_status(models.Model):
    status = models.CharField(u'应用状态', max_length=24)
    def __str__(self):
        return self.status
    class Meta:
        verbose_name = verbose_name_plural = u'应用状态'
        db_table = 'app_status'


#应用程序和子账户关系表--------------------
@python_2_unicode_compatible
class Structure_info(models.Model):
    owner = models.CharField(u'使用者', max_length=48, blank=False, null=False)
    owner_email = models.EmailField(u'使用者Email', blank=False, null=False)
    appname = models.ForeignKey(Structure_appname, verbose_name = u'应用名', blank=False, null=False)
    project = models.ForeignKey(Structure_project, verbose_name = u'归属项目', blank=False, null=False)
    app_remark = models.CharField(u'应用名备注说明', max_length=48, blank=False, null=False)
    data_id = models.ForeignKey(Structure_data_id, verbose_name = u'RDS或Redis-ID', blank=False, null=False)
    data_user= models.CharField(u'RDS或Redis用户名', max_length=48, blank=False, null=False)
    data_remark= models.CharField(u'RDS或Redis备注说明', max_length=96, blank=False, null=False)
    accesskey_id = models.ForeignKey(Structure_accesskey_id, verbose_name = u'AccesskeyID', blank=False, null=False)
    accesskey_remark = models.CharField(u'AccesskeyID备注说明', max_length=96, blank=False, null=False)
    oss_remark = models.TextField(u'OSS操作对象说明', max_length=256, blank=False, null=False)
    mail_remark = models.TextField(u'备注信息', max_length=256, blank = True, null=True)

    def __str__(self):
        return self.owner
    class Meta:
        verbose_name = verbose_name_plural = u'应用关系'
        db_table = 'Structure_info'

#应用程序管理
@python_2_unicode_compatible
class App_info(models.Model):
    owner = models.CharField(u'使用者', max_length=48, blank=False, null=False)
    owner_email = models.EmailField(u'使用者Email', blank=False, null=False)
    project = models.ForeignKey(Structure_project, verbose_name = u'归属项目',  blank=False, null=False)
    Itres_department = models.ForeignKey(Itres_department, verbose_name = u'申请部门',  blank=False, null=False)
    env_types = models.ForeignKey(env_types, verbose_name = u'部署环境',  blank=False, null=False)
    app_types = models.ForeignKey(app_types, verbose_name = u'应用类型',  blank=False, null=False)
    code_types = models.ForeignKey(code_types, verbose_name = u'语言类型', blank=False, null=False)
    appname = models.ForeignKey(Structure_appname, verbose_name = u'应用名', blank=False, null=False)
    app_status = models.ForeignKey(app_status, verbose_name = u'应用状态',  blank=False, null=False)
    app_remark = models.CharField(u'应用名备注说明', max_length=48, blank=False, null=False)
    code_addr = models.CharField(u'代码地址', max_length=48, blank=False, null=False)
    domain = models.URLField(u'域名地址', max_length=96, blank=False, null=False)
    port = models.CharField(u'启动端口', max_length=8, blank=False, null=False)
    amount = models.CharField(u'数量', max_length=8, blank=False, null=False)
    data_id = models.ForeignKey(Structure_data_id, verbose_name = u'RDS或Redis-ID', blank=False, null=False)
    data_user= models.CharField(u'RDS或Redis用户名', max_length=48, blank=False, null=False)
    data_remark= models.CharField(u'RDS或Redis备注说明', max_length=96, blank=False, null=False)
    accesskey_id = models.ForeignKey(Structure_accesskey_id, verbose_name = u'AccesskeyID', blank=False, null=False)
    accesskey_remark = models.CharField(u'AccesskeyID备注说明', max_length=96, blank=False, null=False)
    oss_remark = models.TextField(u'OSS操作对象说明', max_length=256, blank=False, null=False)
    mail_remark = models.TextField(u'备注信息', max_length=256, blank = True, null=True)

    def __str__(self):
        return self.owner
    class Meta:
        verbose_name = verbose_name_plural = u'应用程序'
        db_table = 'App_info'


#域名管理部分
@python_2_unicode_compatible
class domain_owner(models.Model):
    beian = models.CharField(u'备案号主号', max_length=48)
    owner = models.CharField(u'域名持有者', max_length=48)
    num = models.CharField(u'证件号', max_length=48)
    phone = models.CharField(u'电话', max_length=48)
    email = models.EmailField(u'Email', blank=True, null=True)
    remark = models.TextField(u'备注信息', max_length=256, blank = True, null=True)
    def __str__(self):
        return self.beian
    class Meta:
        verbose_name = verbose_name_plural = u'备案号主号'
        db_table = 'domain_owner'

@python_2_unicode_compatible
class domain_supplier(models.Model):
    name = models.CharField(u'注册商', max_length=48)
    addr = models.CharField(u'管理地址', max_length=48)
    user = models.CharField(u'用户名', max_length=48)
    passwd = models.CharField(u'密码', max_length=48)
    remark = models.TextField(u'备注信息', max_length=256, blank = True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = verbose_name_plural = u'注册商'
        db_table = 'domain_supplier'

@python_2_unicode_compatible
class domain_dns(models.Model):
    name = models.CharField(u'解析平台', max_length=48)
    addr = models.CharField(u'管理地址', max_length=48)
    user = models.CharField(u'用户名', max_length=48)
    passwd = models.CharField(u'密码', max_length=48)
    remark = models.TextField(u'备注信息', max_length=256, blank = True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = verbose_name_plural = u'注册商'
        db_table = 'domain_dns'


@python_2_unicode_compatible
class domain_manager(models.Model):
    name = models.CharField(u'网站负责人', max_length=48)
    num = models.CharField(u'证件号', max_length=48)
    phone = models.CharField(u'电话', max_length=48)
    email = models.EmailField(u'Email', blank=False, null=False)
    remark = models.TextField(u'备注信息', max_length=256, blank = True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = verbose_name_plural = u'网站负责人'
        db_table = 'domain_manager'

@python_2_unicode_compatible
class domain_jieru(models.Model):
    name = models.CharField(u'备案接入商', max_length=48)
    addr = models.CharField(u'管理地址', max_length=48)
    user = models.CharField(u'用户名', max_length=48)
    passwd = models.CharField(u'密码', max_length=48)
    remark = models.TextField(u'备注信息', max_length=256, blank = True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = verbose_name_plural = u'备案接入商'
        db_table = 'domain_jieru'

@python_2_unicode_compatible
class domain_info(models.Model):
    domian = models.URLField(u'域名', max_length=96, blank=False, null=False)
    expire = models.DateTimeField(u'到期时间')
    owner = models.ForeignKey(domain_owner, verbose_name = u'备案号主号', null=True)
    supplier = models.ForeignKey(domain_supplier, verbose_name = u'注册商', null=True)
    beian_id= models.CharField(u'备案编号', max_length=48, null=True)
    beian_ip= models.CharField(u'备案IP', max_length=48, null=True)
    manager = models.ForeignKey(domain_manager, verbose_name = u'网站负责人', null=True)
    beian_jieru = models.ForeignKey(domain_jieru, verbose_name = u'备案接入商', null=True)
    domain_dns = models.ForeignKey(domain_dns, verbose_name = u'解析管理平台', null=True)
    remark = models.TextField(u'备注信息', max_length=256, blank = True, null=True)

    def __str__(self):
        return self.domian
    class Meta:
        verbose_name = verbose_name_plural = u'域名管理'
        db_table = 'domain_info'

