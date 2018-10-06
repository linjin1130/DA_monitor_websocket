#!/usr/bin/env python
import asyncio
import json
from da_status import *

from DAboarddata import DAbroaddata
from da_status import DAStatusParser

udp_rc = DAbroaddata()
udp_rc.connectDAboard()

da_parse = DAStatusParser('info.json')
da_dict = {}
da_datas = []
pre_color = []
import config
ip = config.ip
port = config.port
use_false_data = config.use_false_data
from ws4py.client.threadedclient import WebSocketClient

class DummyClient(WebSocketClient):
	
    def opened(self):
		global pre_color
        print('监视数据获取客户端打开')
        while(True):
            message, addr = udp_rc.dabroad_datareq(false_data=use_false_data)
            msg, color = da_parse.bytes_to_str(message)
            da_dict[msg[3]['value']] = color
            # da_set.add(msg[3]['value'])
            # da_list = list(da_set)
            # da_dict.sort()
            da_lists = sorted(da_dict.items())#[[key, value] for key, value in da_dict]
            da_list = [item[0] for item in da_lists]
            color_list = [item[1] for item in da_lists]

            if(len(pre_color) == 0):
                pre_color = color_list
            head = [{'hardware_num': len(da_list)}, {'hardware_list': [da_list,color_list,pre_color]}]
            pre_color = color_list
            msg = head + msg
            result = json.dumps(msg)  # .encode()
            self.send(result)
        # self.send("www.baidu.com")

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, m):
        print(m)


if __name__ == '__main__':
    ws = DummyClient('ws://' + ip + ':' + str(port) + '/ws', protocols=['chat'])
    try:
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()