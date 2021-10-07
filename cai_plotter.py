from bmtk.analyzer.compartment import plot_traces
import matplotlib.pyplot as plt
import h5py

def get_array(path):
    try:
        array = h5py.File(path,'r')
        array = (array['report']['biophysical']['data'][:])
    except:
        pass
    return array


int2pyr = get_array('output/syns_int2pyr_cai.h5')
plot2 = plt.figure(2)
plt.plot(int2pyr)
plt.title("int2pyr cai")
plt.xlabel('time')
plt.ylabel('cai')
"""
pyr2pyr = get_array('output/syns_pyr2pyr_cai.h5')
plot2 = plt.figure(2)
plt.plot(pyr2pyr)
plt.title("pyr2pyr cai")
plt.xlabel('time')
plt.ylabel('cai')

pyr2int = get_array('output/syns_pyr2int_cai.h5')
plot2 = plt.figure(2)
plt.plot(pyr2int)
plt.title("pyr2int cai")
plt.xlabel('time')
plt.ylabel('cai')
"""

plt.show()
