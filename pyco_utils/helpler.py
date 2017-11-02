import os
import sys
import string
import random
import re
from hashlib import md5

import time


def md5sum(content):
    m = md5()
    if not isinstance(content, bytes):
        content = content.encode('utf-8').strip()
    m.update(content)
    s = m.hexdigest().lower()
    return s


def ensure_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def pardir(path, depth=1):
    path = os.path.abspath(path)
    for i in range(depth):
        path = os.path.dirname(path)
    return path


def source_root(path):
    # mark path as source root
    sys.path.insert(0, path)


def short_uuid(length):
    charset = string.ascii_letters + string.digits
    return ''.join([random.choice(charset) for i in range(length)])


def camel_to_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def gap_time(time_point=0, secs=0, mins=0, hours=0, days=0):
    if time_point == 0:
        time_point = int(time.time())
    interval = secs + mins * 60 + hours * 3600 + days * 3600 * 24
    time_point = time_point + interval
    return time_point


def format_date(date, style='%Y-%m-%d %H:%M', zone=0):
    from datetime import datetime, timedelta
    if isinstance(date, int):
        date = datetime.fromtimestamp(date)
    if isinstance(date, str):
        from dateutil.parser import parse
        date = parse(date)
    if isinstance(date, datetime):
        date = date + timedelta(hours=zone)
        dt = date.strftime(style)
        return dt
    else:
        return '0000-00-00 00:00'
