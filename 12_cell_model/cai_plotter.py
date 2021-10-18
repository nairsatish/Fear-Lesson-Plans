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
int2pyr[:] = [x * 1000 for x in int2pyr]
plot1 = plt.figure(1)
plt.plot(int2pyr)
plt.title("int2pyr cai")
plt.xlabel('time')
plt.ylabel('cai (uM)')

pyr2pyr = get_array('output/syns_pyr2pyr_cai.h5')
pyr2pyr[:] = [x * 1000 for x in pyr2pyr]
plot2 = plt.figure(2)
plt.plot(pyr2pyr)
plt.title("pyr2pyr cai")
plt.xlabel('time')
plt.ylabel('cai (uM)')

pyr2int = get_array('output/syns_pyr2int_cai.h5')
pyr2int[:] = [x * 1000 for x in pyr2int]
plot3 = plt.figure(3)
plt.plot(pyr2int)
plt.title("pyr2int cai")
plt.xlabel('time')
plt.ylabel('cai (uM)')

tone2pyr = get_array('output/syns_tone2pyr_cai.h5')
pyr2int[:] = [x * 1000 for x in pyr2int]
plot3 = plt.figure(4)
plt.plot(tone2pyr)
plt.title("tone2pyr cai")
plt.xlabel('time')
plt.ylabel('cai (uM)')


plt.show()
