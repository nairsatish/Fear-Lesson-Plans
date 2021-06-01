from bmtk.analyzer.spike_trains import to_dataframe
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

df = to_dataframe(config_file='simulation_config.json')

df.to_csv('spikedata.csv')

# df0 = df.loc[df['node_ids'] == 0]
# #df0.to_csv('node0.csv')
# x0 = df0['timestamps'].tolist()
# first_trial = []
# second_trial = []
# third_trial = []
# fourth_trial = []
# fifth_trial = []
# sixth_trial = []
# seventh_trial = []
# eighth_trial = []
# ninth_trial = []
# tenth_trial = []
#
# #split values into different arrays
# for i in range(len(x0)):
#     if (x0[i] >= 0 and x0[i] <= 400):
#         first_trial.append(x0[i])
#     if (x0[i] >= 4000 and x0[i] <= 4400):
#         second_trial.append(x0[i])
#     if (x0[i] >= 8000 and x0[i] <= 8400):
#         third_trial.append(x0[i])
#     if (x0[i] >= 12000 and x0[i] <= 12400):
#         fourth_trial.append(x0[i])
#     if (x0[i] >= 16000 and x0[i] <= 16400):
#         fifth_trial.append(x0[i])
#     if (x0[i] >= 20000 and x0[i] <= 20400):
#         sixth_trial.append(x0[i])
#     if (x0[i] >= 24000 and x0[i] <= 24400):
#         seventh_trial.append(x0[i])
#     if (x0[i] >= 28000 and x0[i] <= 28400):
#         eighth_trial.append(x0[i])
#     if (x0[i] >= 32000 and x0[i] <= 32400):
#         ninth_trial.append(x0[i])
#     if (x0[i] >= 36000 and x0[i] <= 36400):
#         tenth_trial.append(x0[i])
#
# #scaling values
# for i in range(len(second_trial)):
#     second_trial[i] -= 4000
# for i in range(len(third_trial)):
#     third_trial[i] -= 8000
# for i in range(len(fourth_trial)):
#     fourth_trial[i] -= 12000
# for i in range(len(fifth_trial)):
#     fifth_trial[i] -= 16000
# for i in range(len(sixth_trial)):
#     sixth_trial[i] -= 20000
# for i in range(len(seventh_trial)):
#     seventh_trial[i] -= 24000
# for i in range(len(eighth_trial)):
#     eighth_trial[i] -= 28000
# for i in range(len(ninth_trial)):
#     ninth_trial[i] -= 32000
# for i in range(len(tenth_trial)):
#     tenth_trial[i] -= 36000
#
# final_array = np.concatenate((first_trial, second_trial, third_trial, fourth_trial,
#                               fifth_trial, sixth_trial, seventh_trial, eighth_trial,
#                               ninth_trial, tenth_trial))
#
#

# bins = find_bins(final_array, 10)
# plt.hist(x=final_array, bins=bins)
# plt.title('P1')
# plt.ylabel("spikes")
# plt.xlabel('ms')
# plt.xlim([0, 400])
# plt.show()

test = []
df0 = df.loc[df['node_ids'] == 0]
max_value = df0.max()

x0 = df0['timestamps'].tolist()



node_spike_array = []
def create_arrays(node_spike_array):
    node_num = 0

    while(node_num <= 9):
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

create_arrays(node_spike_array)

fig, axs = plt.subplots(3, 3, sharey=True, tight_layout=True)
fig.suptitle('Spike histogram for the first 400 ms')

i = 0
column_cnt = 0
row_cnt = 0

while(i < 9):
    bins = find_bins(node_spike_array[i], 10)

    axs[row_cnt, column_cnt].hist(x=node_spike_array[i], bins=bins)
    axs[row_cnt, column_cnt].set_title('pyramidal ' + str(i+1))
    if(i == 8):
        axs[row_cnt, column_cnt].set_title('Interneuron 1 ')
    # axs[row_cnt, column_cnt].ylabel("spikes")
    # axs[row_cnt, column_cnt].xlabel('ms')

    axs[row_cnt, column_cnt].set_xlim([0,400])


    column_cnt = column_cnt+1
    if(column_cnt > 2):
        column_cnt = 0
        row_cnt = row_cnt+1


    i = i+1

