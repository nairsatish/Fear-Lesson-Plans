import numpy as np
import matplotlib.pyplot as plt
import h5py
from bmtk.analyzer.cell_vars import _get_cell_report, plot_report
import matplotlib.pyplot as plt
import csv

#PLOT OF ALL INPUTS
#AFTER SOME TIME TONE AND SHOCK COMES ON
#RANDOM INPUTS
#NEXT PANEL COULD BE TONE INPUT AND HTEN SHOCK INPUT
#RASTER PLOT OF WHEN CELLS SPIKE (ISABEL)

#PLOT CSVS OF TONE AND SHOCK INPUT 
from bmtk.analyzer.compartment import plot_traces
import pandas as pd 
from scipy.signal import find_peaks
import pdb

# Load data
config_file = "simulation_config.json"
raster_file = './output/spikes.h5'

mem_pot_file = './output/v_report.h5'
cai_file = './output/cai_report.h5'

shock_file = 'shock_spikes.csv'
tone_file = 'tone_spikes.csv'

# load 
f = h5py.File(mem_pot_file,'r')
g = h5py.File(cai_file,'r')

shock_array = []
with open(shock_file, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    for row in csvreader:
        shock_array.append(row)

print(shock_array)
shock_x = []
shock_y = []
for element in shock_array:
    word = element[0].split('\'')
    print(word[0])
    shock_x.append(int(word[0]))
    shock_y.append(int(word[2]))

tone_array = []
with open(tone_file, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    for row in csvreader:
        tone_array.append(row)

print(tone_array)
tone_x = []
tone_y = []
for element in tone_array:
    word = element[0].split('\'')
    print(word[0])
    tone_x.append(int(word[0]))
    tone_y.append(int(word[2]))

plt.plot(tone_x, tone_y, '.', label="tone input")
plt.plot(shock_x, shock_y, '.', label="shock input")
plt.xlabel("Time elapsed")
plt.ylabel("Node id")
plt.legend()
plt.show()



mem_potential = f['report']['biophysical']['data']
plt.plot(np.arange(0,mem_potential.shape[0]/10,.1),mem_potential[:,0])
plt.text(200,-80,'tone')
plt.text(700,-80,'tone+shock')
plt.text(1600,-80,'tone+shock')
plt.text(2600,-80,'tone')
plt.xlabel('time (ms)')
plt.ylabel('membrane potential (mV)')



_ = plot_traces(config_file='simulation_config.json', node_ids=[0], report_name='v_report')
plot_two = plot_traces(config_file='simulation_config.json', node_ids=[0], report_name='cai_report')
#caiplt = g['report']['biophysical']['data']
#plt.plot(caiplt[:,0])

plt.show()

h = h5py.File('output\\spikes.h5', 'r')
timestamps = h['spikes']['biophysical']['timestamps'][:]
node_ids = h['spikes']['biophysical']['node_ids'][:]



dh = pd.DataFrame({'node_ids':node_ids, 'ts':timestamps})
#print(dh.head())
plt.plot(dh.ts, dh.node_ids, '.')
plt.xlabel("time(ms)")
plt.ylabel("node id")
plt.plot(tone_x, tone_y, '.', label="tone input")
plt.plot(shock_x, shock_y, '.', label="shock input")
plt.legend()
plt.show()


plt.hist(dh.loc[dh.node_ids==0, 'ts'])
plt.ylabel('node id 0 spike #')
plt.xlabel('time elapsed (ms)')
plt.show()

plt.hist(dh.loc[dh.node_ids==1, 'ts'])
plt.ylabel('node id 1 spike #')
plt.xlabel('time elapsed (ms)')
plt.show()

plt.hist(dh.loc[dh.node_ids==2, 'ts'])
plt.ylabel('node id 2 spike #')
plt.xlabel('time elapsed (ms)')
plt.show()

plt.hist(dh.loc[dh.node_ids==3, 'ts'])
plt.ylabel('node id 3 spike #')
plt.xlabel('time elapsed (ms)')
plt.show()

plt.hist(dh.loc[dh.node_ids==4, 'ts'])
plt.ylabel('node id 4 spike #')
plt.xlabel('time elapsed (ms)')
plt.show()

plt.hist(dh.loc[dh.node_ids==5, 'ts'])
plt.ylabel('node id 5 spike #')
plt.xlabel('time elapsed (ms)')
plt.show()

plt.hist(dh.loc[dh.node_ids==6, 'ts'])
plt.ylabel('node id 6 spike #')
plt.xlabel('time elapsed (ms)')
plt.show()

plt.hist(dh.loc[dh.node_ids==7, 'ts'])
plt.ylabel('node id 7 spike #')
plt.xlabel('time elapsed (ms)')
plt.show()

plt.hist(dh.loc[dh.node_ids==8, 'ts'])
plt.ylabel('node id 8 spike #')
plt.xlabel('time elapsed (ms)')
plt.show()

plt.hist(dh.loc[dh.node_ids==9, 'ts'])
plt.ylabel('node id 9 spike #')
plt.xlabel('time elapsed (ms)')
plt.show()

print(dh.loc[dh.node_ids==9, 'ts'])