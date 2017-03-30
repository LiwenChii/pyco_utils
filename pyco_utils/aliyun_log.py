#!/usr/bin/env python
# encoding:utf-8
__author__ = 'nico'

from time import time
from aliyun.log.logclient import LogClient
from aliyun.log.listlogstoresrequest import ListLogstoresRequest
from aliyun.log.gethistogramsrequest import GetHistogramsRequest

Ali_Project = 'project'  # 上面步骤创建的项目名称
Ali_Query_Store = 'store'  # 上面步骤创建的日志库名称
Ali_Query_Topic = 'search'
Ali_Query_Paras = 'detect'
Ali_Endpoint = 'cn-beijing.sls.aliyuncs.com'  # 选择与上面步骤创建Project所属区域匹配的Endpoint
Ali_AccessKeyId = 'access_id'  # 使用你的阿里云访问秘钥AccessKeyId
Ali_AccessKey = 'access_key'  # 使用你的阿里云访问秘钥AccessKeySecret


class Alilog():
    endpoint = ''  # 选择与上面步骤创建Project所属区域匹配的Endpoint
    accessKeyId = ''  # 使用你的阿里云访问秘钥AccessKeyId
    accessKey = ''  # 使用你的阿里云访问秘钥AccessKeySecret
    client = None

    def __init__(self, endpoint=Ali_Endpoint, access_key=Ali_AccessKey, access_key_id=Ali_AccessKeyId):
        self.endpoint = endpoint
        self.accessKey = access_key
        self.accessKeyId = access_key_id
        self.client = LogClient(endpoint, access_key_id, access_key)

    def list_logstore(self, project=Ali_Project):
        request = ListLogstoresRequest(project)
        logstores = self.client.list_logstores(request)
        logstores.log_print()
        return logstores

    def list_shard(self, project=Ali_Project, logstore=Ali_Query_Store):
        shards = self.client.list_shards(project, logstore)
        shards = shards.get_shards_info()
        return shards

    def get_cursor(self, timestamp, shard_id=0, project=Ali_Project, logstore=Ali_Query_Store):
        res = self.client.get_cursor(project, logstore, shard_id, timestamp)
        res.log_print()
        cursor = res.get_cursor()
        return cursor

    def loggroups_by_shard(self, start_time, count=10, end_cursor=None, shard_id=0, project=Ali_Project,
                           logstore=Ali_Query_Store):
        start_cursor = self.get_cursor(start_time, shard_id, project, logstore)
        res = self.client.pull_logs(project, logstore, shard_id, start_cursor, count, end_cursor)
        # next_cursor = res.get_next_cursor()
        res._transfer_to_json()  # fixme turn the log_list into list , bug of ALiyun
        log_list = res.loggroup_list_json
        return log_list

    def read_log_by_topic(self, start_time, end_time=None, topic=Ali_Query_Topic, query=Ali_Query_Paras):
        if not end_time:
            end_time = int(time())
        request = GetHistogramsRequest(Ali_Project, Ali_Query_Store, start_time, end_time, topic, query)
        response = self.client.get_histograms(request)
        response.log_print()
        # details = response.histograms
        # count = response.get_total_count()
        # logs = response.logs() # fixme


if __name__ == '__main__':
    start_time = int(time()) - 3600 * 24 * 3
    alog = Alilog()
    alog.list_logstore()
    alog.list_shard()
    alog.get_cursor(start_time)
    alog.loggroups_by_shard(start_time)
    alog.read_log_by_topic(start_time)
