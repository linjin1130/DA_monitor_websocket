import random
from datetime import time, date

import h5py  # 导入工具包
import os
f5_names = []
def append(name):
    global f5_names
    f5_names.append(name)

date_str = date.today().strftime("%y%m%d")
date_str = '181121'
file_name = date_str +'.h5'
new_file = 'new'+file_name
with h5py.File(file_name, "r") as f:
    f5_names = []
    f.visit(append)
    with h5py.File(new_file, "w") as nf:
        for key in f5_names:
            if isinstance(f[key], h5py.Dataset):
                dset = f[key]
                print(dset.shape)
                nf.create_dataset(key, dtype='i8', shape=(3600*24, 1024), compression='gzip', data=dset[:,:])

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


