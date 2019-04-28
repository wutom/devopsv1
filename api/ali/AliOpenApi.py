#! /usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import urllib
import requests
import hmac
import random
import datetime
import sys

class AliOpenAPI(object):
    def __init__(self, signature_version='1.0', api_url=None, ak=None, sk=None, api_version=None):
        assert api_url is not None
        assert ak is not None
        assert sk is not None
        assert api_version is not None

        self.signature_once = 0
        self.signature_method = 'HMAC-SHA1'
        self.signature_version = signature_version
        self.api_version = api_version
        self.format = 'json'
        self.signature_method = 'HMAC-SHA1'
        self.api_url = api_url
        self.access_key = ak
        self.access_secret = sk

    def __gen_common_params(self, req_type, api_version, access_key, access_secret, http_params):
        while 1:
            rand_int = random.randint(10, 999999999)
            if rand_int != self.signature_once:
                self.signature_once = rand_int
                break

        # 当前步骤中是否含有AccessKey参数
        if access_key == None:
            return None

        http_params.append(('AccessKeyId', access_key))
        http_params.append(('Format', self.format))
        http_params.append(('Version', api_version))
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        http_params.append(('Timestamp', timestamp))
        http_params.append(('SignatureMethod', self.signature_method))
        http_params.append(('SignatureVersion', self.signature_version))
        http_params.append(('SignatureNonce', str(self.signature_once)))
        # 签名
        http_params = self.sign(req_type, http_params, access_secret)
        return urllib.urlencode(http_params)

    def get(self, http_params=[], host=None, execute=True):
        data = self.__gen_common_params('GET', self.api_version, self.access_key, self.access_secret, http_params)
        api_url = self.api_url

        if data == None:
            url = "%s" % (api_url)
        else:
            url = "%s/?" % api_url + data
        #print ("URL: %s"%url)
        if execute is False:
            return url
        ret = {}
        try:
            if host is not None:
                response = requests.get(url,headers={'Host':host}, verify=False)
            else:
                response = requests.get(url, verify=False)
            ret['code'] = response.status_code
            ret['data'] = response.text
        except Exception as e:
            ret['data'] = str(e)

        return ret

    def __get_data(self, http_params):
        params = self.__gen_common_params('POST', self.api_version, self.access_key, self.access_secret, http_params)
        if params == []:
            data = None
        else:
            data = params.replace("+", "%20")
            data = data.replace("*", "%2A")
            data = data.replace("%7E", "~")
        return data

    def post(self, http_params=[], out_fd=sys.stdout):
        data = self.__get_data(self.api_version, self.access_key, self.access_secret, http_params)
        api_url = self.api_url
        out_fd.write(u"[%s] --> (POST):%s\n%s\n" % (datetime.datetime.now(), api_url, data))
        ret = requests.post(api_url, data, verify=False)
        #print (ret.text)
        return ret

    def sign(self, http_method, http_params, secret):
        list_params = sorted(http_params, key=lambda d: d[0])
        #print list_params
        url_encode_str = urllib.urlencode(list_params)
        #print url_encode_str
        url_encode_str = url_encode_str.replace("+", "%20")
        url_encode_str = url_encode_str.replace("*", "%2A")
        url_encode_str = url_encode_str.replace("%7E", "~")
        string_to_sign = http_method + "&%2F&" + urllib.quote(url_encode_str)
        #print string_to_sign
        hmac_key = str(secret + "&")
        sign_value = str(hmac.new(hmac_key, string_to_sign, hashlib.sha1).digest().encode('base64').rstrip())
        http_params.append(('Signature', sign_value))
        return http_params
class AliWaf(AliOpenAPI):
    def __init__(self, api_url, ak, sk, api_version,instance_id, region,):

        super(AliWaf, self).__init__(api_url=api_url, ak=ak, sk=sk, api_version=api_version)
        self.instance_id = instance_id
        self.region = region

    def DescribeDomainNames(self,instance_id=None, region='cn',execute=True):
        if instance_id is None:
            instance_id = self.instance_id
        if region is None:
            region = self.region
        params = [
            ('Action', 'DescribeDomainNames'),
            ('InstanceId', instance_id),
            ('Region',region),
        ]
        return self.get(http_params=params,execute=execute)

    def DescribeDomainConfig(self,domain,instance_id=None, region='cn',execute=True):
        if instance_id is None:
            instance_id = self.instance_id
        if region is None:
            region = self.region
        params = [
            ('Action', 'DescribeDomainConfig'),
            ('InstanceId', instance_id),
            ('Region',region),
            ('Domain',domain)
        ]
        return self.get(http_params=params,execute=execute)
