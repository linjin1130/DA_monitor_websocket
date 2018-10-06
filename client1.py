#!/usr/bin/env python
import asyncio
import json

import websockets

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
async def chat():
    global pre_color
    async with websockets.connect(
            'ws://'+ip+':'+str(port)+'/ws') as websocket:
        print('监视数据获取客户端打开')
        while(True):
            # 通过网络监视接口，获取原始监视数据
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
            await websocket.send(result)

            # msg = await websocket.recv()
            # print("From Server: {}".format(msg))
            # time.sleep(1)

asyncio.get_event_loop().run_until_complete(chat())
udp_rc.udp_uncon()