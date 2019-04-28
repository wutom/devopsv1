#!/usr/bin/python
# -*- coding: utf-8 -*-
import ldap
#####根据linux python版本加载 pxssh
from pexpect import pxssh
#import pxssh
###加载api的主配置文件获取必要的参数
from config import config

'''
完成LDAP认证并返回值
'''


ldhost = config.LDAP['ldhost']
lduser = config.LDAP['lduser']
ldpwd = config.LDAP['ldpwd']
ldapdn = config.LDAP['ldapdn']

def ldap_getcn(name):
	try:
		ldap.set_option(ldap.OPT_REFERRALS,0)
		conn = ldap.initialize(ldhost)
		conn.protocol_version = ldap.VERSION3
		conn.simple_bind(lduser,ldpwd)
 
		Filter = "(&(|(cn=" + name + ")))"       
		ldap_result_id = conn.search(ldapdn,ldap.SCOPE_SUBTREE,Filter,None)

		result_data = conn.result(ldap_result_id,0)
		if result_data[1] == []:
			print "%s doesn't exist." % name
		else:
			LDID = result_data[1][0][0]
			return LDID
	except ldap.LDAPError, e:
		print e
		conn.unbind_s()

def LDAPlogin(username,password):
	try:
		ldap.set_option(ldap.OPT_REFERRALS,0)
		CN = ldap_getcn(username)
		login = ldap.initialize(ldhost)
		login.simple_bind_s(CN,password)
		login.unbind_s()
		return 'True'
	except Exception,e:
		return 'Flase'
