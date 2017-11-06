# -*- coding: utf-8 -*-

import codecs
from jinja2 import (
    Template,
    Environment,
    PackageLoader,
)

tpl_loader = PackageLoader('utils')
tpl_env = Environment(loader=tpl_loader)


def render_content(content, **kwargs):
    charset = kwargs.pop('charset', 'utf-8')
    content = codecs.encode(content, encoding=charset).decode(charset)
    template = Template(content)
    return template.render(**kwargs)


def render_template(filename, **kwargs):
    template = tpl_env.get_template(filename)
    content = template.render(**kwargs)
    return content


def transform(form):
    data = {}
    for k, v in form.items():
        if isinstance(v, list) and len(v) == 1:
            v = v[0]
        if isinstance(v, bytes):
            v = v.decode()
        if isinstance(v, str):
            v = v.strip()
        data[k] = v
    return data
