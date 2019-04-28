# -*- coding: utf-8 -*-
from base64 import b32encode
from hashlib import sha1
from random import random
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import datetime, time
'''
公共函数部分
'''

##生成一个8位随机数
def pkgen():
	rude = ('vcg',)
	bad_pk = True
	while bad_pk:
		pk = b32encode(sha1(str(random())).digest()).lower()[:8]
		bad_pk = False
		for rw in rude:
			if pk.find(rw) >= 0: bad_pk = True
	return pk


##实现分页
def page_info(request, v_keys, limit):
	paginator = Paginator(v_keys, limit)
	page = request.GET.get('page')

	try:
		list_page = paginator.page(page)
	except PageNotAnInteger:
		list_page = paginator.page(1)
	except EmptyPage:
		list_page = paginator.page(paginator.num_pages)

	return list_page

##字符串时间转换成时间戳
def string2timestamp(strValue):
    try:        
        d = datetime.datetime.strptime(strValue, "%Y%m%d%H%M%S")
        t = d.timetuple()
        timeStamp = int(time.mktime(t))
        timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond))/1000000
        return timeStamp
    except ValueError as e:
        print e
        d = datetime.datetime.strptime(strValue, "%Y%m%d%H%M%S")
        t = d.timetuple()
        timeStamp = int(time.mktime(t))
        timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond))/1000000
        return timeStamp


def timestamp2string(timeStamp):
    try:
        d = datetime.datetime.fromtimestamp(timeStamp)
        str1 = d.strftime("%Y-%m-%d %H:%M:%S.%f")
        # 2015-08-28 16:43:37.283000'
        return str1
    except Exception as e:
        print e
        return ''