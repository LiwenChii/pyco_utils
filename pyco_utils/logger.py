from __future__ import absolute_import

import logging
from functools import wraps
from pprint import pformat


fmt_str = '[%(asctime)s]%(message)s'
fmt = logging.Formatter(fmt_str)


def file_hdl(fmt=fmt, level=logging.ERROR, logfile='.log'):
    hdlr = logging.FileHandler(filename=logfile, mode='a+')
    hdlr.setFormatter(fmt)
    hdlr.setLevel(level)
    return hdlr


def stream_hdl(fmt=fmt, level=logging.ERROR):
    hdlr = logging.StreamHandler()
    hdlr.setFormatter(fmt)
    hdlr.setLevel(level)
    return hdlr


def logger(name='COLOG', **kwargs):
    lg = logging.Logger(name)
    hd1 = file_hdl(**kwargs)
    hd2 = stream_hdl(*kwargs)
    lg.addHandler(hdlr=hd1)
    lg.addHandler(hdlr=hd2)
    return lg


local_logger = logger()


def log(*args, **kwargs):
    lg = local_logger
    level = kwargs.pop('level', logging.INFO)
    result = kwargs.pop('result', None)
    msg = "{} {}".format(pformat(args), pformat(kwargs))
    if result is not None:
        msg += '\n[result] : {}'.format(result)
    lg.log(level, msg)


def log_func(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        log(func.__name__, args, kwargs, result=result)
        return result

    return wrapper


def log_response_after_func(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        resp = func(*args, **kwargs)
        tag = func.__name__
        log_response(resp, tag=tag)
        return resp

    return wrapper


def log_response(resp, tag=''):
    # from requests import Response
    # isinstance(resp, Response):
    status_code = resp.status_code
    if status_code != 200:
        level = logging.ERROR
    else:
        level = logging.INFO
    url = resp.url
    result = format_response(resp)
    log(status_code, url, tag=tag, level=level, result=result)


def format_response(response):
    url = response.url
    status_code = response.status_code
    content = response.content
    info = dict(
        url=url,
        status_code=status_code,
        content=content,
    )
    request = response.request
    if request:
        info['request_body'] = request.body
        info['request_method'] = request.method
        info['request_headers'] = request.headers
    msg = '[Response]' + '\n' + pformat(info, indent=4) + '\n'
    return msg
