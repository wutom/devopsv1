运维管理系统简介
一:版本说明
	1.django1.11
	2.5.5.56-MariaDB
	3.python 2.7.5
	4.bootstrap 3.3.7
二:安装说明
	1.基础软件请自行安装
	2.创建目录/opt/opsdev 
	3.django 创建应用修改必要的配置文件 settings.py 数据库部分即可
	4.Nginx配置示例
#################导航部分由nginx代理完成
server {
    listen 80;
    server_name servername;
	index index.html;

	location / {
         proxy_pass  http://127.0.0.1:8080;
         proxy_set_header   Host             $host:80;
         proxy_set_header   X-Real-IP        $remote_addr;
         proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
         #proxy_set_header 	Via    "ops";
         }
	location /static {
		root /opt/ops/opsdev/;
		autoindex on;
		}

	location /upload {
		root /opt/ops/opsdev/;
		autoindex on;
		}
}
#######################
	
三:功能说明
	1.工单部分实行了资源申请, 应用程序申请, FTP账户申请。
	2.应用管理前台展示了应用程序列表。
	3.资源管理是依赖redis数据,请使用云API将云资源数据汇总到redis总。
	4.入库FTP账户申请管理和FTP账户管理依赖Salt实现。
	5.前台由LDAP统一认证登陆

四:模块介绍
	1.api 调用各种接口的函数模块
	2.config 主配置函数模块
	3.index 首页
	4.itmessage it资源模块
	5.itresource it资源申请工单
	6.static 静态文件
	7.supplier 入库FTP账户模块
	8.templates 静态模板
	9.upload 文档上传存放目录