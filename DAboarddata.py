import struct
import time
from socket import *
import os
import csv
false_raw_data = []
with open(os.path.join(os.getcwd(),'false_monitor_data.dat'), 'r') as fd_file:
    reader = csv.reader(fd_file)
    for line in reader:
        false_raw_data.append(line)

class DAbroaddata(object):
    dabroad_host=''
    dabroad_port=6789
    bufsize = 1024
    pos = 0

    def __init__(self):
        self.bufsize = self.bufsize

    #与DA板建立连接
    def connectDAboard(self):
        addr = (self.dabroad_host, self.dabroad_port)
        self.udpServer = socket(AF_INET, SOCK_DGRAM)  # 创建一个服务器端UDP套接字
        self.udpServer.bind(addr)  # 开始监听

    #得到DA板返回的数据
    def dabroad_datareq(self, false_data = True, prepare_data = False):
    # def dabroad_datareq(self, false_data = False, prepare_data = True):
        # 当false_data = True时 返回假数据（以前采集和存储的）
        data = None
        addr = None
        # print(false_data)
        if not false_data:
            data, addr = self.udpServer.recvfrom(self.bufsize)  # 接收数据和返回地址
            # print(data, addr)
            if prepare_data:
                with open(os.path.join(os.getcwd(),'false_monitor_data.dat'), 'a', newline='') as fd_file:
                    writer = csv.writer(fd_file)
                    writer.writerow([list(data), addr], )
        else:
            # print(false_raw_data[self.pos%len(false_raw_data)])
            data1, addr1 = false_raw_data[self.pos%len(false_raw_data)]
            d1 = data1[1:-1].strip().split(',')
            d2 = [int(i) for i in d1]
            data = struct.pack('{}B'.format(len(d2)), *d2)
            addr = addr1[1:-1].split(',')
            self.pos += 1
            time.sleep(0.1)
        return  data,addr

    def udp_uncon(self):
        self.udpServer.close()
        return