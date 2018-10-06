import threading
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
users = set()
msg_source = None

class IndexPageHandler(tornado.web.RequestHandler):
  def get(self):
    self.render('index.html')

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        # print('oring')
        return True

    def open(self):
        users.add(self)
        print('当前监视用户数：{}'.format(len(users)))
        pass

    def on_message(self, message):
        global msg_source
        if msg_source is not None:
            for user in users:
                user.write_message(message)
        else:
            msg_source = self
            print('删除非监视用户：{}'.format(msg_source))
            users.remove(self)
            print('当前监视用户数：{}'.format(len(users)))

    def on_close(self):
        users.remove(self)
        print('监视用户离开,当前监视用户数：{}'.format(len(users)))
        pass

class Application(tornado.web.Application):

  def __init__(self, ip):
    handlers = [
      (r'/', IndexPageHandler),
      (r'/ws', WebSocketHandler)
    ]
    settings = {"template_path": ".", "address":ip}
    tornado.web.Application.__init__(self, handlers, **settings)

import config
config.process_html()
if __name__ == '__main__':
    ip = config.ip
    port = config.port
    print('监视服务器启动于：{}:{}'.format(ip,port))
    print('请执行监视数据获取客户端')
    ws_app = Application(ip)
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


'''

python ws_app.py

'''


