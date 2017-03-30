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

def upload(filename, path='.'):
    file = '{}/{}'.format(path, filename)
    with open(file, 'rb') as fs:
        aliyun_bucket.put_object(filename, fs, progress_callback=percentage)


def download(key, filename='', save=True):
    # filename = sys.argv[1]
    if not filename:
        filename = key

    if aliyun_bucket.object_exists(key):
        reps1 = aliyun_bucket.get_object_to_file(key, filename, progress_callback=percentage)
        print(' [oss]:get_object({}) : [{}]'.format(key, reps1.status))
        if not save:
            reps2 = aliyun_bucket.delete_object(key)
            print(' [oss]delete_object({}) : [{}]'.format(key, reps2.status))
    else:
        warn = '[warn]: "{key}" dose not exist.'.format(key=key)
        print(warn)



def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}/{1}    {2}% '.format(consumed_bytes, total_bytes, rate))
        sys.stdout.flush()


def list_keys(prefix='', delimiter='', marker='', max_keys=100):
    reps = aliyun_bucket.list_objects(prefix, delimiter, marker, max_keys)
    if reps.status == 200:
        object_list = reps.object_list
        keys = [obj.key for obj in object_list]
        return keys


def delete_key(key):
    aliyun_bucket.delete_object(key=key)


def delete_keys(keys):
    for key in keys:
        reps = delete_key(key=key)
        print(reps.status)

