import redis

from . import (
    jsonify,
    Response,
    app,
)

# default: host='localhost', port=6379, db=0
redis_client = redis.Redis()


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
    # 对应前端
    # var subscribe = function (channel) {
    #     var url = "/" + channel + '/subscribe';
    #     var sse = new EventSource(url);
    #     sse.onmessage = function (e) {
    #         var msg = JSON.parse(e.data);
    #         RespMsg(msg);
    #     };
    # };
    return Response(stream(channel), mimetype="text/event-stream")
