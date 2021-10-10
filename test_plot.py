import h5py
import pandas
import numpy
import matplotlib.pyplot as plt
from bmtk.analyzer.compartment import plot_traces

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
_ = plot_traces(config_file='test_SC.json', node_ids=[1], report_name='v_report',show=False, title='SOM cell')

int2pyr = get_array('output/syns_int2pyr_cai.h5')
plot2 = plt.figure(1)
plt.plot(int2pyr)
plt.title("int2pyr cai")
plt.xlabel('time')
plt.ylabel('cai')

plt.show()