from __future__ import absolute_import
import os
import logging
from functools import wraps
from pprint import pformat

from requests import Response

LOG_LEVEL = logging.INFO
LEVEL_ERROR = 'error'
LOGGER_NAME = '{project_name}'
LOGGER_FILE = '{project_name}.log'
LOGGER_FORMATTER = '[%(asctime)s]%(message)s'


def ensure_dir(file):
    fdir = os.path.dirname(file)
    if not os.path.exists(fdir):
        os.makedirs(fdir)


def LocalLogger(**kwargs):
    level = kwargs.get('level', LOG_LEVEL)
    logger_name = kwargs.get('name', LOGGER_NAME)
    logger_file = kwargs.get('filename', LOGGER_FILE)
    mode = kwargs.get('filemode', 'a+')
    fs = kwargs.get('format', LOGGER_FORMATTER)
    fmt = logging.Formatter(fs)
    ensure_dir(logger_file)
    hdlr = logging.FileHandler(filename=logger_file, mode=mode)
    hdlr.setFormatter(fmt)
    logger = logging.Logger(logger_name)
    logger.addHandler(hdlr=hdlr)
    logger.setLevel(level=level)
    return logger


local_logger = LocalLogger()


def log(*args, **kwargs):
    logger = local_logger
    level = kwargs.pop('level', None)
    stdout = kwargs.pop('stdout', False)
    result = kwargs.pop('result', None)
    content = "{} {}".format(pformat(args), pformat(kwargs))
    if result is not None:
        content += '\n[result] : {}'.format(result)
    if level == LEVEL_ERROR:
        logger.error(content)
    else:
        logger.info(content)
        logger.log(level)
    if stdout:
        print(content)


def log_response(resp, tag='', status_filter=None):
    if isinstance(resp, Response):
        if status_filter is None:
            status_filter = [200]
        status_code = resp.status_code
        if status_code not in status_filter:
            content = resp.content
            url = resp.url
            tag = '[API - {}] - {}'.format(tag, status_code)
            request = resp.request
            request_body = request.body if request else None
            request_headers = dict(request.headers) if request else None
            log(tag, url,
                level='error',
                status_code=status_code,
                response_content=content,
                request_body=request_body,
                request_headers=request_headers
                )


def log_response_after_func(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        resp = func(*args, **kwargs)
        tag = func.func_name
        log_response(resp, tag=tag)
        return resp

    return wrapper


def log_func(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        log(func.__name__, *args, result=result, **kwargs)
        return result

    return wrapper
