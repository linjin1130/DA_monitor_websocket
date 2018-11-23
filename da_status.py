# coding: utf-8
import datetime
import json
import calc

class DAStatusParser:
    def __init__(self, info_file):
        self.parser_info = self.load_parse_info(info_file)

    def load_parse_info(self, file_name):
        with open(file_name, encoding='utf-8') as json_file:
            parse_info = json.load(json_file)
            return parse_info

    def item_info(self, index):
        return self.parser_info[index]

    def byte_position(self, entry):
        get_byte_len = lambda l: (l >> 3) + ((l & 7) > 0)
        byte_offset = entry['startByte']
        bit_len = entry['bitLength']
        byte_len = get_byte_len(bit_len + entry['startBit'])
        return byte_offset, byte_len

    def masked_data(self, data, entry):
        bit_offset = entry['startBit']
        bit_len = entry['bitLength']
        mask = ((1 << bit_len) - 1) << bit_offset
        masked = (data & mask) >> bit_offset
        return masked

    def parse_data(self, data, entry, index):
        parse_type = entry['parseType']
        color = ''
        if parse_type == 'enum':
            option = entry['EnumValue'].get(str(data), {})
            value = option.get('name', 'undefined')
            color = option.get('color')
        elif parse_type == 'calc':
            calc_index = entry['dispIndex']
            func = getattr(calc, f'calc_{calc_index:02d}', lambda x: x)
            value = func(data)
        else:
            value = data
        w = len(hex(data)) - 2
        w = w + (w & 1)
        return {
            'name': entry['name'],
            'hex': f'0x{data:0{w}X}',
            'value': value,
            'color': color,
            'index': index,
            'parseType': parse_type
        }

    def bytes_to_str(self, data):
        parse_info = self.parser_info
        pos = self.byte_position 
        masked = self.masked_data
        parse = self.parse_data
        items = []
        color = "#000000"
        host = '0.0.0.0'
        t = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        items.append({
            'name': '采样时间',
            'hex': '0x000000',
            'value': t,
            'color': '',
            'index': 0,
            'parseType': 'calc'
        })

        for i, entry in enumerate(parse_info):
            byte_offset, byte_len = pos(entry)
            seg = data[byte_offset:byte_offset+byte_len]
            # print(seg)
            # print(data)
            seg_hex = int.from_bytes(seg, 'big')
            seg_data = masked(seg_hex, entry)
            item = parse(seg_data, entry, i+1)
            items.append(item)
            if item['color'] == '#FF0000':
                color = item['color']
            elif item['color'] == '#0000FF':
                if color != '#FF0000':
                    color = item['color']
            elif item['color'] == '#00FF00':
                if(color != '#FF0000' and color != '#0000FF' ):
                    color = item['color']
            if item['name'] == '当前上位机IP':
                host = item['value']


        if len(items) & 0x01 == 1:
            items.append({
                'name': '采样时间',
                'hex': t,
                'value': t,
                'color': '',
                'index': 0,
                'parseType': 'calc'
            })
        return items, color, host
