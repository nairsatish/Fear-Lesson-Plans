import h5py
from pathlib import Path
import os
import pandas as pd
import matplotlib.pyplot as plt

f = h5py.File('network\\biophysical_biophysical_edges.h5', 'r')
sid = f['edges']['biophysical_to_biophysical']['source_node_id'][:]
tid = f['edges']['biophysical_to_biophysical']['target_node_id'][:]
#print(sid)
#print(tid)

df = pd.DataFrame({'sid':sid, 'tid':tid})
print(df.head())

g = h5py.File('network\\tone_biophysical_edges.h5', 'r')
edge_sid = g['edges']['tone_to_biophysical']['source_node_id'][:]
edge_tid = g['edges']['tone_to_biophysical']['target_node_id'][:]

dg = pd.DataFrame({'sid':sid, 'tid':tid})
print(dg.head())

#output file lookin
h = h5py.File('output\\spikes.h5', 'r')
timestamps = h['spikes']['biophysical']['timestamps'][:]
node_ids = h['spikes']['biophysical']['node_ids'][:]



dh = pd.DataFrame({'node_ids':node_ids, 'ts':timestamps})
print(dh.head())
plt.plot(dh.ts, dh.node_ids, '.')
plt.show()



i = h5py.File('output\\v_report.h5', 'r')
data = i['report']['biophysical']['data'][:]
time = i['report']['biophysical']['mapping']['time'][:]
print(data)
print(time)

i = h5py.File('output\\cai_report.h5', 'r')
data = i['report']['biophysical']['data'][:]
time = i['report']['biophysical']['mapping']['time']
print(data)
print('new')
print(time)
# dh = pd.DataFrame({'data':data, 'time':time})
# plt.plot(dh.time, dh.data)