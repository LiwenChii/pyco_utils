# -*- coding:utf-8 -*-
import oss2

ACCESS_KEY_ID = ''
ACCESS_KEY_SECRET = ''
ENDPOINT = ''
BUCKET_NAME = ''

aliyun_auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
aliyun_bucket = oss2.Bucket(aliyun_auth, ENDPOINT, BUCKET_NAME)
aliyun_blob_root = 'http://{}.{}/'.format(BUCKET_NAME, ENDPOINT)


def upload_file_data(filename, data, blob_name):
    blob_key = blob_name + filename
    blob_url = aliyun_blob_root + blob_key
    blob = aliyun_bucket.put_object(key=blob_key, data=data)
    return blob_url


def blob_urls(prefix='', max_keys=100):
    result = aliyun_bucket.list_objects(prefix=prefix, max_keys=max_keys)
    objects = result.object_list
    urls = [aliyun_blob_root + obj.key for obj in objects]
    return urls
