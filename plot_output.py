import numpy as np
import matplotlib.pyplot as plt
import h5py
from bmtk.analyzer.cell_vars import _get_cell_report, plot_report
import matplotlib.pyplot as plt
import pandas as pd 
from scipy.signal import find_peaks
import pdb

# Load data
config_file = "simulation_config.json"
raster_file = './output/spikes.h5'

mem_pot_file = './output/v_report.h5'
cai_file = './output/cai_report.h5'

# load 
f = h5py.File(mem_pot_file,'r')

mem_potential = f['report']['tone']['data']
plt.plot(np.arange(0,mem_potential.shape[0]/10,.1),mem_potential[:,0])
plt.text(200,-80,'tone')
plt.text(700,-80,'tone+shock')
plt.text(1600,-80,'tone+shock')
plt.text(2600,-80,'tone')
plt.xlabel('time (ms)')
plt.ylabel('membrane potential (mV)')

plt.show()


