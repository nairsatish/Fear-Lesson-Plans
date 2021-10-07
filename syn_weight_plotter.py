import h5py
import pandas
import numpy
import matplotlib.pyplot as plt
from bmtk.analyzer.compartment import plot_traces

try:
    _ = plot_traces(config_file='simulation_configWEIGHTS.json', report_path='output/syns_shock2int.h5', title='shock2int',show=False)
except:
    pass
try:
    _ = plot_traces(config_file='simulation_configWEIGHTS.json', report_path='output/syns_tone2pyr.h5', title='tone2pyr',show=False)
except:
    pass
_ = plot_traces(config_file='simulation_configWEIGHTS.json', report_path='output/syns_pyr2int.h5', title='pyr2int',show=False)
_ = plot_traces(config_file='simulation_configWEIGHTS.json', report_path='output/syns_pyr2pyr.h5', title='pyr2pyr',show=False)
_ = plot_traces(config_file='simulation_configWEIGHTS.json', report_path='output/syns_int2pyr.h5', title='int2pyr',show=False)
_ = plot_traces(config_file='simulation_configWEIGHTS.json', report_path='output/syns_int2int.h5', title='int2int',show=False)


plt.show()




