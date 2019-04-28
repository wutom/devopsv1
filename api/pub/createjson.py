# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json, time, re, os, sys, subprocess
from datetime import datetime as dat

###app models
from config.models import mail_info, Structure_info, Structure_appname, Structure_data_id, Structure_accesskey_id, Structure_project
from itmessage.models import Dev_info
from api.ali.cloud import Cloud as cloud
cloud = cloud()
from itmessage.models import Dev_info

os_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


###获取首页数据生成json文件
###初始化原始数据返回字典
def it_data():
    try:
        ali_rds = cloud.get_Ali_Rds_List()
        ali_ecs = cloud.get_Ali_Ecs_List()
        ali_slb = cloud.get_Ali_Slb_List()
        ten_dns = cloud.get_Tx_Cns_List()
        ali_ram = cloud.get_Ali_Ram_List()
        ali_waf = cloud.get_Ali_Waf()
        ali_oss = cloud.get_Ali_Oss()
        jenkins_list = cloud.get_Jenkins_Builds_Pro()
    except TypeError:
        ali_rds = {}
        ali_ecs = {}
        ali_slb = {}
        ali_ram = {}
        ten_dns = {}
        ali_waf = {}
        ali_oss = {}
        jenkins_list = {}

    dev = Dev_info.objects.count()
    pro = Structure_project.objects.count()
    dev_count = dev
    pro_count = pro

    v_list = {}
    v_list[u"设备数"] = dev_count
    v_list[u"项目数"] = pro_count
    v_list[u"负载均衡"] = len(ali_slb)
    v_list[u"虚拟主机"] = len(ali_ecs)
    v_list[u"数据库"] = len(ali_rds)
    v_list[u"云账户"] = len(ali_ram)
    v_list[u"防火墙"] = len(ali_waf)
    v_list[u"在线域名"] = len(ten_dns)
    v_list[u"OSS"] = len(ali_oss)

    return v_list

def jenkins_data():
    try:
        jenkins_list = cloud.get_Jenkins_Builds_Pro()
    except TypeError:
        jenkins_list = {}

    return jenkins_list


'''
start 柱状图汇总函数
'''
def charts_itdata(datadict):
    #charts_proportion 格式化字典到v_k 生产数据
    v_k = []
    v_d = []
    data = {}
    series = []
    series_dict = {}
    for i in datadict:
        v_d.append(datadict[i])
        v_k.append(i)
    series_dict['name'] = u'数量'
    series_dict['data'] = v_d
    series.append(series_dict)
    data['series'] = series
    data['categories'] = v_k
    return data


def charts_bar_json():
    #charts_pie_json 生产柱状图数据json文件
    dj = {}
    itdata = it_data()
    data = charts_itdata(datadict=itdata)
    dj['code'] = 0
    dj['result'] = 'true'
    dj['messge'] = 'success'
    dj['data'] = data
    jsonfile = os_path + "/static/json/bar_it.json"
    with open(jsonfile, "w") as f:
        json.dump(dj,f)
'''
end 柱状图汇总函数
'''


'''
start 饼形图汇总函数
'''
def charts_proportion(datadict):
    #charts_proportion 格式化字典到v_k 生产比例数据
    count =len(datadict)
    
    v_k = []
    for k in datadict:
        v_k.append(k['ServiceName'])

    d_k = {}
    for k in v_k:
        d_k[k] = d_k.get(k, 0) + 1

    v_list = []
    for k in d_k:
        v_dict = {}
        v_dict['category'] = k
        v_dict['value'] = float(int(d_k[k]))/float(count)*100
        v_list.append(v_dict)
    return v_list


def charts_pie_json():
    #charts_pie_json 生产饼形图数据json文件
    dj = {}
    jkdata = jenkins_data()
    data = charts_proportion(datadict=jkdata)
    dj['code'] = 0
    dj['result'] = 'true'
    dj['messge'] = 'success'
    dj['data'] = {'title': u'应用程序发版累计比例', 'series': data}
    jsonfile = os_path + "/static/json/pie_jenkins.json"
    with open(jsonfile, "w") as f:
        json.dump(dj,f)
'''
end 饼形图汇总函数
'''