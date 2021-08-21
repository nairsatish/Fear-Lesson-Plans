import h5py
import pandas
import numpy
import matplotlib.pyplot as plt

f = h5py.File('output/syns_pyr2int.h5', 'r')

#temp = f['report']['biophysical']['mapping']

#element_ids = f['report']['biophysical']['mapping']['element_ids'][:]
#element_pos = f['report']['biophysical']['mapping']['element_pos'][:]
#index_pointer = f['report']['biophysical']['mapping']['index_pointer'][:]
#node_ids = f['report']['biophysical']['mapping']['node_ids'][:]
#src_ids = f['report']['biophysical']['mapping']['src_ids'][:]
#time = f['report']['biophysical']['mapping']['time'][:]
#trg_ids = f['report']['biophysical']['mapping']['trg_ids'][:]
data = f['report']['biophysical']['data']
print(data)
plt.plot(data)
plt.xlabel("time")
plt.ylabel('weight')
plt.show()


#code for checking starting weights
"""
path = "updated_conns/tone_biophysical_edges.h5"
f = h5py.File(path, 'r')
weights = f['edges']['tone_biophysical']['0']['syn_weight'][:]
print(weights)
"""