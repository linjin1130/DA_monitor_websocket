import random
from datetime import time, date

import h5py  # 导入工具包
import os
date_str = date.today().strftime("%y%m%d")
file_name = date_str +'.h5'
f = None
if not os.path.exists(file_name):
    print('创建文件')
    f = f = h5py.File(file_name, 'w')
    dset = f.create_dataset(date_str, shape=(3600 * 24, 1024), dtype='i8')
else:
    f = h5py.File(file_name, 'a')  # 创建一个h5文件，文件指针是f
data= [random.randint(0,255) for i in range(3600*25)]
# data= [random.randint(0,255) for i in range(3600*25)]
# data= [i%255 for i in range(3600*25)]
# data = data*1024
print('start')
f[date_str][:,0] = data

# dset = f.create_dataset(date_str, shape=(3600*25, 1024), dtype='i8', compression='gzip')
# dset = f.create_dataset(date_str, shape=(3600*25, 1024), dtype='i8', data=data)
# dset = data
# print(data)
# data = 0
#
# # data.attrs["name"] = u"Hello"
# dt = h5py.special_dtype(vlen=str)     # PY3
# print(f.keys())
# if date_str not in f.keys():
#     print('创建dset')
#     dset = f.create_dataset(date_str, shape=(1, 1), dtype='i8', maxshape=(3600 * 25, 1), compression='gzip')
# else:
#     dset = f[date_str]
#     new_size = dset.size+1
#     dset.resize(new_size, axis=0)
# dset = f[date_str]
# dset[dset.size-1] = data
# size = dset.size
# print(dset[0:dset.size])
# # f[date_str] = data
#
# for i in range(3600 * 25-1):
#     new_size = dset.size + 1
#     dset.resize(new_size, axis=0)
#     dset[dset.size - 1] = i%255
f.close()


