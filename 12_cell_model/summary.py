import matplotlib.pyplot as plt
from bmtk.analyzer.spike_trains import plot_raster, plot_rates_boxplot
from bmtk.analyzer.compartment import plot_traces
import h5py

def get_array(path):
    try:
        array = h5py.File(path,'r')
        array = (array['report']['biophysical']['data'][:])
    except:
        pass
    return array

def plot_syn_weight():
    int2pyr = get_array('output/syns_int2pyr.h5')
    pyr2pyr = get_array('output/syns_pyr2pyr.h5')
    pyr2int = get_array('output/syns_pyr2int.h5')
    tone2pyr = get_array('output/syns_tone2pyr.h5')


    fig, axs = plt.subplots(2,2, sharex=True, tight_layout=True)
    fig.suptitle('syn weights')
    axs[0, 0].plot(int2pyr)
    axs[0, 0].set_title("int2pyr syn weight")
    axs[0, 1].plot(pyr2pyr)
    axs[0, 1].set_title("pyr2pyr syn weight")
    axs[1, 0].plot(pyr2int)
    axs[1, 0].set_title("pyr2int syn weight")
    axs[1, 1].plot(tone2pyr)
    axs[1, 1].set_title("tone2pyr syn weight")

    plt.show()

def plot_cai():
    int2pyr = get_array('output/syns_int2pyr_cai.h5')
    int2pyr[:] = [x * 1000 for x in int2pyr]
    pyr2pyr = get_array('output/syns_pyr2pyr_cai.h5')
    pyr2pyr[:] = [x * 1000 for x in pyr2pyr]
    pyr2int = get_array('output/syns_pyr2int_cai.h5')
    pyr2int[:] = [x * 1000 for x in pyr2int]
    tone2pyr = get_array('output/syns_cai.h5')
    #tone2pyr[:] = [x * 1000 for x in tone2pyr]


    fig, axs = plt.subplots(2,2, sharex=True, tight_layout=True)
    fig.suptitle('cai')
    axs[0, 0].plot(int2pyr)
    axs[0, 0].set_title("int2pyr cai")
    axs[0, 1].plot(pyr2pyr)
    axs[0, 1].set_title("pyr2pyr cai")
    axs[1, 0].plot(pyr2int)
    axs[1, 0].set_title("pyr2int cai")
    axs[1, 1].plot(tone2pyr)
    axs[1, 1].set_title("tone2pyr cai")

    plt.show()


#plot_syn_weight()
#plot_cai()

time = (52000, 53000)  # full time is 232500 sense period is 40000
plot_raster = plot_raster(config_file='simulation_config_W+Cai.json', group_by='pop_name', title='raster', times=time)
plot_boxplot = plot_rates_boxplot(config_file='simulation_config_W+Cai.json', group_by='pop_name', title='boxplot',times=time)
v_report = plot_traces(config_file='simulation_config_W+Cai.json', node_ids=[10], title='voltage report', times=time)
