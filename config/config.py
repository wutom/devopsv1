#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
这是api各个接口集中配置文件
'''

SQLDBCF={
	'dbname':'*****************',
	'dbuser':'*****************',
	'dbhost':'*****************',
	'passwd':'*****************'
}

LDAP={
	'ldhost':'ldap://localhost',
	'ldapdn':'ou=People,dc=vcg,dc=com',
	'lduser':'root',
	'ldpwd':'******',
}

###
configs = {
    'redis': {
        'RedisHost': 'localhost',
        'RedisPort': 6379,
    },
    'AliAK': {
        'AccessKey': '*******************',
        'AccessKeySecret' : '*******************',
    },
    'TxAK': {
        'secretId' : '*******************',
        'secretKey' :  '*******************',
    },
}
