from  pyco_utils.helpler import (
    pardir,
    short_uuid,
    str2list,
    list2dict,
    str2dict,
    fetch_dict,
)


def test_pardir():
    p0 = pardir(__file__)
    # /pyco_utils/tests
    p1 = pardir('.')
    # /pyco_utils
    assert p0.startswith(p1)
    assert p0 == p1 + '/tests'
    print (p0)
    print (p1)


def test_short_uuid():
    m = short_uuid(4)
    assert len(m) == 4


def test_str2list():
    m = 'as\nyou\n \nSee'
    ds = str2list(m)
    ds2 = str2list(m, filter_func=bool)
    assert ds == ['as', 'you', 'See']
    assert ds == ds2


def test_list2dict():
    m = [
        'Host: localhost:3000  ',
        'Content-Type: text/html\n',
    ]
    d = list2dict(m)
    assert d['Host'] == 'localhost:3000'
    assert d['Content-Type'] == 'text/html'


def test_str2dict():
    s = 'Host: localhost:3000  \r\n' \
        'Content-Type: text/html\r\n'
    d = str2dict(s)
    assert d['Host'] == 'localhost:3000'
    assert d['Content-Type'] == 'text/html'


def test_fetch_dict():
    s = '''
        Host: fanyi.baidu.com
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
        Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
        Accept-Encoding: gzip, deflate
        Connection: keep-alive
        Pragma: no-cache
        Cache-Control: no-cache
        '''
    keys = ['Host', 'Connection']
    form = str2dict(s)
    ds = fetch_dict(form, keys)
    assert len(ds) == 2


