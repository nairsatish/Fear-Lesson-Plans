from bmtk.analyzer.spike_trains import plot_raster, plot_rates_boxplot, plot_rates
from bmtk.utils.reports.spike_trains import plotting
from bmtk.analyzer.compartment import plot_traces
from bmtk.utils.reports.spike_trains.plotting import plot_raster
import matplotlib.pyplot as plt
import csv
import h5py
import numpy as np
from bmtk.analyzer.spike_trains import to_dataframe
import pandas as pd
from bmtk.analyzer.spike_trains import to_dataframe
import math


#df = to_dataframe(config_file='simulation_config.json')

#plot_raster(config_file='simulation_config.json', group_by='pop_name')
#plotting.plot_raster("./output/spikes.h5",node_groups=[{'node_ids': range(0, 3), 'c': 'b', 'label': 'pyr'}],
#                     times=(0,1000))
#plot_rates(config_file='simulation_config.json', group_by='pop_name')
#plot_rates_boxplot(config_file='simulation_config.json', group_by='pop_name')
#_ = plot_traces(config_file='simulation_config.json', group_by='pop_name', report_name='v_report')
#_ = plot_traces(config_file='simulation_config.json', node_ids=[0], report_name='v_report')
#_ = plot_traces(config_file='simulation_config.json', node_ids=[0], report_name='cai_report')

#plot_raster('output/spikes.h5',
#node_groups=[{'node_ids': range(0, 1), 'c': 'b', 'label': 'pyr'},
#             {'node_ids': range(1, 2), 'c': 'r', 'label': 'inh'}])

def plot_v_report():
    v_report = './output/v_report.h5'
    f = h5py.File(v_report, "r")
    data = (f['report']['biophysical']['data'])
    plt.figure()
    plt.plot(data[:, 0])
    plt.show()
    plt.close()

def plot_spikes():
    #math to make
    #w = 10
    #n = math.ceil((data.max() - data.min()) / w)

    df = to_dataframe(config_file='simulation_config.json')
    fig, axs = plt.subplots(3, 3, sharey=True, tight_layout=True)
    fig.suptitle('Total spike histogram')
    df0 = df.loc[df['node_ids'] == 0]
    df1 = df.loc[df['node_ids'] == 1]
    df2 = df.loc[df['node_ids'] == 2]
    df3 = df.loc[df['node_ids'] == 3]
    df4 = df.loc[df['node_ids'] == 4]
    df5 = df.loc[df['node_ids'] == 5]
    df6 = df.loc[df['node_ids'] == 6]
    df7 = df.loc[df['node_ids'] == 7]
    df8 = df.loc[df['node_ids'] == 8]
    x0 = df0['timestamps'].tolist()
    x1 = df1['timestamps'].tolist()
    x2 = df2['timestamps'].tolist()
    x3 = df3['timestamps'].tolist()
    x4 = df4['timestamps'].tolist()
    x5 = df5['timestamps'].tolist()
    x6 = df6['timestamps'].tolist()
    x7 = df7['timestamps'].tolist()
    x8 = df8['timestamps'].tolist()
    axs[0, 0].hist(x=x0,bins=10)
    axs[0, 0].set_title('P1')
    # axs[0, 0].set_xlim([0, 1500])
    axs[0, 1].hist(x=x1)
    axs[0, 1].set_title('P2')
    # axs[0, 1].set_xlim([0, 1500])
    axs[0, 2].hist(x=x2)
    axs[0, 2].set_title('P3')
    # axs[0, 2].set_xlim([0, 1500])
    axs[1, 0].hist(x=x3)
    axs[1, 0].set_title('P4')
    # axs[1, 0].set_xlim([0, 1500])
    axs[1, 1].hist(x=x4)
    axs[1, 1].set_title('P5')
    # axs[1, 1].set_xlim([0, 1500])
    axs[1, 2].hist(x=x5)
    axs[1, 2].set_title('P6')
    # axs[1, 2].set_xlim([0, 1500])
    axs[2, 0].hist(x=x6)
    axs[2, 0].set_title('P7')
    # axs[2, 0].set_xlim([0, 1500])
    axs[2, 1].hist(x=x7)
    axs[2, 1].set_title('P8')
    # axs[2, 1].set_xlim([0, 1500])
    axs[2, 2].hist(x=x8)
    axs[2, 2].set_title('I1')
    # axs[2, 2].set_xlim([0, 1500])
    for ax in axs.flat:
        ax.set(xlabel='time(ms)', ylabel='# of spikes')
    plt.show()
    plt.show()

