from bmtk.analyzer.compartment import plot_traces
import matplotlib.pyplot as plt

#_ = plot_traces(config_file='simulation_configWEIGHTS.json', report_path='output/syns_cai.h5', title='tone2pyr')
_ = plot_traces(config_file='simulation_configWEIGHTS.json', report_path='output/syns_pyr2int_cai.h5', title='pyr2int',show=False)
_ = plot_traces(config_file='simulation_configWEIGHTS.json', report_path='output/syns_pyr2pyr_cai.h5', title='pyr2pyr',show=False)
_ = plot_traces(config_file='simulation_configWEIGHTS.json', report_path='output/syns_int2pyr_cai.h5', title='int2pyr',show=False)
plt.show()
