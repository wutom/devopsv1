# -*- coding: utf-8 -*-

from aliyunsdkcore.client import AcsClient
import redis,json,sys
import config.config as Config
import urllib3
urllib3.disable_warnings()

class Cloud(object):
    def __init__(self, region=None):

        self.access_key = Config.configs['AliAK']['AccessKey']
        self.access_secret = Config.configs['AliAK']['AccessKeySecret']
        self.redis_host = Config.configs['redis']['RedisHost']
        self.redis_port = Config.configs['redis']['RedisPort']
        self.secret_id = Config.configs['TxAK']['secretId']
        self.secret_key = Config.configs['TxAK']['secretKey']
        self.region = "cn-beijing"

        try:
            assert isinstance(self.redis_port, object)
            self.conn = redis.Redis(host=self.redis_host, port=self.redis_port)
        except BaseException as e:
            return e.message

    #def ErrorOut(self,message = None):

    def update_Ali_Ecs(self):
        try:
            from aliyunsdkcore.acs_exception.exceptions import ClientException
            from aliyunsdkcore.acs_exception.exceptions import ServerException
            from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
            Ali_Ecs_Info = {}
            client = AcsClient(self.access_key, self.access_secret, self.region);
            request = DescribeInstancesRequest.DescribeInstancesRequest()
            request.set_PageSize(100)
            response = client.do_action_with_exception(request)
            EcsInfo = json.loads(response.decode('utf-8'))
            PageCount = int(EcsInfo['TotalCount'] // EcsInfo['PageSize']) + 1

            for PageNumber in range(1, PageCount + 1):
                request.set_PageNumber(PageNumber)
                response = client.do_action_with_exception(request)
                EcsInfo = json.loads(response.decode('utf-8'))
                for InstanceInfo in EcsInfo['Instances']['Instance']:
                    Ali_Ecs_Info[InstanceInfo['InstanceId']] = InstanceInfo
            return self.conn.set('Ali_Ecs_Info', json.dumps(Ali_Ecs_Info))
        except BaseException as e:
            return e.message

    def update_Ali_Rds(self):
        try:
            from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest
            from aliyunsdkrds.request.v20140815 import DescribeDBInstanceAttributeRequest
            Ali_Rds_Info = {}
            client = AcsClient(self.access_key, self.access_secret, self.region);
            request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
            request.set_PageSize(100)
            response = client.do_action_with_exception(request)
            RdsInfo = json.loads(response)

            for DBInstance in RdsInfo['Items']['DBInstance']:
                request = DescribeDBInstanceAttributeRequest.DescribeDBInstanceAttributeRequest()
                request.set_DBInstanceId(DBInstance['DBInstanceId'])
                response = client.do_action_with_exception(request)
                Ali_Rds_Info[DBInstance['DBInstanceId']] = \
                json.loads(response.decode('utf-8'))['Items']['DBInstanceAttribute'][0]
            return self.conn.set('Ali_Rds_Info', json.dumps(Ali_Rds_Info))
        except BaseException as e:
            return e.message

    def update_Ali_Slb(self):
        try:
            from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest
            from aliyunsdkslb.request.v20140515 import DescribeLoadBalancerAttributeRequest
            Ali_Slb_Info = {}
            client = AcsClient(self.access_key, self.access_secret, self.region);
            request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
            response = client.do_action_with_exception(request)
            SLBInfo = json.loads(response)

            for SLBInstance in SLBInfo['LoadBalancers']['LoadBalancer']:
                request = DescribeLoadBalancerAttributeRequest.DescribeLoadBalancerAttributeRequest()
                request.set_LoadBalancerId(SLBInstance['LoadBalancerId'])
                response = client.do_action_with_exception(request)
                Ali_Slb_Info[SLBInstance['LoadBalancerId']] = json.loads(response.decode('utf-8'))
            return self.conn.set('Ali_Slb_Info', json.dumps(Ali_Slb_Info))
        except BaseException as e:
            return e.message

    def update_Ali_Waf(self):
        try:
            from api.ali.AliOpenApi import AliWaf
            api_url = "https://wafopenapi.cn-hangzhou.aliyuncs.com"
            instance_id = "waf-n66fqwzdegfi"
            api_version = "2018-01-17"
            region = "cn"
            Ali_Waf_Info = {}
            t = AliWaf(api_url=api_url, ak=self.access_key, sk=self.access_secret, api_version=api_version, instance_id=instance_id, region=region)
            respon = t.DescribeDomainNames()
            if respon['code'] == 200:
                domain_list = json.loads(respon['data'])['Result']['DomainNames']
                for domain in domain_list:
                    domain_info = t.DescribeDomainConfig(domain=domain)
                    if domain_info['code'] == 200:
                        Ali_Waf_Info[domain] = json.loads(domain_info['data'])
            return self.conn.set('Ali_Waf_Info', json.dumps(Ali_Waf_Info))
        except BaseException as e:
            return e.message

    def update_Ali_Cs(self):
        try:
            from aliyunsdkcs.request.v20151215 import DescribeClustersRequest
            from aliyunsdkcs.request.v20151215 import GetClusterProjectsRequest
            client = AcsClient(self.access_key, self.access_secret, self.region);
            request = DescribeClustersRequest.DescribeClustersRequest()
            status, header, res = client.get_response(request)
            Ali_Cs_Info = {}
            for cluster_info in json.loads(res):
                cluster_name = cluster_info['name']
                cluster_type = cluster_info['cluster_type']
                cluster_id = cluster_info['cluster_id']
                if cluster_type == 'Kubernetes':
                    continue
                else:
                    request = GetClusterProjectsRequest.GetClusterProjectsRequest()
                    request.set_ClusterId(cluster_id)
                    status, header, res = client.get_response(request)
                    cluster_info['applications'] = json.loads(res)
                    Ali_Cs_Info[cluster_name] = cluster_info
            return self.conn.set('Ali_Cs_Info', json.dumps(Ali_Cs_Info))
        except BaseException as e:
            return e.message

    def update_Ali_Oss(self):
        try:
            import os
            import oss2
            Ali_Oss_Info = {}
            access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', Config.configs['AliAK']['AccessKey'])
            access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', Config.configs['AliAK']['AccessKeySecret'])
            endpoint = os.getenv('OSS_TEST_ENDPOINT', 'oss-cn-beijing.aliyuncs.com')
            service = oss2.Service(oss2.Auth(access_key_id, access_key_secret), endpoint)
            for info in oss2.BucketIterator(service):
                oss_info = {}
                bucket_name = os.getenv('OSS_TEST_BUCKET', info.name)
                bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
                bucket_info = bucket.get_bucket_info()
                oss_info['name'] = bucket_info.name
                oss_info['storage_class'] = bucket_info.storage_class
                oss_info['creation_date'] = bucket_info.creation_date
                oss_info['intranet_endpoint'] = bucket_info.intranet_endpoint
                oss_info['extranet_endpoint'] = bucket_info.extranet_endpoint
                oss_info['owner'] = bucket_info.owner.id
                oss_info['grant'] = bucket_info.acl.grant
                Ali_Oss_Info[bucket_name] = oss_info
            return self.conn.set('Ali_Oss_Info', json.dumps(Ali_Oss_Info))
        except BaseException as e:
            return e.message

    def update_Ali_Ram(self):
        try:
            from aliyunsdkram.request.v20150501 import ListUsersRequest
            from aliyunsdkram.request.v20150501 import GetUserRequest
            from aliyunsdkram.request.v20150501 import ListAccessKeysRequest
            from aliyunsdkram.request.v20150501 import ListPoliciesForUserRequest
            client = AcsClient(self.access_key, self.access_secret, self.region);
            Ali_Ram_Info = {}
            request = ListUsersRequest.ListUsersRequest()
            response = client.do_action_with_exception(request)
            RamInfo = json.loads(response.decode('utf-8'))
            for Ram_User_Info in RamInfo['Users']['User']:
                # RAM用户信息
                request = GetUserRequest.GetUserRequest()
                request.set_UserName(Ram_User_Info['UserName'])
                response = client.do_action_with_exception(request)
                RamUserInfo = json.loads(response.decode('utf-8'))['User']
                # RAM用户AK
                request = ListAccessKeysRequest.ListAccessKeysRequest()
                request.set_UserName(Ram_User_Info['UserName'])
                response = client.do_action_with_exception(request)
                RamUserInfo['AccessKey'] = json.loads(response.decode('utf-8'))['AccessKeys']['AccessKey']
                # RAM用户权限
                request = ListPoliciesForUserRequest.ListPoliciesForUserRequest()
                request.set_UserName(Ram_User_Info['UserName'])
                response = client.do_action_with_exception(request)
                RamUserInfo['Policy'] = json.loads(response.decode('utf-8'))['Policies']['Policy']

                Ali_Ram_Info[Ram_User_Info['UserName']] = RamUserInfo
            return self.conn.set('Ali_Ram_Info', json.dumps(Ali_Ram_Info))
        except BaseException as e:
            return e.message

    def update_Tx_Cns(self):
        try:
            from QcloudApi.qcloudapi import QcloudApi
            module = 'cns'
            action = 'DomainList'
            config = {
                'secretId': self.secret_id,
                'secretKey': self.secret_key,
                'method': 'GET',
                'SignatureMethod': 'HmacSHA1',
                'Version': '2017-03-12'
            }
            action_params = {
                'length': 100
            }
            Tx_Cns_Info = {}
            service = QcloudApi(module, config)
            respon = json.loads(service.call(action, action_params))
            for donmains in respon['data']['domains']:
                action = 'RecordList'
                action_params = {
                    'domain': donmains['name'],
                    'qProjectId': -1
                }
                service = QcloudApi(module, config)
                respon = json.loads(service.call(action, action_params))
                Tx_Cns_Info[respon['data']['domain']['name']] = respon['data']
            return self.conn.set('Tx_Cns_Info', json.dumps(Tx_Cns_Info))
        except BaseException as e:
            return e.message

    def update_Jenkins_Builds_Pro(self):
        try:
            import requests
            res = requests.get("http://jenkins-manage.vcg.com/pro_deploy_history.txt")
            builds_history_pro = []
            for line in res.text.split('\n'):
                if line == '':
                    break
                builds_history_dict = {}
                for line_line in line.split(','):
                    builds_history_dict[line_line.split(':')[0]] = line_line.split(':')[1]
                builds_history_pro.append(builds_history_dict)
            builds_history_pro.reverse()
            return self.conn.set('Jenkins_Builds_Pro_Info', json.dumps(builds_history_pro))
        except BaseException as e:
            return e.message

    def update_Jenkins_Builds_Pre(self):
        try:
            import requests
            res = requests.get("http://jenkins-manage.vcg.com/pre_deploy_history.txt")
            builds_history_pre = []
            for line in res.text.split('\n'):
                if line == '':
                    break
                builds_history_dict = {}
                for line_line in line.split(','):
                    builds_history_dict[line_line.split(':')[0]] = line_line.split(':')[1]
                    builds_history_pre.append(builds_history_dict)
                builds_history_pre.reverse()
            return self.conn.set('Jenkins_Builds_Pre_Info', json.dumps(builds_history_pre))
        except BaseException as e:
            return e.message

    def update_All(self):
        self.update_Ali_Cs()
        self.update_Ali_Ecs()
        self.update_Ali_Oss()
        self.update_Ali_Ram()
        self.update_Ali_Rds()
        self.update_Ali_Slb()
        self.update_Ali_Waf()
        self.update_Tx_Cns()
        self.update_Jenkins_Builds_Pre()
        self.update_Jenkins_Builds_Pro()


    def get_Ali_Waf(self):
        if self.conn.get('Ali_Waf_Info') == None:
            return 'Redis中无此Key'
        else:
            try:
                Ali_Waf_Info = json.loads(self.conn.get('Ali_Waf_Info'))
                domain_info_list = []
                for domain in Ali_Waf_Info.keys():
                    domain_info = {}
                    domain_info['SourceIps'] = Ali_Waf_Info[domain]['Result']['DomainConfig']['SourceIps']
                    domain_info['Cname'] = Ali_Waf_Info[domain]['Result']['DomainConfig']['Cname']
                    domain_info['Name'] = domain
                    domain_info_list.append(domain_info)
                return domain_info_list
            except BaseException as e:
                return e.message

    def get_Ali_Ecs_List(self):
        if self.conn.get('Ali_Ecs_Info') == None:
            return 'Redis中无此Key'
        else:
            EcsDatas = json.loads(self.conn.get('Ali_Ecs_Info'))
            EcsDataList = []
            try:
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
                            NewEcsData['InnerIpAddress'] = \
                            EcsData.get('VpcAttributes').get('PrivateIpAddress').get('IpAddress')[0]
                        except IndexError as e:
                            NewEcsData['InnerIpAddress'] = None
                        try:
                            NewEcsData['PublicIpAddress'] = EcsData.get('PublicIpAddress').get('IpAddress')[0]
                        except IndexError as e:
                            NewEcsData['PublicIpAddress'] = None
                    EcsDataList.append(NewEcsData)
                return EcsDataList
            except BaseException as e:
                return e.message

    def get_Ali_Ecs_Detail(self):
        if self.conn.get('Ali_Ecs_Info') == None:
            return 'Redis中无此Key'
        else:
            try:
                EcsDatas = json.loads(self.conn.get('Ali_Ecs_Info'))
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
                            NewEcsData['InnerIpAddress'] = \
                            EcsData.get('VpcAttributes').get('PrivateIpAddress').get('IpAddress')[0]
                        except IndexError as e:
                            NewEcsData['InnerIpAddress'] = None
                        try:
                            NewEcsData['PublicIpAddress'] = EcsData.get('PublicIpAddress').get('IpAddress')[0]
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
            except BaseException as e:
                return e.message

    def get_Ali_Rds_List(self):
        if self.conn.get('Ali_Rds_Info') == None:
            return 'Redis中无此Key'
        else:
            try:
                RdsDatas = json.loads(self.conn.get('Ali_Rds_Info'))
                RdsDataList = []
                for RdsData in RdsDatas.values():
                    NewRdsData = {}
                    NewRdsData['DBInstanceId'] = RdsData['DBInstanceId']
                    NewRdsData['DBInstanceDescription'] = RdsData.get('DBInstanceDescription')
                    NewRdsData['ConnectionString'] = RdsData['ConnectionString']
                    RdsDataList.append(NewRdsData)
                return RdsDataList
            except BaseException as e:
                return e.message

    def get_Ali_Rds_Detail(self):
        if self.conn.get('Ali_Rds_Info') == None:
            return 'Redis中无此Key'
        else:
            try:
                RdsDatas = json.loads(self.conn.get('Ali_Rds_Info'))
                RdsDatasDetail = {}
                for RdsData in RdsDatas.values():
                    NewRdsData = {}
                    datas = ['DBInstanceId', 'DBInstanceDescription', 'ConnectionString', 'ZoneId', 'Port',
                             'DBInstanceStorageType', 'DBInstanceCPU',
                             'MaxConnections', 'Engine', 'EngineVersion', 'DBInstanceStatus', 'MaxIOPS', 'DBInstanceClass',
                             'DBInstanceStorage', 'CreationTime', 'ExpireTime',
                             'DBInstanceMemory']
                    for data in datas:
                        NewRdsData[data] = RdsData[data]
                    RdsDatasDetail[NewRdsData['DBInstanceId']] = NewRdsData
                return RdsDatasDetail
            except BaseException as e:
                return e.message

    def get_Ali_Slb_List(self):
        if self.conn.get('Ali_Slb_Info') == None:
            return 'Redis中无此Key'
        else:
            try:
                SlbDatas = json.loads(self.conn.get('Ali_Slb_Info'))
                SlbDataList = []
                for SlbData in SlbDatas.values():
                    NewSlbData = {}
                    NewSlbData['LoadBalancerId'] = SlbData['LoadBalancerId']
                    NewSlbData['LoadBalancerName'] = SlbData.get('LoadBalancerName')
                    NewSlbData['Address'] = SlbData['Address']
                    NewSlbData['ListenerPort'] = SlbData['ListenerPorts']['ListenerPort']
                    SlbDataList.append(NewSlbData)
                return SlbDataList
            except BaseException as e:
                return e.message

    def get_Ali_Slb_Detail(self):
        if self.conn.get('Ali_Slb_Info') == None:
            return 'Redis中无此Key'
        else:
            try:
                SlbDatas = json.loads(self.conn.get('Ali_Slb_Info'))
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
                    SlbDatasDetail[NewSlbData['LoadBalancerId']] = NewSlbData
                return SlbDatasDetail
            except BaseException as e:
                return e.message

    def get_Tx_Cns_List(self):
        if self.conn.get('Tx_Cns_Info') == None:
            return 'Redis中无此Key'
        else:
            try:
                CnsDatas = json.loads(self.conn.get('Tx_Cns_Info'))
                Cnslist = []
                for CnsData in CnsDatas.values():
                    NewCnsData = {}
                    NewCnsData['name'] = CnsData['domain']['name']
                    NewCnsData['grade'] = CnsData['domain']['grade']
                    NewCnsData['owner'] = CnsData['domain']['owner']
                    NewCnsData['id'] = CnsData['domain']['id']
                    NewCnsData['sub_domains'] = CnsData['info']['sub_domains']
                    NewCnsData['id'] = CnsData['domain']['id']
                    NewCnsData['status'] = CnsData['domain']['status']
                    Cnslist.append(NewCnsData)
                return Cnslist
            except BaseException as e:
                return e.message

    def get_Tx_Cns_Detail(self):
        if self.conn.get('Tx_Cns_Info') == None:
            return 'Redis中无此Key'
        else:
            try:
                CnsDatas = json.loads(self.conn.get('Tx_Cns_Info'))
                CnsDetail = {}
                for CnsData in CnsDatas.values():
                    CnsDetail[CnsData['domain']['name']] = CnsData['records']
                return CnsDetail
            except BaseException as e:
                return e.message

    def get_Jenkins_Builds_Pro(self):
        if self.conn.get('Jenkins_Builds_Pro_Info') == None:
            return 'Redis中无此Key'
        else:
            builds_history_pro = json.loads(self.conn.get('Jenkins_Builds_Pro_Info'))
            return builds_history_pro

    def get_Jenkins_Builds_Pre(self):
        if self.conn.get('Jenkins_Builds_Pre_Info') == None:
            return 'Redis中无此Key'
        else:
            builds_history_pre = json.loads(self.conn.get('Jenkins_Builds_Pre_Info'))
            return builds_history_pre

    def get_Ali_Oss(self):
        if self.conn.get('Ali_Oss_Info') == None:
            return 'Redis中无此Key'
        else:
            try:
                OssDatas = json.loads(self.conn.get('Ali_Oss_Info'))
                return OssDatas.values()
            except BaseException as e:
                return e.message

    def get_Ali_Cs(self):
        if self.conn.get('Ali_Cs_Info') == None:
            return 'Redis中无此Key'
        else:
            try:
                CsDatas = json.loads(self.conn.get('Ali_Cs_Info'))
                clusters = []
                for cluster_name in CsDatas.keys():
                    cluster = {}
                    cluster_app_name = []
                    for applications in CsDatas[cluster_name]['applications']:
                        cluster_app_name.append(applications['name'])
                        cluster['name'] = cluster_name
                        cluster['applications'] = cluster_app_name
                    clusters.append(cluster)
                return clusters
            except BaseException as e:
                return e.message

    def get_Ali_Ram_List(self):
        if self.conn.get('Ali_Ram_Info') == None:
            return 'Redis中无此Key'
        else:
            try:
                RamDatas = json.loads(self.conn.get('Ali_Ram_Info'))
                RamDataList = []
                for RamData in RamDatas.values():
                    NewRamData = {}
                    NewRamData['UserName'] = RamData['UserName']
                    NewRamData['Comments'] = RamData['Comments']
                    NewRamData['DisplayName'] = RamData.get('DisplayName')
                    NewRamData['CreateDate'] = RamData['CreateDate']
                    RamDataList.append(NewRamData)
                return RamDataList
            except BaseException as e:
                return e.message

    def get_Ali_Ram_Detail(self):
        if self.conn.get('Ali_Ram_Info') == None:
            return 'Redis中无此Key'
        else:
            try:
                RamDatas = json.loads(self.conn.get('Ali_Ram_Info'))
                RamDataList = []
                for RamData in RamDatas.values():
                    NewRamData = {}
                    NewRamData['UserName'] = RamData['UserName']
                    NewRamData['Comments'] = RamData['Comments']
                    NewRamData['DisplayName'] = RamData.get('DisplayName')
                    NewRamData['CreateDate'] = RamData['CreateDate']
                    RamDataList.append(NewRamData)
                return RamDataList
            except BaseException as e:
                return e.message