for ax in axs.flat:
    ax.set(xlabel='time(ms)', ylabel='# of spikes')
plt.show()

def create_arrays_extinction(node_spike_array):
    total_spikes = []
    timestamp = 76000
    node_num = 0
    while(node_num <= 9):
        df0 = df.loc[df['node_ids'] == node_num]
        x0 = df0['timestamps'].tolist()
        trial_spikes = []
        i = 0
        while(i < 30):
            for j in range(len(x0)):
                if(x0[j] >= timestamp+(i*4000) and x0[j] <= timestamp+(i*4000+400)):
                    value = x0[j]-(i*4000)
                    trial_spikes.append(value)
        #should go through all 30 trials and get every value and condense them
            i = i+1

        # should create a list of lists 9 of them each one being a node
        node_spike_array.append(trial_spikes)
        node_num = node_num+1

    #print(total_spikes)
    #node_spike_array = total_spikes
    print(node_spike_array)


extinction_array = []
create_arrays_extinction(extinction_array)
print(extinction_array)

fig, axs = plt.subplots(3, 3, sharey=True, tight_layout=True)
fig.suptitle('Spike histogram for extinction ms')

i = 0
column_cnt = 0
row_cnt = 0

while(i < 9):
    bins = find_bins(extinction_array[i], 10)

    axs[row_cnt, column_cnt].hist(x=extinction_array[i], bins=bins)
    axs[row_cnt, column_cnt].set_title('pyramidal ' + str(i+1))
    if(i == 8):
        axs[row_cnt, column_cnt].set_title('Interneuron 1 ')
    # axs[row_cnt, column_cnt].ylabel("spikes")
    # axs[row_cnt, column_cnt].xlabel('ms')

    #axs[row_cnt, column_cnt].set_xlim([0,400])


    column_cnt = column_cnt+1
    if(column_cnt > 2):
        column_cnt = 0
        row_cnt = row_cnt+1


    i = i+1

for ax in axs.flat:
    ax.set(xlabel='time(ms)', ylabel='# of spikes')
plt.show()

def create_arrays_extinction_final(node_spike_array):
    total_spikes = []
    timestamp = 116400
    node_num = 0
    while(node_num <= 9):
        df0 = df.loc[df['node_ids'] == node_num]
        x0 = df0['timestamps'].tolist()
        trial_spikes = []
        i = 0
        while(i < 30):
            for j in range(len(x0)):
                if(x0[j] >= timestamp+(i*4000) and x0[j] <= timestamp+(i*4000+400)):
                    value = x0[j]-(i*4000)
                    trial_spikes.append(value)
        #should go through all 30 trials and get every value and condense them
            i = i+1

        # should create a list of lists 9 of them each one being a node
        node_spike_array.append(trial_spikes)
        node_num = node_num+1

    #print(total_spikes)
    #node_spike_array = total_spikes
    print(node_spike_array)

extinction_array = []
create_arrays_extinction_final(extinction_array)
print(extinction_array)

fig, axs = plt.subplots(3, 3, sharey=True, tight_layout=True)
fig.suptitle('Spike histogram for extinction ms')

i = 0
column_cnt = 0
row_cnt = 0

while(i < 9):
    bins = find_bins(extinction_array[i], 10)

    axs[row_cnt, column_cnt].hist(x=extinction_array[i], bins=bins)
    axs[row_cnt, column_cnt].set_title('pyramidal ' + str(i+1))
    if(i == 8):
        axs[row_cnt, column_cnt].set_title('Interneuron 1 ')
    # axs[row_cnt, column_cnt].ylabel("spikes")
    # axs[row_cnt, column_cnt].xlabel('ms')

    #axs[row_cnt, column_cnt].set_xlim([0,400])


    column_cnt = column_cnt+1
    if(column_cnt > 2):
        column_cnt = 0
        row_cnt = row_cnt+1


    i = i+1

for ax in axs.flat:
    ax.set(xlabel='time(ms)', ylabel='# of spikes')
plt.show()