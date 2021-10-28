from bmtk.analyzer.spike_trains import to_dataframe
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

df = to_dataframe(config_file='simulation_config_W+Cai.json')
#df0 = df.loc[df['node_ids'] == 0]
#df0.to_csv("spikes.csv")
node_spike_array = []

def tone_response(node_spike_array):
    node_num = 0

    while(node_num <= 11):
        df0 = df.loc[df['node_ids'] == node_num]

        x0 = df0['timestamps'].tolist()
        first_trial = []
        second_trial = []
        third_trial = []
        fourth_trial = []
        fifth_trial = []
        sixth_trial = []
        seventh_trial = []
        eighth_trial = []
        ninth_trial = []
        tenth_trial = []

        for i in range(len(x0)):
            if (x0[i] >= 0 and x0[i] <= 400):
                first_trial.append(x0[i])
            if (x0[i] >= 4000 and x0[i] <= 4400):
                second_trial.append(x0[i])
            if (x0[i] >= 8000 and x0[i] <= 8400):
                third_trial.append(x0[i])
            if (x0[i] >= 12000 and x0[i] <= 12400):
                fourth_trial.append(x0[i])
            if (x0[i] >= 16000 and x0[i] <= 16400):
                fifth_trial.append(x0[i])
            if (x0[i] >= 20000 and x0[i] <= 20400):
                sixth_trial.append(x0[i])
            if (x0[i] >= 24000 and x0[i] <= 24400):
                seventh_trial.append(x0[i])
            if (x0[i] >= 28000 and x0[i] <= 28400):
                eighth_trial.append(x0[i])
            if (x0[i] >= 32000 and x0[i] <= 32400):
                ninth_trial.append(x0[i])
            if (x0[i] >= 36000 and x0[i] <= 36400):
                tenth_trial.append(x0[i])

        for i in range(len(second_trial)):
            second_trial[i] -= 4000
        for i in range(len(third_trial)):
            third_trial[i] -= 8000
        for i in range(len(fourth_trial)):
            fourth_trial[i] -= 12000
        for i in range(len(fifth_trial)):
            fifth_trial[i] -= 16000
        for i in range(len(sixth_trial)):
            sixth_trial[i] -= 20000
        for i in range(len(seventh_trial)):
            seventh_trial[i] -= 24000
        for i in range(len(eighth_trial)):
            eighth_trial[i] -= 28000
        for i in range(len(ninth_trial)):
            ninth_trial[i] -= 32000
        for i in range(len(tenth_trial)):
            tenth_trial[i] -= 36000

        final_array = np.concatenate((first_trial, second_trial, third_trial, fourth_trial,
                                      fifth_trial, sixth_trial, seventh_trial, eighth_trial,
                                      ninth_trial, tenth_trial))

        node_spike_array.append(final_array)

        node_num = node_num+1

def find_bins(array, width):
    minimmum = np.min(array)
    maximmum = np.max(array)
    bound_min = -1.0 * (minimmum % width - minimmum)
    bound_max = maximmum - maximmum % width + width
    n = int((bound_max - bound_min) / width) + 1
    bins = np.linspace(bound_min, bound_max, n)
    return bins

def set_up_graphs_sense():
    fig, axs = plt.subplots(4, 3, sharey=True, tight_layout=True, sharex=True)
    fig.suptitle('Spike histogram sensitization', y=1)

    i = 0
    column_cnt = 0
    row_cnt = 0

    while (i < 12):
        bins = find_bins(node_spike_array[i], 10)

        axs[row_cnt, column_cnt].hist(x=node_spike_array[i], bins=bins)
        axs[row_cnt, column_cnt].set_title('PN' + str(i + 1))
        if (i == 8):
            axs[row_cnt, column_cnt].set_title('OLM 1 ')
        if (i == 9):
            axs[row_cnt, column_cnt].set_title('OLM 2 ')
        if (i == 10):
            axs[row_cnt, column_cnt].set_title('PV 1 ')
        if (i == 11):
            axs[row_cnt, column_cnt].set_title('PV 2 ')
        # axs[row_cnt, column_cnt].ylabel("spikes")
        # axs[row_cnt, column_cnt].xlabel('ms')

        axs[row_cnt, column_cnt].set_xlim([0, 400])

        column_cnt = column_cnt + 1
        if (column_cnt > 2):
            column_cnt = 0
            row_cnt = row_cnt + 1

        i = i + 1

    plt.setp(axs[-1, :], xlabel='time (ms)')
    plt.setp(axs[:, 0], ylabel='spike count')

def spike_freq_bar_tone():
    hz = []
    for i in range(12):
        hz.append(((len(node_spike_array[i]))/0.4)/10) # calculates firing rate in Hz

    plot2 = plt.figure(2)
    x = [0,1,2,3,4,5,6,7,8,9,10,11]
    cells = ["PN1", "PN2", "PN3", "PN4", "PN5", "PN6", "PN7", "PN8", "SOM1", "SOM2", "PV1", "PV2"]
    plt.xticks(x, cells)
    plt.bar(height=hz,x=cells)
    plt.title("firing rates during tone during sensitization")
    plt.xlabel("cells")
    plt.ylabel("firing rate (Hz)")
    plt.grid()

