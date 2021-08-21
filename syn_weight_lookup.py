import h5py
import pandas
import numpy
import matplotlib.pyplot as plt

f = h5py.File('output/syns.h5','r')

temp = f['report']['biophysical']['mapping']

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
#numpy.savetxt('syn_report.csv', data, delimiter=",")

