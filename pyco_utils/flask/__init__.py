import redis
from flask import (
    Flask,
    Response,
    abort,
    jsonify,
    request,
)

app = Flask(__name__)
app.secret_key = 'key'


def json_response(success, data=None, message=''):
    r = dict(
        success=success,
        data=data,
        message=message,
    )
    return jsonify(r)


@app.route('/map')
def url_map():
    def format_map(url_map):
        rules = url_map._rules
        total = len(rules)
        urls = []
        for rule in rules:
            u = dict(rule=rule.rule,
                     endpoint=rule.endpoint,
                     args=list(rule.arguments),
                     methods=list(rule.methods))
            urls.append(u)
        data = dict(total=total, urls=urls)
        return data

    url_map = app.url_map
    url_map = format_map(url_map)
    data = dict(url_map=url_map)
    data = jsonify(data)
    return data, 200