def create_arrays_extinction_early(node_spike_array):
    total_spikes = []
    timestamp = 116000
    node_num = 0
    while(node_num <= 12):
        df0 = df.loc[df['node_ids'] == node_num]
        df0.sort_values(by=['timestamps'])
        x0 = df0['timestamps'].tolist()
        trial_spikes = []
        i = 0
        while(i < 10):
            for j in range(len(x0)):
                if(x0[j] >= timestamp+(i*4000) and x0[j] <= timestamp+(i*4000+400)):
                    value = (x0[j]-(i*4000) - timestamp)
                    trial_spikes.append(value)

        #should go through all 30 trials and get every value and condense them
            i = i+1

        # should create a list of lists 12 of them each one being a node
        node_spike_array.append(trial_spikes)
        node_num = node_num+1
    #print(total_spikes)
    #node_spike_array = total_spikes
    #print(node_spike_array)

def set_up_graphs_EE():
    fig, axs = plt.subplots(4, 3, sharey=True, tight_layout=True, sharex=True)
    fig.suptitle('Spike histogram for early extinction', y=1)

    i = 0
    column_cnt = 0
    row_cnt = 0

    while (i < 12):
        bins = find_bins(extinction_array[i], 10)

        axs[row_cnt, column_cnt].hist(x=extinction_array[i], bins=bins)
        axs[row_cnt, column_cnt].set_title('PN ' + str(i + 1))
        if (i == 8):
            axs[row_cnt, column_cnt].set_title('OLM 1 ')
        if (i == 9):
            axs[row_cnt, column_cnt].set_title('OLM 2 ')
        if (i == 10):
            axs[row_cnt, column_cnt].set_title('PV 1 ')
        if (i == 11):
            axs[row_cnt, column_cnt].set_title('PV 1 ')
        # axs[row_cnt, column_cnt].ylabel("spikes")
        # axs[row_cnt, column_cnt].xlabel('ms')

        # axs[row_cnt, column_cnt].set_xlim([0,400])

        column_cnt = column_cnt + 1
        if (column_cnt > 2):
            column_cnt = 0
            row_cnt = row_cnt + 1

        i = i + 1

    plt.setp(axs[-1, :], xlabel='time (ms)')
    plt.setp(axs[:, 0], ylabel='spike count')

tone_response(node_spike_array)

set_up_graphs_sense()

spike_freq_bar_tone()

#EE stuff
extinction_array = []
#create_arrays_extinction_early(extinction_array)
#set_up_graphs_EE()

plt.show()

shock_response_arr = []
def shock_response(node_spike_array):
    node_num = 0

    while(node_num <= 11):
        df0 = df.loc[df['node_ids'] == node_num]

        x0 = df0['timestamps'].tolist()
        first_trial = []
        second_trial = []
        third_trial = []
        fourth_trial = []
        fifth_trial = []
        sixth_trial = []
        seventh_trial = []
        eighth_trial = []
        ninth_trial = []
        tenth_trial = []

        for i in range(len(x0)):
            if (x0[i] >= 1750 and x0[i] <= 1850):
                first_trial.append(x0[i])
            if (x0[i] >= 5750 and x0[i] <= 5850):
                second_trial.append(x0[i])
            if (x0[i] >= 9750 and x0[i] <= 9850):
                third_trial.append(x0[i])
            if (x0[i] >= 13750 and x0[i] <= 13850):
                fourth_trial.append(x0[i])
            if (x0[i] >= 17750 and x0[i] <= 17850):
                fifth_trial.append(x0[i])
            if (x0[i] >= 21750 and x0[i] <= 21850):
                sixth_trial.append(x0[i])
            if (x0[i] >= 25750 and x0[i] <= 25850):
                seventh_trial.append(x0[i])
            if (x0[i] >= 29750 and x0[i] <= 29850):
                eighth_trial.append(x0[i])
            if (x0[i] >= 33750 and x0[i] <= 33850):
                ninth_trial.append(x0[i])
            if (x0[i] >= 37750 and x0[i] <= 37850):
                tenth_trial.append(x0[i])
        """
        for i in range(len(second_trial)):
            second_trial[i] -= 5750
        for i in range(len(third_trial)):
            third_trial[i] -= 9750
        for i in range(len(fourth_trial)):
            fourth_trial[i] -= 13750
        for i in range(len(fifth_trial)):
            fifth_trial[i] -= 
        for i in range(len(sixth_trial)):
            sixth_trial[i] -= 25750
        for i in range(len(seventh_trial)):
            seventh_trial[i] -= 29750
        for i in range(len(eighth_trial)):
            eighth_trial[i] -= 33750
        for i in range(len(ninth_trial)):
            ninth_trial[i] -= 32000
        for i in range(len(tenth_trial)):
            tenth_trial[i] -= 36000
        """

        final_array = np.concatenate((first_trial, second_trial, third_trial, fourth_trial,
                                      fifth_trial, sixth_trial, seventh_trial, eighth_trial,
                                      ninth_trial, tenth_trial))

        node_spike_array.append(final_array)

        node_num = node_num+1

def spike_freq_bar_shock():
    hz = []
    for i in range(12):
        hz.append(((len(shock_response_arr[i]))/0.1)/10) # calculates firing rate in Hz

    print(shock_response_arr[9])
    plot2 = plt.figure(3)
    x = [0,1,2,3,4,5,6,7,8,9,10,11]
    cells = ["PN1", "PN2", "PN3", "PN4", "PN5", "PN6", "PN7", "PN8", "SOM1", "SOM2", "PV1", "PV2"]
    plt.xticks(x, cells)
    plt.bar(height=hz,x=cells)
    plt.title("firing rates during shock during sensitization")
    plt.xlabel("cells")
    plt.ylabel("firing rate (Hz)")
    plt.grid()

shock_response(shock_response_arr)

spike_freq_bar_shock()

plt.show()