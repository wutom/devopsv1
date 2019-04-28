#!/usr/bin/env python
#encoding:utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancerAttributeRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstanceAttributeRequest
import redis,json

import sys
sys.path.append("..")
import config.config_default as Config

RegionId = "cn-beijing"
conn = redis.Redis(host=Config.configs['redis']['RedisHost'], port=Config.configs['redis']['RedisPort'])

def update_Ecs():
    Ecs_Info = {}
    client = AcsClient(Config.configs['AliAK']['AccessKey'],
                            Config.configs['AliAK']['AccessKeySecret'],
                            RegionId);
    request = DescribeInstancesRequest.DescribeInstancesRequest()
    request.set_PageSize(100)
    response = client.do_action_with_exception(request)
    EcsInfo = json.loads(response.decode('utf-8'))
    PageCount = int(EcsInfo['TotalCount'] // EcsInfo['PageSize']) + 1

    for PageNumber in range(1,PageCount+1):
        request.set_PageNumber(PageNumber)
        response = client.do_action_with_exception(request)
        EcsInfo = json.loads(response.decode('utf-8'))
        for InstanceInfo in EcsInfo['Instances']['Instance']:
            Ecs_Info[InstanceInfo['InstanceId']] = InstanceInfo
    conn.set('Ecs_Info',json.dumps(Ecs_Info))

def update_Rds():
    Rds_Info = {}
    client = AcsClient(Config.configs['AliAK']['AccessKey'],
                       Config.configs['AliAK']['AccessKeySecret'],
                       RegionId);
    request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
    request.set_PageSize(100)
    response = client.do_action_with_exception(request)
    RdsInfo = json.loads(response)

    for DBInstance in RdsInfo['Items']['DBInstance']:
        request = DescribeDBInstanceAttributeRequest.DescribeDBInstanceAttributeRequest()
        request.set_DBInstanceId(DBInstance['DBInstanceId'])
        response = client.do_action_with_exception(request)
        Rds_Info[DBInstance['DBInstanceId']] = json.loads(response.decode('utf-8'))['Items']['DBInstanceAttribute'][0]

    conn.set('Rds_Info', json.dumps(Rds_Info))

def update_Slb():
    Slb_Info = {}
    client = AcsClient(Config.configs['AliAK']['AccessKey'],
                       Config.configs['AliAK']['AccessKeySecret'],
                       RegionId);
    request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
    response = client.do_action_with_exception(request)
    SLBInfo = json.loads(response)

    for SLBInstance in SLBInfo['LoadBalancers']['LoadBalancer']:
        request = DescribeLoadBalancerAttributeRequest.DescribeLoadBalancerAttributeRequest()
        request.set_LoadBalancerId(SLBInstance['LoadBalancerId'])
        response = client.do_action_with_exception(request)
        Slb_Info[SLBInstance['LoadBalancerId']] = json.loads(response.decode('utf-8'))

    conn.set('Slb_Info', json.dumps(Slb_Info))

def get_Ecs_List():
    EcsDatas=json.loads(conn.get('Ecs_Info'))
    EcsDataList = []
    for EcsData in EcsDatas.values():
        NewEcsData = {}
        NewEcsData['InstanceId'] = EcsData['InstanceId']
        NewEcsData['InstanceName'] = EcsData.get('InstanceName')
        NewEcsData['InstanceNetworkType'] = EcsData.get('InstanceNetworkType')
        if EcsData['InstanceNetworkType'] == 'classic':
            try:
                NewEcsData['InnerIpAddress'] = EcsData.get('InnerIpAddress').get('IpAddress')[0]
            except IndexError as e:
                NewEcsData['InnerIpAddress'] = None
            try:
                NewEcsData['PublicIpAddress'] = EcsData.get('PublicIpAddress').get('IpAddress')[0]
            except IndexError as e:
                NewEcsData['PublicIpAddress'] = None
        else:
            try:
                NewEcsData['InnerIpAddress'] = EcsData['VpcAttributes']['PrivateIpAddress']['IpAddress'][0]
            except IndexError as e:
                NewEcsData['InnerIpAddress'] = None
            try:
                NewEcsData['PublicIpAddress'] = EcsData['EipAddress']['IpAddress']
            except IndexError as e:
                NewEcsData['PublicIpAddress'] = None
        EcsDataList.append(NewEcsData)
    return EcsDataList

def get_Ecs_Detail():
    EcsDatas=json.loads(conn.get('Ecs_Info'))
    EcsDatasDetail = {}
    for EcsData in EcsDatas.values():
        NewEcsData = {}
        NewEcsData['InstanceId'] = EcsData['InstanceId']
        NewEcsData['InstanceName'] = EcsData.get('InstanceName')
        NewEcsData['InstanceNetworkType'] = EcsData['InstanceNetworkType']
        if EcsData['InstanceNetworkType'] == 'classic':
            try:
                NewEcsData['InnerIpAddress'] = EcsData.get('InnerIpAddress').get('IpAddress')[0]
            except IndexError as e:
                NewEcsData['InnerIpAddress'] = None
            try:
                NewEcsData['PublicIpAddress'] = EcsData.get('PublicIpAddress').get('IpAddress')[0]
            except IndexError as e:
                NewEcsData['PublicIpAddress'] = None
        else:
            try:
                NewEcsData['InnerIpAddress'] = EcsData.get('NetworkInterfaces').get('NetworkInterface')[0].get('PrimaryIpAddress')
            except IndexError as e:
                NewEcsData['InnerIpAddress'] = None
            try:
                NewEcsData['PublicIpAddress'] = EcsData.get('EipAddress').get('IpAddress')
            except IndexError as e:
                NewEcsData['PublicIpAddress'] = None
        NewEcsData['ZoneId'] = EcsData['ZoneId']
        NewEcsData['InstanceType'] = EcsData['InstanceType']
        NewEcsData['Status'] = EcsData['Status']
        NewEcsData['Description'] = EcsData['Description']
        NewEcsData['Cpu'] = EcsData['Cpu']
        NewEcsData['Memory'] = EcsData['Memory']
        NewEcsData['OSName'] = EcsData['OSName']
        NewEcsData['CreationTime'] = EcsData['CreationTime']
        NewEcsData['ExpiredTime'] = EcsData['ExpiredTime']
        EcsDatasDetail[NewEcsData['InstanceId']] = NewEcsData
    return EcsDatasDetail

def get_Rds_List():
    RdsDatas=json.loads(conn.get('Rds_Info'))
    RdsDataList = []
    for RdsData in RdsDatas.values():
        NewRdsData = {}
        NewRdsData['DBInstanceId'] = RdsData['DBInstanceId']
        NewRdsData['DBInstanceDescription'] = RdsData.get('DBInstanceDescription')
        NewRdsData['ConnectionString'] = RdsData['ConnectionString']
        RdsDataList.append(NewRdsData)
    return RdsDataList

def get_Rds_Detail():
    RdsDatas=json.loads(conn.get('Rds_Info'))
    RdsDatasDetail = {}
    for RdsData in RdsDatas.values():
        NewRdsData = {}
        datas = ['DBInstanceId','DBInstanceDescription','ConnectionString','ZoneId','Port','DBInstanceStorageType','DBInstanceCPU',
                'MaxConnections','Engine','EngineVersion','DBInstanceStatus','MaxIOPS','DBInstanceClass','DBInstanceStorage','CreationTime','ExpireTime',
                 'DBInstanceMemory']
        for data in datas:
            NewRdsData[data] = RdsData[data]
        RdsDatasDetail[NewRdsData['DBInstanceId']] = NewRdsData
    return RdsDatasDetail

def get_Slb_List():
    SlbDatas=json.loads(conn.get('Slb_Info'))
    SlbDataList = []
    for SlbData in SlbDatas.values():
        NewSlbData = {}
        NewSlbData['LoadBalancerId'] = SlbData['LoadBalancerId']
        NewSlbData['LoadBalancerName'] = SlbData.get('LoadBalancerName')
        NewSlbData['Address'] = SlbData['Address']
        NewSlbData['ListenerPort'] = SlbData['ListenerPorts']['ListenerPort']
        SlbDataList.append(NewSlbData)
    return SlbDataList

def get_Slb_Detail():
    SlbDatas = json.loads(conn.get('Slb_Info'))
    SlbDatasDetail = {}
    for SlbData in SlbDatas.values():
        NewSlbData = {}
        NewSlbData['LoadBalancerId'] = SlbData['LoadBalancerId']
        NewSlbData['LoadBalancerName'] = SlbData.get('LoadBalancerName')
        NewSlbData['Address'] = SlbData['Address']
        NewSlbData['AddressType'] = SlbData['AddressType']
        NewSlbData['ListenerPort'] = SlbData['ListenerPorts']['ListenerPort']
        NewSlbData['NetworkType'] = SlbData['NetworkType']
        NewSlbData['MasterZoneId'] = SlbData['MasterZoneId']
        NewSlbData['SlaveZoneId'] = SlbData['SlaveZoneId']
        NewSlbData['RegionId'] = SlbData['RegionId']
        NewSlbData['AddressType'] = SlbData['AddressType']
        NewSlbData['CreateTime'] = SlbData['CreateTime']
        NewSlbData['LoadBalancerStatus'] = SlbData['LoadBalancerStatus']
        #NewSlbData['BackendServerId'] = SlbData['BackendServers']['BackendServer']['ServerId']
        #NewSlbData['BackendServerWeight'] = SlbData['BackendServers']['BackendServer']['Weight']
        #NewSlbData['BackendServerType'] = SlbData['BackendServers']['BackendServer']['Type']
        SlbDatasDetail[NewSlbData['LoadBalancerId']] = NewSlbData
    return SlbDatasDetail