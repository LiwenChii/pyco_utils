from json import JSONEncoder
from datetime import (
    datetime,
    timedelta,
)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            t = obj.strftime('%Y/%m/%d %H:%M:%S')
            return t
        elif isinstance(obj, timedelta):
            t = str(obj)
            return t
        else:
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
