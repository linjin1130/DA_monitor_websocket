#!/usr/bin/env python
import asyncio
import json

import time
import websockets

from DAboarddata import DAbroaddata
from da_status import DAStatusParser

udp_rc = DAbroaddata()
udp_rc.connectDAboard()

da_parse = DAStatusParser('info.json')
da_dict = {}
da_datas = []
pre_color = []
ttl = 5
import config
ip = config.ip
port = config.port
use_false_data = config.use_false_data
last_time = time.time()
async def chat():
    global pre_color
    global last_time
    async with websockets.connect(
            'ws://'+ip+':'+str(port)+'/ws') as websocket:
        print('监视数据获取客户端打开')
        while(True):
            # 通过网络监视接口，获取原始监视数据
            message, addr = udp_rc.dabroad_datareq(false_data=use_false_data)
            msg, color, host = da_parse.bytes_to_str(message)
            da_dict[msg[3]['value']] = [color,ttl, host]
            # da_set.add(msg[3]['value'])
            # da_list = list(da_set)
            # da_dict.sort()
            if (time.time() - last_time) > 1:
                rm_key = []
                for key in da_dict:
                    # print(da_dict[key])
                    val = da_dict[key]
                    val[1] -= 1
                    da_dict[key] = val
                    if val[1] < 1:
                        rm_key.append(key)
                        print(f'数据源{key}不再更新')
                for key in rm_key:
                    da_dict.pop(key)
                last_time = time.time()
                # print(time.time() - last_time)

            #生成上位机ip为key的列表
            host_dic = {}
            for key in da_dict:
                host_dic[da_dict[key][2]]=[]
            for key in da_dict:## 生成主机为键值，【板号，颜色对】的列表
                host_dic[da_dict[key][2]].append([key,da_dict[key][0]])
            for key in host_dic:
                host_dic[key].sort()
            # print(host_dic)
            # da_lists = sorted(da_dict.items())#[[key, value] for key, value in da_dict]
            host_list = []
            da_list = []
            color_list = []
            for key in host_dic:
                host_list += [key]
                if len(host_dic[key]) > 1:
                    for i in range(len(host_dic[key])-1):
                        host_list.append("")
                for item in host_dic[key]:
                    da_list.append(item[0])# = [item[0] for item in da_lists]
                    color_list.append(item[1])# = [item[1] for item in da_lists]
            # print(host_list)
            # print(color_list)
            # print(da_list)
            if(len(pre_color) == 0):
                pre_color = color_list
            head = [{'hardware_num': [len(da_list), len(host_dic.keys())]}, {'hardware_list': [da_list,color_list,pre_color, host_list]}]
            pre_color = color_list
            msg = head + msg
            result = json.dumps(msg)  # .encode()
            await websocket.send(result)

            # msg = await websocket.recv()
            # print("From Server: {}".format(msg))
            # time.sleep(1)

asyncio.get_event_loop().run_until_complete(chat())
udp_rc.udp_uncon()