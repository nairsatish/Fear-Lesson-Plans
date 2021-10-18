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

#int2int = get_array('output/syns_int2int.h5')
#plot1 = plt.figure(1)
#plt.plot(int2int)
#plt.title("int2int weight")
#plt.xlabel('time')
#plt.ylabel('Weight')

int2pyr = get_array('output/syns_int2pyr.h5')
plot2 = plt.figure(2)
plt.plot(int2pyr)
plt.title("int2pyr weight")
plt.xlabel('time')
plt.ylabel('Weight')

pyr2pyr = get_array('output/syns_pyr2pyr.h5')
plot3 = plt.figure(3)
plt.plot(pyr2pyr)
plt.title("pyr2pyr weight")
plt.xlabel('time')
plt.ylabel('Weight')

pyr2int = get_array('output/syns_pyr2int.h5')
plot4 = plt.figure(4)
plt.plot(pyr2int)
plt.title("pyr2int weight")
plt.xlabel('time')
plt.ylabel('Weight')

tone2pyr = get_array('output/syns_tone2pyr.h5')
plot4 = plt.figure(5)
plt.plot(tone2pyr)
plt.title("tone2pyr weight")
plt.xlabel('time')
plt.ylabel('Weight')

plt.show()


