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


# eg : mysql.proxy rows

def sort_rows(rows, key):
    # python2 cmp
    # func = lambda a, b: cmp(a.get(key), b.get(key))
    # ds = sort(rows, cmp=func)
    # python3, cmp is deprecated
    func = lambda x: x.get(key)
    ds = sorted(rows, key=func)
    return ds


def ensure_field(form, query):
    for k, v in query.items():
        dv = form.get(k)
        if dv != v:
            return False
    return True


def filter_rows(rows, query):
    from functools import partial
    func = partial(ensure_field, query=query)
    ds = list(filter(func, rows))
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


def format_dict(form, nullable=False, autoInt=True, autoBool=True, autoDrop=True):
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
