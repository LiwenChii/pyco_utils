
from functools import wraps


def format_func(cls, name, *args, **kwargs):
    t1 = ', '.join(str(x) for x in args)
    t2 = ''
    if kwargs:
        t2 = ', ' + ', '.join('{}={}'.format(k, v) for k, v in kwargs.items())
    text = '{}.{}({}{})'.format(cls, name, t1, t2)
    return text


class Alog(object):
    def __getattribute__(self, name):
        def wrap(*args, **kwargs):
            # 这样如果 Alog 不存在属性时，不会直接报错，
            # Alog.attr_func.__name__ = 'wrap'
            m = super(Alog, self).__getattribute__(name)(*args, **kwargs)
            if name.startswith('api'):
                d = '{} ==> {}'.format(format_func(self.__class__, name, *args, **kwargs), m)
                print(d)
            return m

        return wrap


class Flog(object):
    def __getattribute__(self, name):
        # 注意 Flog 和 Alog 不一样，
        # 这样如果 Flog 不存在 属性时，会正常报错
        func = super(Flog, self).__getattribute__(name)
        if isinstance(func, (int, str, float, dict, list, tuple)):
            return func
        else:
            @wraps(func)
            def wrap(*args, **kwargs):
                m = func(*args, **kwargs)
                if not name.startswith('_'):
                    d = '{} ==> {}'.format(format_func(self.__class__.__name__, name, *args, **kwargs), m)
                    print(d)
                return m

            return wrap


class Mlog(Flog):
    def __getattr__(self, name):
        # 这样会死循环
        # func = getattr(self, name)
        # 当并不存在属性值时候，才会 getattr
        def wrap(*args, **kwargs):
            print('!!!', format_func(self.__class__.__name__, name, *args, **kwargs))

        return wrap
