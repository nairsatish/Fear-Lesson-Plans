import matplotlib.pyplot as plt
from bmtk.analyzer.spike_trains import plot_raster, plot_rates_boxplot, plot_rates
from bmtk.analyzer.compartment import plot_traces
import numpy as np
import h5py
import pandas as pd

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

def raster(spikes_df, node_set, start=0,end=80000, ax=None):
    spikes_df = spikes_df[spikes_df['timestamps'] > start]
    spikes_df = spikes_df[spikes_df['timestamps'] < end]
    for node in node_set:
        cells = range(node['start'], node['end'] + 1)  # +1 to be inclusive of last cell
        cell_spikes = spikes_df[spikes_df['node_ids'].isin(cells)]

        ax.scatter(cell_spikes['timestamps'], cell_spikes['node_ids'],
                   c='tab:' + node['color'], s=5, label=node['name'])

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(reversed(handles), reversed(labels),loc='lower right')
    ax.grid(False)

def spike_frequency_bar_graph(spikes_df, node_set, ms, start=0, end=80000, ax=None, n_bins=10):
    mean = []
    name = []
    labels = []
    for node in node_set:
        cells = range(node['start'], node['end'] + 1)  # +1 to be inclusive of last cell
        cell_spikes = spikes_df[spikes_df['node_ids'].isin(cells)]

        # skip the first few ms
        cell_spikes = cell_spikes[cell_spikes['timestamps'] > start]
        cell_spikes = cell_spikes[cell_spikes['timestamps'] < end]
        spike_counts = cell_spikes.node_ids.value_counts()
        total_seconds = (ms) / 1000
        spike_counts_per_second = spike_counts / total_seconds

        spikes_mean = spike_counts_per_second.mean()
        spikes_std = spike_counts_per_second.std()

        label = "{} : {:.2f} ({:.2f})".format(node['name'], spikes_mean, spikes_std)
        #print(label)
        c = "tab:" + node['color']
        if ax:
            mean.append(spikes_mean)
            name.append(node['name'])
            labels.append(label)
            ax.bar(node['name'], spikes_mean,label=label,color=c)


    if ax:
        ax.legend()

#plot_syn_weight()
#plot_cai()

f = h5py.File('output/spikes.h5','r')
spikes_df = pd.DataFrame({'node_ids':f['spikes']['biophysical']['node_ids'],'timestamps':f['spikes']['biophysical']['timestamps']})
node_set = [
    {"name": "PN_A", "start": 0, "end": 4, "color": "blue"},
    {"name": "PN_C", "start": 5, "end": 7, "color": "pink"},
    {"name": "SOM", "start": 8, "end": 9, "color": "red"},
    {"name": "PV", "start": 10, "end": 11, "color": "orange"}
]
fig, axs = plt.subplots(2,2,figsize=(12,4.8))#6.4,4.8 default
axs[0,0].set_title("sen period")
axs[0,1].set_title('condition period')
start1 = 4000
end1 = 5000
start2 = 52000
end2 = 53000
raster(spikes_df, node_set, start=start1, end=end1, ax=axs[0,0])
raster(spikes_df, node_set, start=start2, end=end2, ax=axs[0,1])
spike_frequency_bar_graph(spikes_df,node_set,start=start1,end=end1,ax=axs[1,0],ms=(end1-start1))
spike_frequency_bar_graph(spikes_df,node_set,start=start2,end=end2,ax=axs[1,1],ms=(end2-start2))

plt.show()

