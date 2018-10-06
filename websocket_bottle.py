from bottle import request, Bottle, abort, template
from geventwebsocket import WebSocketError
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

import threading
import json
from da_status import *
from python3.web.DAboarddata import DAbroaddata
import config
config.process_html()
ip = config.ip
port = config.port
use_false_data = config.use_false_data
udp_rc = DAbroaddata()
udp_rc.connectDAboard()

da_parse = DAStatusParser('info.json')
da_set = set()

app = Bottle()
users = set()


@app.get('/')
def index():
    return template('index')

@app.get('/ws')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    users.add(wsock)

    if not wsock:
        abort(400, 'Expected WebSocket request.')
    count = 0
    print(u"现有连接用户：%s" % (len(users)))
    while True:
        message, addr = udp_rc.dabroad_datareq(false_data=use_false_data)
        if len(users) < 1:
            break
        count += 1
        if count > 10:
            wsock = request.environ.get('wsgi.websocket')
            if wsock:
                users.add(wsock)
            count = 0
        msg = da_parse.bytes_to_str(message)
        da_set.add(msg[3]['value'])
        da_list = list(da_set)
        da_list.sort()
        # print(da_list)
        head = [{'hardware_num':len(da_list)}, {'hardware_list':da_list}]
        msg = head+msg
        # print(msg)
        if message:
            result = json.dumps(msg)#.encode()
            # print(result)
            for user in users:
                try:
                    user.send(result)
                except WebSocketError:
                    print(u'某用户已断开连接')
                    users.remove(wsock)
                    break

    # 如果有客户端断开，则删除这个断开的websocket
    print('离开')
    # users.remove(wsock)


# server = WSGIServer(("127.0.0.1", 8002), app,handler_class=WebSocketHandler)
server = WSGIServer((ip, port), app,handler_class=WebSocketHandler)
server.serve_forever()
udp_rc.udp_uncon()
