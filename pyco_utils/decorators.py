# coding: utf-8

import threading
from functools import wraps

from .logger import log


def retry(func, count=3):
    def decorator(*args, **kwargs):
        for i in range(count - 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log('[retry Error]', func.__name__, *args, **kwargs)
                log(e)
        return func(*args, **kwargs)

    return decorator


def ajax_func(func, daemon=True):
    @wraps(func)
    def wrapper(*args, **kwargs):
        th = threading.Thread(target=func, args=args, kwargs=kwargs)
        th.daemon = daemon
        log(func.__name__, args, kwargs, daemon)
        th.start()

    return wrapper


def singleton(cls):
    # 使用这个装饰器的类，不能作为父类被继承
    instance = {}

    def get_instance(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return get_instance
