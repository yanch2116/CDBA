# Use this script to convert ROMP's npz file to npy file
# Then you just need to change the npy path in src/server.py
import numpy as np
npz_path = ''
npy_path = ''

a = np.load(
    npz_path, allow_pickle=True)['results'][()]
b = []
for key in a:
    temp = np.append(a[key][0]['poses'], a[key][0]['trans'])
    b.append(temp)
np.save(npy_path, b, allow_pickle=True)
