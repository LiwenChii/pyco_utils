import os
import sys
import string
import random


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
