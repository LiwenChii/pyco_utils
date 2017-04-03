class EchoCls(object):
    # todo
    def __getattr__(self, name):
        def wrap(*args):
            m = name if args is None else name + str(tuple(args))
            print(m)
            return self.name

        return wrap


from flask.json import JSONEncoder
from datetime import datetime
import calendar


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                if obj.utcoffset() is not None:
                    obj = obj - obj.utcoffset()
                return int(
                    calendar.timegm(obj.timetuple())
                )
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


class Utf8Encoder:
    @classmethod
    def encode_list(cls, data):
        rv = []
        for item in data:
            if isinstance(item, str):
                item = item.encode('utf-8')
            elif isinstance(item, list):
                item = cls.encode_list(item)
            elif isinstance(item, dict):
                item = cls.encode_dict(item)
            rv.append(item)
        return rv

    @classmethod
    def encode_dict(cls, data):
        rv = {}
        for key, value in data.iteritems():
            if isinstance(key, str):
                key = key.encode('utf-8')
            if isinstance(value, str):
                value = value.encode('utf-8')
            elif isinstance(value, list):
                value = cls.encode_list(value)
            elif isinstance(value, dict):
                value = cls.encode_dict(value)
            rv[key] = value
        return rv