def tone_and_shock_plot():
    #load tone and shoock files
    shock_file = 'shock_spikes.csv'
    tone_file = 'tone_spikes.csv'

    shock_array = []
    with open(shock_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            shock_array.append(row)

    #print(shock_array)
    shock_x = []
    shock_y = []
    for element in shock_array:
        word = element[0].split('\'')
        #print(word[0])
        #print(int(word[2]))
        #print(int(word[0]))
        #exit(1)
        if len(shock_x) == 5:
            #break
            pass
        shock_x.append(int(word[0]))
        shock_y.append(int(word[2]))

    tone_array = []
    with open(tone_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            tone_array.append(row)

    #print(tone_array)
    tone_x = []
    tone_y = []
    for element in tone_array:
        word = element[0].split('\'')
        #print(word[0])
        if len(tone_x) == 5:
            #break
            pass
        tone_x.append(int(word[0]))
        tone_y.append(int(word[2]))

    plt.plot(tone_x, tone_y, '.', label="tone input")
    plt.plot(shock_x, shock_y, '.', label="shock input")
    plt.xlabel("Time elapsed")
    plt.ylabel("Node id")
    plt.legend()
    plt.show()

def membrane_potenial_plot(): # not a good function thing labels are off
    mem_pot_file = './output/v_report.h5'
    f = h5py.File(mem_pot_file, 'r')
    mem_potential = f['report']['biophysical']['data']
    plt.plot(np.arange(0, mem_potential.shape[0] / 10, .1), mem_potential[:, 0])
    plt.text(200, -80, 'tone')
    plt.text(700, -80, 'tone+shock')
    plt.text(1600, -80, 'tone+shock')
    plt.text(2600, -80, 'tone')
    plt.xlabel('time (ms)')
    plt.ylabel('membrane potential (mV)')
    plt.show()

def plot_9_spikes_400():
    h = h5py.File('output/spikes.h5', 'r')
    timestamps = h['spikes']['biophysical']['timestamps'][:]
    node_ids = h['spikes']['biophysical']['node_ids'][:]
    df = pd.DataFrame({'node_ids': node_ids, 'ts': timestamps})
    fig, axs = plt.subplots(3, 3, sharey=True, tight_layout=True)
    fig.suptitle('Spike histogram for the first 400 ms')
    axs[0, 0].hist(df.loc[(df.node_ids == 0) & (df.ts <= 400)])
    axs[0, 0].set_title('P1')
    axs[0, 0].set_xlim([0, 400])
    axs[0, 1].hist(df.loc[(df.node_ids == 1) & (df.ts <= 400)])
    axs[0, 1].set_title('P2')
    axs[0, 1].set_xlim([0, 400])
    axs[0, 2].hist(df.loc[(df.node_ids == 2) & (df.ts <= 400)])
    axs[0, 2].set_title('P3')
    axs[0, 2].set_xlim([0, 400])
    axs[1, 0].hist(df.loc[(df.node_ids == 3) & (df.ts <= 400)])
    axs[1, 0].set_title('P4')
    axs[1, 0].set_xlim([0, 400])
    axs[1, 1].hist(df.loc[(df.node_ids == 4) & (df.ts <= 400)])
    axs[1, 1].set_title('P5')
    axs[1, 1].set_xlim([0, 400])
    axs[1, 2].hist(df.loc[(df.node_ids == 5) & (df.ts <= 400)])
    axs[1, 2].set_title('P6')
    axs[1, 2].set_xlim([0, 400])
    axs[2, 0].hist(df.loc[(df.node_ids == 6) & (df.ts <= 400)])
    axs[2, 0].set_title('P7')
    axs[2, 0].set_xlim([0, 400])
    axs[2, 1].hist(df.loc[(df.node_ids == 7) & (df.ts <= 400)])
    axs[2, 1].set_title('P8')
    axs[2, 1].set_xlim([0, 400])
    axs[2, 2].hist(df.loc[(df.node_ids == 8) & (df.ts <= 400)])
    axs[2, 2].set_title('I1')
    axs[2, 2].set_xlim([0, 400])
    # axs[0,0].plot(dh.loc[(dh.node_ids==9) & (dh.ts <= 400)])
    for ax in axs.flat:
        ax.set(xlabel='time(ms)', ylabel='# of spikes')
    plt.show()


def plot_9_spikes():
    h = h5py.File('output/spikes.h5', 'r')
    timestamps = h['spikes']['biophysical']['timestamps'][:]
    node_ids = h['spikes']['biophysical']['node_ids'][:]
    df = pd.DataFrame({'node_ids': node_ids, 'ts': timestamps})
    fig, axs = plt.subplots(3, 3, sharey=True, tight_layout=True)
    fig.suptitle('Total spike histogram')
    axs[0, 0].hist(df.loc[(df.node_ids == 0)])
    axs[0, 0].set_title('P1')
    #axs[0, 0].set_xlim([0, 1500])
    axs[0, 1].hist(df.loc[(df.node_ids == 1)])
    axs[0, 1].set_title('P2')
    #axs[0, 1].set_xlim([0, 1500])
    axs[0, 2].hist(df.loc[(df.node_ids == 2)])
    axs[0, 2].set_title('P3')
    #axs[0, 2].set_xlim([0, 1500])
    axs[1, 0].hist(df.loc[(df.node_ids == 3)])
    axs[1, 0].set_title('P4')
    #axs[1, 0].set_xlim([0, 1500])
    axs[1, 1].hist(df.loc[(df.node_ids == 4)])
    axs[1, 1].set_title('P5')
    #axs[1, 1].set_xlim([0, 1500])
    axs[1, 2].hist(df.loc[(df.node_ids == 5)])
    axs[1, 2].set_title('P6')
    #axs[1, 2].set_xlim([0, 1500])
    axs[2, 0].hist(df.loc[(df.node_ids == 6)])
    axs[2, 0].set_title('P7')
    #axs[2, 0].set_xlim([0, 1500])
    axs[2, 1].hist(df.loc[(df.node_ids == 7)])
    axs[2, 1].set_title('P8')
    #axs[2, 1].set_xlim([0, 1500])
    axs[2, 2].hist(df.loc[(df.node_ids == 8)])
    axs[2, 2].set_title('I1')
    #axs[2, 2].set_xlim([0, 1500])
    for ax in axs.flat:
        ax.set(xlabel='time(ms)', ylabel='# of spikes')
    plt.show()

plot_spikes()
#plot_9_spikes_400()
#plot_9_spikes()

#plot_v_report()
#tone_and_shock_plot()



