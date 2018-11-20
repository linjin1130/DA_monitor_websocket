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

f5_names = []
def append(name):
    global f5_names
    f5_names.append(name)

from datetime import date
import h5py  # 导入工具包
def hdf5_write(addr, data):
    global f5_names
    date_str = date.today().strftime("%y%m%d")
    file_name = date_str + '.h5'
    # print(addr)
    path = '/'.join([addr[0], date_str])
    day_second = int(time.time() - time.mktime(date.today().timetuple()))
    if not os.path.exists(file_name):
        print('创建文件')
        f = h5py.File(file_name, 'w')
        f.create_dataset(path, shape=(3600 * 24, 1024), dtype='i8', compression='gzip')
        f.close()
    with h5py.File(file_name, "a") as f:
        f5_names = []
        f.visit(append)
        if path not in f5_names:
            f.create_dataset(path, shape=(3600 * 24, 1024), dtype='i8', compression='gzip')
        f[path][day_second,:] = data

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
            f_data = struct.unpack('{}B'.format(len(data)), data)
            hdf5_write(addr, f_data)
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
            time.sleep(0.5)


        return  data,addr

    def udp_uncon(self):
        self.udpServer.close()
        return