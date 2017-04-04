import os
import sys
import string
import random
import re
from hashlib import md5

from datetime import datetime, timedelta
import time



def clock_ts(time_point=0, secs=0, mins=0, hours=0, days=0):
    '''
    :param time_point, secs,  mins,  hours,  days: int (1,0,-1)
    '''
    if time_point == 0:
        time_point = int(time.time())
    interval = secs + mins * 60 + hours * 3600 + days * 3600 * 24
    time_point = time_point + interval
    return time_point


# def format_date(date, style='%Y-%m-%d %H:%M', zone=0):
#     if isinstance(date, int):
#         date = datetime.fromtimestamp(date)
#     if isinstance(date, str):
#         from dateutil.parser import parse
#         date = parse(date)
#     if isinstance(date, datetime):
#         date = date + timedelta(hours=zone)
#         dt = date.strftime(style)
#         return dt
#     else:
#         return '0000-00-00 00:00'

def pardir(path, depth=1):
    path = os.path.abspath(path)
    for i in range(depth):
        path = os.path.dirname(path)
    return path


def source_root(path):
    sys.path.insert(0, path)


def short_uuid(length):
    charset = string.ascii_letters + string.digits
    return ''.join([random.choice(charset) for i in range(length)])


def camel_to_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def md5sum(content):
    m = md5()
    if not isinstance(content, bytes):
        content = content.encode('utf-8').strip()
    m.update(content)
    s = m.hexdigest().lower()
    return s


def str2list(text, line_sep='\n', strip_chars=None, filter_func=None):
    paras = [x.strip(strip_chars) for x in text.split(line_sep)]
    data = list(filter(filter_func, paras))
    return data


def list2dict(lines, sep=':', strip_chars=None):
    result = {}
    for i, line in enumerate(lines):
        paras = line.split(sep)
        k = paras[0].strip(strip_chars)
        v = ':'.join(paras[1:]).strip(strip_chars)
        result[k] = v
    return result


def str2dict(text, line_sep='\n', dict_sep=':'):
    ls = str2list(text, line_sep)
    ds = list2dict(ls, dict_sep)
    return ds


def fetch_dict(form, keys, default=None):
    ds = {}
    for k in keys:
        v = form.get(k, default)
        ds[k] = v
    return ds


def mirror_dict(form):
    '''dict(
        a=dict(x=0,y=1),     ==>   x=dict(a=0, b=0),
        b=dict(x=0,y=1),     ==>   y=dict(a=1, b=1),
    )
    '''
    result = {}
    if bool(form) and isinstance(form, dict):
        from_keys = form.keys()
        items = form.values()
        to_keys = items[0].keys()
        result = {tk: dict(map(lambda fk, item: (fk, item.get(tk)), from_keys, items)) for tk in to_keys}
        return result
    return result


# eg : mysql.proxy rows

def sort_rows(rows, key):
    # python2 cmp
    # func = lambda a, b: cmp(a.get(key), b.get(key))
    # ds = sort(rows, cmp=func)
    # python3, cmp is deprecated
    func = lambda x: x.get(key)
    ds = sorted(rows, key=func)
    return ds


def include(form, query):
    for k, v in query.items():
        dv = form.get(k)
        if dv != v:
            return False
    return True


def filter_rows(rows, query):
    from functools import partial
    func = partial(include, query=query)
    ds = list(filter(func, rows))
    return ds


def proxy_wget(url, file='temp.html'):
    # command = 'proxychains4 wget www.google.com'
    command = 'proxychains4 wget -O "{file}" "{url}"'.format(file=file, url=url)
    os.system(command)
    with open(file, 'r+') as f:
        return f.read()
