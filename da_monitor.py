import time
from socket import *
# from config_util import *

class DAbroaddata(object):
    dabroad_host=''
    dabroad_port=6789
    bufsize = 1024


    def __init__(self):
        # self.confobj = Config()
        # self.dabroad_host = self.confobj.dabroad_host
        # self.dabroad_port = self.confobj.dabroad_port
        self.bufsize = self.bufsize

    #与DA板建立连接
    def connectDAboard(self):
        addr = (self.dabroad_host, self.dabroad_port)
        self.udpServer = socket(AF_INET, SOCK_DGRAM)  # 创建一个服务器端UDP套接字
        self.udpServer.bind(addr)  # 开始监听

    #得到DA板返回的数据
    def dabroad_datareq(self):
        data, addr = self.udpServer.recvfrom(self.bufsize)  # 接收数据和返回地址
        return  data,addr

    def udp_uncon(self):
        self.udpServer.close()
        return


udp_rc = DAbroaddata()
udp_rc.connectDAboard()
# for i in range(10000):
while(1):
    data, addr = udp_rc.dabroad_datareq()
    print(addr, data)
    # time.sleep(0.01)



#!/usr/bin/python
# encoding=utf-8

import time
import websocket

# 配置远程服务器的IP，帐号，密码，端口等，因我做了双机密钥信任，所以不需要密码
# websocket服务端地址
ws_server = "ws://127.0.0.1:8002/websocket/"
def tailfLog():
    """获取远程服务器实时日志，并发送到websocket服务端"""

    ws = websocket.WebSocket.create_connection(ws_server)   # 创建websocket连接
    while True:
        data, addr = udp_rc.dabroad_datareq()
        if addr[0]:
            ws.send(addr[0])   #把内容发送到websocket服务端
        print(time.time())

if __name__ == '__main__':
    tailfLog()