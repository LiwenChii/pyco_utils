# -*- coding: utf-8 -*-
import os
import time
import string
import hashlib
import random

from datetime import datetime


def md5(content, length=32):
    md = hashlib.md5()
    if not isinstance(content, bytes):
        content = content.encode('utf-8')
    md.update(content)
    s = md.hexdigest()[:length]
    return s


def short_uuid(length=12):
    charset = string.ascii_letters + string.digits
    return ''.join([random.choice(charset) for i in range(length)])


def utctime():
    t = int(time.time())
    return t


def date_string(fmt='%Y%m%d%H%M%S'):
    d = datetime.utcnow()
    md = d.strftime(fmt)
    return md


def auto_form(form, nullable=False, autoInt=True, autoBool=True, autoDrop=True):
    '''
    :param form: request_form
    :param nullable: 是否抛弃键值空
    :param autoInt:  是否检测字符串，并自动转换数值型
    :param autoBool: 是否检测字符串，并自动转换布尔型
    :param autoDrop: 是否抛弃空字符串键值，
    :return:
    '''
    data = {}
    for k, v in form.items():
        if not nullable and v is None:
            print('drop<{}:{}>'.format(k, v))
        elif isinstance(v, str):
            v = v.strip()
            s = v.lower()
            if autoDrop and not (bool(v)):
                print('drop<{}:{}>'.format(k, v))
            elif autoInt and v.isdigit():
                data[k] = int(v)
            elif autoBool and s == 'false':
                data[k] = False
            elif autoBool and s == 'true':
                data[k] = True
            else:
                data[k] = v
        else:
            data[k] = v
    return data


def ensure_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def upload_file(file, allow_ext='png;jpg;jpeg;gif', url_prefix='/uploads/images/', path=''):
    filename = file.filename
    paras = filename.split('.')
    ext = paras[-1].lower()
    allow_exts = allow_ext.lower().strip(';').split(';')
    if ext in allow_exts:
        filename = '.'.join(paras).replace('/', '-').replace('\\', '-')
        filename = '_'.join([date_string(), filename])
        url = '{}{}'.format(url_prefix, filename)
        f = os.path.join(path, filename)
        file.save(f)
        file.seek(0)
        return url


def compress_avatar(file, from_path='', to_path=''):
    image = '{}/{}'.format(from_path, file)
    avatar = '{}/{}'.format(to_path, file)
    cmd = 'magick {} -resize 64x64 {}'.format(image, avatar)
    status = os.system(cmd)
    code = os.WEXITSTATUS(status)
    if code == 0:
        return True, avatar
    else:
        return False, image
