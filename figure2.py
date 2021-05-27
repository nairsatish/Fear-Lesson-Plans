from bmtk.analyzer.spike_trains import to_dataframe
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

df = to_dataframe(config_file='simulation_config.json')

df.to_csv('spikedata.csv')

df0 = df.loc[df['node_ids'] == 9]
df0.to_csv('node0.csv')
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

#split values into different arrays
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

#scaling values
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


def find_bins(array, width):
    minimmum = np.min(array)
    maximmum = np.max(array)
    bound_min = -1.0 * (minimmum % width - minimmum)
    bound_max = maximmum - maximmum % width + width
    n = int((bound_max - bound_min) / width) + 1
    bins = np.linspace(bound_min, bound_max, n)
    return bins
bins = find_bins(final_array, 10)
plt.hist(x=final_array, bins=bins)
plt.title('P1')
plt.ylabel("spikes")
plt.xlabel('ms')
plt.xlim([0, 400])
plt.show()
print(len(df0))
print(len(df))

