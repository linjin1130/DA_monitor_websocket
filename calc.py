# coding: utf-8
import datetime
import struct

def calc_02(x):
    y = 30 + 7.3 * (x - 39200) / 1000
    return round(y,2)

def calc_03(x):
    return str(datetime.timedelta(seconds=x))

def calc_04(x):
    return struct.unpack("<I", struct.pack(">I", x))[0]

def calc_05(x):
    return struct.unpack("<H", struct.pack(">H", x))[0]

def calc_06(x):
    sw_ver = (x & 0xFF000000) >> 24
    hw_ver = (x & 0xFF0000) >> 16
    big_ver = (x & 0xFF00) >> 8
    return f'{big_ver:02d}-{hw_ver:03d}-{sw_ver:03d}'

def calc_07(x):
    b = struct.pack('>I', x)
    return '.'.join(str(i) for i in b)

def calc_09(x):
    b = struct.pack('>H', x)
    ser = b[1]
    num = b[0]
    if 2 <= ser <= 14:
        s = chr(ord('A') + ser)
    else:
        s = 'A/B'
    return f'{num:03d}'

def calc_12(x):
    return struct.unpack("<H", struct.pack(">H", x))[0]

def calc_13(x):

    return struct.unpack("<I", struct.pack(">I", x))[0] >> 8

def calc_14(x):
    """
    返回满电流码值对应的电压值
    :param value: 满电流码值
    :return: 电压值
    """
    value = x
    sign = value >> 9
    code = value & 0x1FF
    current = round(20.48 + ((code - (sign << 9)) * 13.1) / 1024, 3)
    # volts = (20.48 + ((code - (sign << 9)) * 13.1) / 512) * 0.05
    return f'{current}mA'