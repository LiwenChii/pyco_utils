from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy


class Event():
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    level = db.Column(db.Enum('A', 'B', 'C', 'D'), default='C')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def to_dict(self):
        data = vars(self).copy()
        for k, v in data.items():
            if k.startswith('_'):
                data.pop(k)
        return data


###########
# stream
###########

import redis
from flask import (
    Flask,
    Response,
    abort,
    jsonify,
)

app = Flask(__name__)
app.secret_key = 'key'

redis_client = redis.Redis()


# default: host='localhost', port=6379, db=0

def stream(channel):
    # 对每一个用户 创建一个[发布订阅]对象
    pubsub = redis_client.pubsub()
    # 订阅广播频道
    pubsub.subscribe(channel)
    for msg in pubsub.listen():
        if msg['type'] == 'message':
            data = msg['data'].decode('utf-8')
            # 用 sse 返回给前端
            yield jsonify(dict(data=data))


@app.route('/<channel>/subscribe', methods=['GET', 'POST'])
def channel_subscribe(channel):
    return Response(stream(channel), mimetype="text/event-stream")
    # 对应前端
    # var subscribe = function (channel) {
    #     var url = "/" + channel + '/subscribe';
    #     var sse = new EventSource(url);
    #     sse.onmessage = function (e) {
    #         var msg = JSON.parse(e.data);
    #         RespMsg(msg);
    #     };
    # };

