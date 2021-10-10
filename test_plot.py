import h5py
import pandas
import numpy
import matplotlib.pyplot as plt
from bmtk.analyzer.compartment import plot_traces
from bmtk.analyzer.spike_trains import plot_raster

def get_array(path):
    try:
        array = h5py.File(path,'r')
        array = (array['report']['biophysical']['data'][:])
    except:
        pass
    return array

int2pyr = get_array('output/syns_int2pyr.h5')
plot2 = plt.figure(2)
plt.plot(int2pyr)
plt.title("int2pyr weight")
plt.xlabel('time')
plt.ylabel('Weight')

_ = plot_traces(config_file='test_SC.json', node_ids=[0], report_name='v_report',show=False, title='PN cell')
_ = plot_traces(config_file='test_SC.json', node_ids=[1], report_name='v_report',show=False, title='PV cell')

int2pyr = get_array('output/syns_int2pyr_cai.h5')
int2pyr[:] = [x * 1000 for x in int2pyr]
plot2 = plt.figure(1)
plt.plot(int2pyr)
plt.title("int2pyr cai")
plt.xlabel('time')
plt.ylabel('cai (uM)')

pyr2int = get_array('output/syns_pyr2int_cai.h5')
pyr2int[:] = [x * 1000 for x in pyr2int]
plot2 = plt.figure(5)
plt.plot(pyr2int)
plt.title("pyr2int cai")
plt.xlabel('time')
plt.ylabel('cai (uM)')

pyr2int = get_array('output/syns_pyr2int.h5')
plot2 = plt.figure(6)
plt.plot(pyr2int)
plt.title("pyr2int weight")
plt.xlabel('time')
plt.ylabel('Weight')

_ = plot_raster(config_file='test_SC.json', group_by='pop_name', title='raster', show=False)

plt.show()