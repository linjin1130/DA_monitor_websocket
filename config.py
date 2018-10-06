import os
import socket
#方法1
#获取本机电脑名
def get_host_ip1():
    myname = socket.getfqdn(socket.gethostname(  ))
    #获取本机ip
    myaddr = socket.gethostbyname(myname)
    return myaddr

# 可以封装成函数，方便 Python 的程序调用
#方法二
def get_host_ip2():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


#方法3
def get_host_ip3():
    addrs = socket.getaddrinfo(socket.gethostname(),None)
    for item in addrs:
        if (len(item[-1]) < 3):
            net_seg = int(item[-1][0].split('.')[0])
            if net_seg != 10:
                return item[-1][0]

ip = get_host_ip3()
port = 8003
use_false_data = True
def process_html():
    lines = []
    with open(os.path.join(os.getcwd(),'index.html'), 'r', encoding='utf-8') as file_hd:
        for line in file_hd.readlines():
            if line.find("new WebSocket('ws:") > 0:
                line = line[:line.index('WebSocket')] + "WebSocket('ws://" + ip +":" + str(port)+"/ws');\n"
            lines.append(line)
    with open(os.path.join(os.getcwd(), 'index.html'), 'w', encoding='utf-8') as file_hd:
        file_hd.writelines(lines)


